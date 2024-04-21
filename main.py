from ursina import *
from panda3d.ai import AIWorld, AICharacter
from prefabs.material import Material
from prefabs.entity import cEntity
from prefabs.light import SpotLight
from assets.scripts.BaseEnemy import BaseEnemy
from prefabs.first_person_controller import FirstPersonController

app = Ursina()
player = FirstPersonController()
player.collider = BoxCollider(player, center=(0, player.height / 2, 0), size=(0.5, player.height, 0.5))

# Spawn protection variables
global spawn_protection_duration
spawn_protection_duration = 5  # Duration of spawn protection in seconds
spawn_protected = True

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
material2.texture_scale = Vec2(2, 2)
walls = cEntity(model="assets/objects/imcummingmaze.obj", scale=5, position=(10, 0, 10), collider="mesh", shader=shader)
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

# Create a jumpscare text
jumpscare_text = Text(text="h", y=-0.3, origin=(0, 0), scale=100, color=color.red, background=True, background_color=color.black, enabled=False)

def on_collision():
    global spawn_protected
    global spawn_protection_duration

    if not spawn_protected:  # Check if not spawn protected
        # Reset player position
        player.position = Vec3(0, 1, 0)
        # Show jumpscare text
        jumpscare_text.enabled = True
        invoke(jumpscare_text.disable, delay=2)  # Disable jumpscare text after 1 second
        # Reset spawn protection
        spawn_protected = True
        spawn_protection_duration = 3  # Reset spawn protection duration

def update():
    global spawn_protection_duration
    global spawn_protected

    flashlight_light.direction = camera.forward.normalized()
    flashlight_light.update_values()
    direction_to_player = player.position - enemy.position
    direction_to_player.y = 0
    direction_to_player.normalize()
    enemy.position += direction_to_player * 0.03
    enemy.look_at_2d(player.position, 'y')
    collision_info = enemy.intersects(walls)
    if collision_info.hit:
        collision_normal = collision_info.normal.normalized()
        slide_direction = Vec3(collision_normal.x, 0, collision_normal.z)
        enemy.position += slide_direction * 0.09
    if not spawn_protected and player.intersects(enemy).hit:
        on_collision()

    # Decrease spawn protection duration
    if spawn_protected:
        spawn_protection_duration -= time.dt
        if spawn_protection_duration <= 0:
            spawn_protected = False

Audio("assets/sfx/burningmemory.ogg").play()
window.vsync = True
app.run()
