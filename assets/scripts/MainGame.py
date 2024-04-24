from ursina import *
from prefabs.material import Material
from prefabs.entity import cEntity
from prefabs.light import SpotLight
from assets.scripts.BaseEnemy import BaseEnemy
from assets.scripts.SoulOrb import SoulOrb
from prefabs.first_person_controller import FirstPersonController
import json


class MainGame(Entity):

    def __init__(self, **kwargs):
        super().__init__()
        self.obj_dir = ""
        self.room_audio = ""
        self.player_pos = Vec3(0, 0, 0)
        self.soul_positions = []
        self.enemy_init_pos = Vec3(0, 0, 0)
        self.enemy_spawn_locations = []
        self.enemy_texture = ""
        self.enemy_found_player_audio = ""
        self.enemy_chase_audio = ""
        self.chase_scream_short = ""
        self.level = 1
        self.finished_level = False

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
        self.floor = cEntity(model="plane", collider="mesh", scale=80, shader=self.shader, position=(0, 0.2, 0),
                             rotation=(180, 180, 0), double_sided=True)
        self.floor.set_material(floor_material)

        roof = cEntity(model="plane", texture="grass", collider="mesh", scale=80, position=(0, 7, 0),
                       shader=self.shader)
        roof.rotation = (180, 180, 0)

        enemy_material = Material()
        enemy_material.texture = load_texture(self.enemy_texture)
        enemy_material.specular_map = load_texture(self.enemy_texture)
        enemy = BaseEnemy(model="quad", shader=self.shader, position=(6, 3, 0), double_sided=True,
                          scale=(6, 6, enemy_material.texture.width), collider="box", target=self.player,
                          walls=self.walls,
                          flashlight=self.flashlight_light)
        enemy.collider = BoxCollider(enemy, Vec3(0, 0, 0), Vec3(0.5, 1, 0))
        enemy.set_material(enemy_material)
        enemy.found_player_audio = Audio(self.enemy_found_player_audio, autoplay=False)
        enemy.chase_audio = Audio(self.enemy_chase_audio, autoplay=False)
        enemy.chase_scream_short = Audio(self.chase_scream_short, autoplay=False)
        enemy.spawn_locations = self.enemy_spawn_locations

        enemy.disable()
        self.flashlight_light.update_values()
        # self.bgm.play()

    def update(self):
        if (self.player.collected_souls == len(self.soul_positions)) and not self.finished_level:
            self.finished_level = True
            self.load_next_level()
            # Entity(parent=camera.ui, model='quad', texture="assets/videos/gratitude.mp4", scale=(2, 1), z=100)
            # invoke(application.quit, delay=15)
        self.flashlight_light.direction = camera.forward.normalized()
        self.flashlight_light.update_values()

        self.counter_text.text = f"{self.player.collected_souls} / {len(self.soul_positions)}"

        if self.player.is_dead:
            self.load_next_level()
            self.bgm.stop()

    def load_next_level(self):
        self.level += 1
        destroy(self.walls)

        data = json.load(open("assets/levels_info.json"))

        self.player.world_position = data[f"room{self.level}"]["playerPos"]

        wall_material = Material()
        wall_material.texture = load_texture("assets/textures/chipping-painted-wall_albedo")
        wall_material.specular_map = load_texture("assets/textures/chipping-painted-wall_metallic")
        wall_material.texture_scale = Vec2(100, 100)
        self.walls = cEntity(model=f"assets/objects/room{self.level}.obj", scale=6, position=(0, -0.5, 0), collider="mesh",
                             shader=self.shader)
        self.walls.set_material(wall_material)
        for vec in data[f"room{self.level}"]["soul_positions"]:
            self.soul_positions.append(Vec3(vec[0], vec[1], vec[2]))
            orb = SoulOrb(model="sphere", color=color.cyan, texture=None, shader=self.shader, player=self.player,
                          collider="sphere",
                          font=self.counter_text.font
                          )
            orb.world_position = Vec3(vec[0], vec[1], vec[2])
