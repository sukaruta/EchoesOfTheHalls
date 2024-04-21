from ursina import *
from prefabs.material import Material
from prefabs.entity import cEntity
from prefabs.light import SpotLight
from assets.scripts.BaseEnemy import BaseEnemy
from prefabs.first_person_controller import FirstPersonController

app = Ursina()
player = FirstPersonController()
player.position = (5, 0, 5)
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
enemy.collider = 'box'

material2 = Material()
material2.texture = load_texture("assets/textures/chipping-painted-wall_albedo")
material2.specular_map = load_texture("assets/textures/chipping-painted-wall_metallic")
material2.texture_scale = Vec2(100, 100)
walls = cEntity(model="assets/objects/imcummingmaze.obj", scale=6, position=(0, 0, 0), collider="mesh", shader=shader)
walls.set_material(material2)

material3 = Material()
material3.texture = load_texture("assets/textures/floortile.jpg")
material3.specular_map = load_texture("assets/textures/floortile.jpg")
floor = cEntity(model="plane", collider="box", scale=80, shader=shader, position=(0, 0.2, 0), rotation=(180, 180, 0), double_sided=True)
floor.set_material(material3)

roof = cEntity(model="plane", texture="grass", collider="box", scale=80, position=(0, 7, 0), shader=shader)
roof.rotation = (180, 180, 0)

flashlight_light.update_values()

def update():
    flashlight_light.direction = camera.forward.normalized()
    flashlight_light.update_values()
    direction_to_player = player.position - enemy.position
    distance_to_player = direction_to_player.length()
    direction_to_player.y = 0
    direction_to_player.normalize()
    enemy.position += direction_to_player * 0.03
    enemy.look_at_2d(player.position, 'y')
    collision_info = enemy.intersects(walls)
    if collision_info.hit:
        collision_normal = collision_info.normal.normalized()
        slide_direction = Vec3(collision_normal.x, 0, collision_normal.z)
        enemy.position += slide_direction * 0.09


Audio("assets/sfx/burningmemory.ogg").play()
window.vsync = True
app.run()