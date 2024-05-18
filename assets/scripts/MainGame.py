from ursina import *
from prefabs.material import Material
from prefabs.entity import cEntity
from prefabs.light import SpotLight
from assets.scripts.BaseEnemy import BaseEnemy
from assets.scripts.CatchEnemy import CatchEnemy
from assets.scripts.SoulOrb import SoulOrb
from prefabs.first_person_controller import FirstPersonController


class MainGame(Entity):

    def __init__(self, **kwargs):
        super().__init__()
        self.jumpscare_warn = None
        self.enemy_found_player_audio = None
        self.enemy_screech_audio = ""
        self.obj_dir = ""
        self.room_audio = ""
        self.player_pos = Vec3(0, 0, 0)
        self.soul_positions = []
        self.enemy_init_pos = Vec3(0, 0, 0)
        self.enemy_spawn_locations = []
        self.enemy_texture = ""
        self.enemy_screech_audio = ""
        self.enemy_chase_audio = ""
        self.chase_scream_short = ""
        self.jumpscare_texture = ""
        self.level = 1
        self.finished_level = False
        self.data = None

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.shader = Shader.load(Shader.GLSL, "assets/shaders/vertex.vert", "assets/shaders/SpotFragment.frag")
        self.bgm = Audio(self.room_audio)
        self.player = FirstPersonController()
        self.player.collected_souls = 0
        self.player.world_position = self.player_pos
        self.player.collider = BoxCollider(self.player, center=(0, self.player.height / 2, 0),
                                           size=(0.5, self.player.height, 0.5))

        self.flashlight_light = SpotLight(color=color.white, rotation=self.player.camera_pivot.rotation)
        self.flashlight_light.texture = None
        self.flashlight_light.model = None
        self.flashlight_light.setShader(self.shader)
        self.flashlight_light.add_script(SmoothFollow(self.player, offset=(0, self.player.height, 0)))

        self.counter_text = Text(text=f"{self.player.collected_souls} / {len(self.soul_positions)}", parent=camera.ui,
                                 font=rf"assets/fonts/DS-DIGII.ttf", y=0.48, x=-0.85)

        wall_material = Material()
        wall_material.texture = load_texture("assets/textures/chipping-painted-wall_albedo")
        wall_material.specular_map = load_texture("assets/textures/chipping-painted-wall_metallic")
        wall_material.texture_scale = Vec2(100, 100)
        self.walls = cEntity(model=self.obj_dir, scale=6, position=(0, 0, 0), collider="mesh",
                             shader=self.shader)
        self.walls.set_material(wall_material)

        for pos in self.soul_positions:
            orb = SoulOrb(model="sphere", color=color.cyan, texture=None, shader=self.shader, player=self.player,
                          collider="sphere",
                          font=self.counter_text.font
                          )
            orb.world_position = pos

        floor_material = Material()
        floor_material.texture = load_texture("assets/textures/floortile.jpg")
        floor_material.specular_map = load_texture("assets/textures/floortile.jpg")
        floor_material.texture_scale = Vec2(10, 10)
        self.floor = cEntity(model="plane", collider="mesh", scale=80, shader=self.shader, position=(0, 0.2, 0), double_sided=True)
        self.floor.set_material(floor_material)

        roof_material = Material()
        roof_material.texture = load_texture("assets/textures/plaster.jpg")
        roof_material.specular_map = load_texture("assets/textures/plaster.jpg")
        roof = cEntity(model="plane", collider="mesh", scale=80, position=(0, 7, 0),
                       shader=self.shader)
        roof.rotation = (180, 180, 0)

        enemy_material = Material()
        enemy_material.texture = load_texture(self.enemy_texture)
        enemy_material.specular_map = load_texture(self.enemy_texture)
        self.enemy = BaseEnemy(model="quad", shader=self.shader, position=(6, 3, 0), double_sided=True,
                               scale=(6, 6, enemy_material.texture.width), collider="box", target=self.player,
                               walls=self.walls,
                               flashlight=self.flashlight_light,
                               jumpscare_texture=self.jumpscare_texture,
                               finished_level=self.finished_level
                               )
        self.enemy.collider = BoxCollider(self.enemy, Vec3(0, 0, 0), Vec3(0.5, 1, 0))
        self.enemy.set_material(enemy_material)
        self.enemy.found_player_audio = Audio(self.enemy_found_player_audio, autoplay=False)
        self.enemy.chase_audio = Audio(self.enemy_chase_audio, autoplay=False)
        self.enemy.chase_scream_short = Audio(self.chase_scream_short, autoplay=False)
        self.enemy.spawn_locations = self.enemy_spawn_locations

        # self.enemy.disable()
        self.flashlight_light.update_values()
        self.bgm.play()

    def update(self):
        if (self.player.collected_souls == len(self.soul_positions)) and not self.finished_level:
            self.finished_level = True
            self.loading_screen()
        self.flashlight_light.direction = camera.forward.normalized()
        self.flashlight_light.update_values()

        self.counter_text.text = f"{self.player.collected_souls} / {len(self.soul_positions)}"

        if self.player.is_dead:
            self.load_next_level()
            self.bgm.stop()

    def loading_screen(self):
        self.level += 1
        if self.enemy.pursuing_player and not self.level - 1 == 3:
            self.enemy.chase_audio.stop()
            self.enemy.chase_scream_short.stop()
            self.enemy.found_player_audio.stop()
            self.enemy.pursuit_timeout.kill()
        destroy(self.walls)
        destroy(self.enemy)
        if self.level > len(self.data):
            Entity(parent=camera.ui, model='quad', texture="assets/videos/finish.mp4", scale=(2, 1), z=100)
            finish_audio = Audio("assets/videos/finish.mp4", autoplay=True)
            invoke(application.quit, delay=finish_audio.length)
            return
        next_level = Entity(parent=camera.ui, model='quad', texture="assets/videos/next_level.mp4", scale=(2, 1), z=100)
        next_level_audio = Audio("assets/video/next_level.mp4")
        invoke(destroy, next_level, delay=6.50)
        invoke(destroy, next_level_audio, delay=6.50)
        invoke(self.load_next_level, delay=6.50)

    def load_next_level(self):
        if self.level > len(self.data):
            Entity(parent=camera.ui, model='quad', texture="assets/videos/finish.mp4", scale=(2, 1), z=100)
            finish_audio = Audio("assets/videos/finish.mp4", autoplay=True)
            invoke(application.quit, delay=finish_audio.length)
            return

        self.player.world_position = self.data[f"room{self.level}"]["playerPos"]

        wall_material = Material()
        wall_material.texture = load_texture("assets/textures/chipping-painted-wall_albedo")
        wall_material.specular_map = load_texture("assets/textures/chipping-painted-wall_metallic")
        wall_material.texture_scale = Vec2(100, 100)
        self.walls = cEntity(model=f"assets/objects/room{self.level}.obj", scale=6, position=(0, -0.5, 0),
                             collider="mesh",
                             shader=self.shader)
        self.walls.set_material(wall_material)
        for vec in self.data[f"room{self.level}"]["soul_positions"]:
            self.soul_positions.append(Vec3(vec[0], vec[1], vec[2]))
            orb = SoulOrb(model="sphere", color=color.cyan, texture=None, shader=self.shader, player=self.player,
                          collider="sphere",
                          font=self.counter_text.font
                          )
            orb.world_position = Vec3(vec[0], vec[1], vec[2])

        self.enemy_texture = self.data[f"room{self.level}"]["enemy"]["texture"]
        enemy_material = Material()
        enemy_material.texture = load_texture(self.enemy_texture)
        enemy_material.specular_map = load_texture(self.enemy_texture)

        if self.level == 3:
            self.enemy = CatchEnemy(model="quad",
                                    shader=self.shader,
                                    position=Vec3(
                                        self.data[f"room{self.level}"]["enemy"]["init_pos"][0],
                                        self.data[f"room{self.level}"]["enemy"]["init_pos"][1],
                                        self.data[f"room{self.level}"]["enemy"]["init_pos"][2]),
                                    collider="box",
                                    double_sided=True,
                                    scale=(6, 6, enemy_material.texture.width),
                                    target=self.player,
                                    walls=self.walls,
                                    flashlight=self.flashlight_light,
                                    jumpscare_texture=self.data[f"room{self.level}"]["enemy"]["jumpscare_texture"],
                                    finished_level=self.finished_level
                                    )
            self.enemy.collider = BoxCollider(self.enemy, Vec3(0, 0, 0), Vec3(0.5, 1, 0))
            self.enemy.set_material(enemy_material)
            self.enemy.screech = Audio(self.data[f"room{self.level}"]["enemy"]["screech"], autoplay=False)
            self.enemy.jumpscare_warn_sound = Audio(self.data[f"room{self.level}"]["enemy"]["jumpscare_warn"], autoplay=False)
            self.enemy.jumpscare_sound = Audio(self.data[f"room{self.level}"]["enemy"]["jumpscare"], autoplay=False)
            self.enemy.spawn_locations = [
                Vec3(self.data[f"room{self.level}"]["enemy"]["spawn_locations"][0][0],
                     self.data[f"room{self.level}"]["enemy"]["spawn_locations"][0][1],
                     self.data[f"room{self.level}"]["enemy"]["spawn_locations"][0][2]),
                Vec3(self.data[f"room{self.level}"]["enemy"]["spawn_locations"][1][0],
                     self.data[f"room{self.level}"]["enemy"]["spawn_locations"][1][1],
                     self.data[f"room{self.level}"]["enemy"]["spawn_locations"][1][2]),
                Vec3(self.data[f"room{self.level}"]["enemy"]["spawn_locations"][2][0],
                     self.data[f"room{self.level}"]["enemy"]["spawn_locations"][2][1],
                     self.data[f"room{self.level}"]["enemy"]["spawn_locations"][2][2]),
                Vec3(self.data[f"room{self.level}"]["enemy"]["spawn_locations"][3][0],
                     self.data[f"room{self.level}"]["enemy"]["spawn_locations"][3][1],
                     self.data[f"room{self.level}"]["enemy"]["spawn_locations"][3][2])
            ]
        else:
            self.enemy = BaseEnemy(model="quad",
                                   shader=self.shader,
                                   position=Vec3(
                                       self.data[f"room{self.level}"]["enemy"]["init_pos"][0],
                                       self.data[f"room{self.level}"]["enemy"]["init_pos"][1],
                                       self.data[f"room{self.level}"]["enemy"]["init_pos"][2]),
                                   collider="box",
                                   double_sided=True,
                                   scale=(6, 6, enemy_material.texture.width),
                                   target=self.player,
                                   walls=self.walls,
                                   flashlight=self.flashlight_light,
                                   jumpscare_texture=self.data[f"room{self.level}"]["enemy"]["jumpscare_texture"],
                                   finished_level=self.finished_level
                                   )
            self.enemy.collider = BoxCollider(self.enemy, Vec3(0, 0, 0), Vec3(0.5, 1, 0))
            self.enemy.set_material(enemy_material)
            self.enemy_found_player_audio = self.data[f"room{self.level}"]["enemy"]["found_player_audio"]
            self.enemy_chase_audio = self.data[f"room{self.level}"]["enemy"]["found_player_audio"]
            self.chase_scream_short = self.data[f"room{self.level}"]["enemy"]["chase_scream_short"]
            self.enemy.found_player_audio = Audio(self.enemy_found_player_audio, autoplay=False)
            self.enemy.chase_audio = Audio(self.enemy_chase_audio, autoplay=False)
            self.enemy.chase_scream_short = Audio(self.chase_scream_short, autoplay=False)
            self.enemy.spawn_locations = [
                Vec3(self.data[f"room{self.level}"]["enemy"]["spawn_locations"][0][0],
                     self.data[f"room{self.level}"]["enemy"]["spawn_locations"][0][1],
                     self.data[f"room{self.level}"]["enemy"]["spawn_locations"][0][2]),
                Vec3(self.data[f"room{self.level}"]["enemy"]["spawn_locations"][1][0],
                     self.data[f"room{self.level}"]["enemy"]["spawn_locations"][1][1],
                     self.data[f"room{self.level}"]["enemy"]["spawn_locations"][1][2]),
                Vec3(self.data[f"room{self.level}"]["enemy"]["spawn_locations"][2][0],
                     self.data[f"room{self.level}"]["enemy"]["spawn_locations"][2][1],
                     self.data[f"room{self.level}"]["enemy"]["spawn_locations"][2][2]),
                Vec3(self.data[f"room{self.level}"]["enemy"]["spawn_locations"][3][0],
                     self.data[f"room{self.level}"]["enemy"]["spawn_locations"][3][1],
                     self.data[f"room{self.level}"]["enemy"]["spawn_locations"][3][2])
            ]

        # self.enemy.disable()

        self.finished_level = False
