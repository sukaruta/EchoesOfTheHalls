from ursina import *
from panda3d.ai import AIWorld, AICharacter
from prefabs.material import Material
from prefabs.entity import cEntity
from prefabs.light import SpotLight
from assets.scripts.BaseEnemy import BaseEnemy
from prefabs.first_person_controller import FirstPersonController

app = Ursina()
player = FirstPersonController()
flashlight = cEntity()
shader = Shader.load(Shader.GLSL, "assets/shaders/vertex.vert", "assets/shaders/SpotFragment.frag")
flashlight_light = SpotLight(color=color.white, rotation=player.camera_pivot.rotation)
flashlight_light.texture = None
flashlight_light.model = None
flashlight_light.setShader(shader)
flashlight_light.add_script(SmoothFollow(player, offset=(0, player.height, 0)))

material69 = Material()
material69.texture = load_texture("assets/textures/kimmonster.png")
material69.specular_map = load_texture("assets/textures/kimmonster.png")
enemy = BaseEnemy(model="quad", shader=shader, position=(2, 3, 0), double_sided=True, scale=6, collider="mesh")
enemy.set_material(material69)

material2 = Material()
material2.texture = load_texture("assets/textures/chipping-painted-wall_albedo")
material2.specular_map = load_texture("assets/textures/chipping-painted-wall_metallic")
material2.texture_scale = Vec2(2, 2)
walls = cEntity(model="assets/objects/testroom2.obj", scale=50, position=(10, 0, 10), collider="mesh", shader=shader)
walls.set_material(material2)

material3 = Material()
material3.texture = load_texture("assets/textures/floortile.jpg")
material3.specular_map = load_texture("assets/textures/floortile.jpg")
floor = cEntity(model="testroom2_floor.obj", collider="box", scale=(50, 50, 50))
floor.set_material(material3)
floor.shader = shader

roof = cEntity(model="plane", texture="grass", collider="box", scale=(100, 100, 100), position=(0, 7, 0), shader=shader)
roof.rotation = (180, 180, 0)

flashlight_light.update_values()

def update():
    flashlight_light.direction = camera.forward.normalized()
    flashlight_light.update_values()
    enemy.look_at_2d(player.position, 'y')
Audio("assets/sfx/burningmemory.ogg").play()
window.vsync = True
app.run()
