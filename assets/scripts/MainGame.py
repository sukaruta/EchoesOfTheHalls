from ursina import *
from prefabs.material import Material
from prefabs.entity import cEntity
from prefabs.light import SpotLight
from assets.scripts.BaseEnemy import BaseEnemy
from assets.scripts.SoulOrb import SoulOrb
from prefabs.first_person_controller import FirstPersonController


class MainGame(Entity):

    def __init__(self, **kwargs):
        super().__init__()

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.finished_game = False
        shadee = Shader.load(Shader.GLSL, "assets/shaders/vertex.vert", "assets/shaders/SpotFragment.frag")
        self.bgm = Audio("assets/sfx/burningmemory.ogg")
        self.player = FirstPersonController()
        self.player.collider = BoxCollider(self.player, center=(0, self.player.height / 2, 0),
                                           size=(0.5, self.player.height, 0.5))

        self.flashlight_light = SpotLight(color=color.white, rotation=self.player.camera_pivot.rotation)
        self.flashlight_light.texture = None
        self.flashlight_light.model = None
        self.flashlight_light.setShader(shadee)
        self.flashlight_light.add_script(SmoothFollow(self.player, offset=(0, self.player.height, 0)))

        self.soul_positions = [
            Vec3(12, 1, 3),
            Vec3(-18, 1, 7),
            Vec3(26, 1, -26),
            Vec3(5, 1, 10)
        ]

        self.counter_text = Text(text=f"{self.player.collected_souls} / {len(self.soul_positions)}", parent=camera.ui,
                            font=rf"assets/fonts/DS-DIGII.ttf", y=0.48, x=-0.85)

        for pos in self.soul_positions:
            orb = SoulOrb(model="sphere", color=color.cyan, texture=None, shader=shadee, player=self.player,
                          collider="sphere",
                          font=self.counter_text.font)
            orb.world_position = pos

        material2 = Material()
        material2.texture = load_texture("assets/textures/chipping-painted-wall_albedo")
        material2.specular_map = load_texture("assets/textures/chipping-painted-wall_metallic")
        material2.texture_scale = Vec2(100, 100)
        walls = cEntity(model="assets/objects/imcummingmaze.obj", scale=6, position=(0, 0, 0), collider="mesh",
                        shader=shadee)
        walls.set_material(material2)

        material3 = Material()
        material3.texture = load_texture("assets/textures/floortile.jpg")
        material3.specular_map = load_texture("assets/textures/floortile.jpg")
        floor = cEntity(model="plane", collider="mesh", scale=80, shader=shadee, position=(0, 0.2, 0),
                        rotation=(180, 180, 0), double_sided=True)
        floor.set_material(material3)

        roof = cEntity(model="plane", texture="grass", collider="mesh", scale=80, position=(0, 7, 0), shader=shadee)
        roof.rotation = (180, 180, 0)

        material69 = Material()
        material69.texture = load_texture("assets/textures/kimmonster.png")
        material69.specular_map = load_texture("assets/textures/kimmonster.png")
        enemy = BaseEnemy(model="quad", shader=shadee, position=(6, 3, 0), double_sided=True,
                          scale=(6, 6, material69.texture.width), collider="box", target=self.player, walls=walls,
                          flashlight=self.flashlight_light)
        enemy.collider = BoxCollider(enemy, Vec3(0, 0, 0), Vec3(0.5, 1, 0))
        enemy.set_material(material69)
        enemy.found_player_audio = Audio("assets/sfx/monsters/kim/found_player.wav", autoplay=False)
        enemy.chase_audio = Audio("assets/sfx/monsters/kim/chase_scream.wav", autoplay=False)
        enemy.spawn_locations = [Vec3(27, 0, 27), Vec3(-12, 0, 25), Vec3(-11, 0, -2), Vec3(-25, 0, -12)]

        self.flashlight_light.update_values()
        self.bgm.play()

    def update(self):
        if (self.player.collected_souls == len(self.soul_positions)) and not self.finished_game:
            self.finished_game = True
            scene.clear()
            Entity(parent=camera.ui, model='quad', texture="assets/videos/gratitude.mp4", scale=(2, 1), z=100)
            invoke(application.quit, delay=15)
        self.flashlight_light.direction = camera.forward.normalized()
        self.flashlight_light.update_values()

        self.counter_text.text = f"{self.player.collected_souls} / {len(self.soul_positions)}"

        if self.player.is_dead:
            self.bgm.stop()
