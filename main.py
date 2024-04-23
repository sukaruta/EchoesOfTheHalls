from ursina import *
from assets.scripts.MainGame import MainGame


def start_game():
    scene.clear()
    MainGame()


def init_game():
    scene.clear()
    Entity(parent=camera.ui, model='quad', texture="assets/videos/dialogue.mp4", scale=(2, 1), z=100)
    Audio("assets/sfx/death_screen.wav").play()
    invoke(start_game, delay=7)


app = Ursina(fullscreen=True, icon="assets/textures/echoes.ico")
menu_video_sound = Audio("assets/sfx/neon_sounds.mp3")
menu_video_sound.loop = True
menu_video_sound.play()
menu_bg = Entity(parent=camera.ui, model='quad', texture="assets/videos/neon_flickering.mp4", scale=(2, 1), z=100)
start = Button(radius=0, text='Start (BETA)', scale=(.2, .1), y=-0.1, on_click=init_game)
menu_icon = Entity(parent=camera.ui, model='quad', texture="assets/textures/echoes.png", scale=0.5, y=0.3)
start.alpha = 0.4

window.vsync = True
app.run()

# bgm = Audio("assets/sfx/burningmemory.ogg")
# player = FirstPersonController()
# player.collider = BoxCollider(player, center=(0, player.height / 2, 0), size=(0.5, player.height, 0.5))

# shader = Shader.load(Shader.GLSL, "assets/shaders/vertex.vert", "assets/shaders/SpotFragment.frag")
#
# soul_positions = [
#     Vec3(12, 1, 3),
#     Vec3(-18, 1, 7),
#     Vec3(26, 1, -26),
#     Vec3(5, 1, 10)
# ]
#
# counter_text = Text(text=f"{player.collected_souls} / {len(soul_positions)}", parent=camera.ui, font=rf"assets/fonts/DS-DIGII.ttf", y=0.48, x=-0.85)
#
# for pos in soul_positions:
#     orb = SoulOrb(model="sphere", color=color.cyan, texture=None, shader=shader, player=player, collider="sphere", font=counter_text.font)
#     orb.world_position = pos
#
# flashlight_light = SpotLight(color=color.white, rotation=player.camera_pivot.rotation)
# flashlight_light.texture = None
# flashlight_light.model = None
# flashlight_light.setShader(shader)
# flashlight_light.add_script(SmoothFollow(player, offset=(0, player.height, 0)))
#
#
# material2 = Material()
# material2.texture = load_texture("assets/textures/chipping-painted-wall_albedo")
# material2.specular_map = load_texture("assets/textures/chipping-painted-wall_metallic")
# material2.texture_scale = Vec2(100, 100)
# walls = cEntity(model="assets/objects/imcummingmaze.obj", scale=6, position=(0, 0, 0), collider="mesh", shader=shader)
# walls.set_material(material2)
#
# material3 = Material()
# material3.texture = load_texture("assets/textures/floortile.jpg")
# material3.specular_map = load_texture("assets/textures/floortile.jpg")
# floor = cEntity(model="plane", collider="mesh", scale=80, shader=shader, position=(0, 0.2, 0), rotation=(180, 180, 0), double_sided=True)
# floor.set_material(material3)
#
# roof = cEntity(model="plane", texture="grass", collider="mesh", scale=80, position=(0, 7, 0), shader=shader)
# roof.rotation = (180, 180, 0)
#
# material69 = Material()
# material69.texture = load_texture("assets/textures/kimmonster.png")
# material69.specular_map = load_texture("assets/textures/kimmonster.png")
# enemy = BaseEnemy(model="quad", shader=shader, position=(6, 3, 0), double_sided=True, scale=(6, 6, material69.texture.width), collider="box", target=player, walls=walls, flashlight=flashlight_light)
# enemy.collider = BoxCollider(enemy, Vec3(0, 0, 0), Vec3(0.5, 1, 0))
# enemy.set_material(material69)
# enemy.found_player_audio = Audio("assets/sfx/monsters/kim/found_player.wav", autoplay=False)
# enemy.chase_audio = Audio("assets/sfx/monsters/kim/chase_scream.wav", autoplay=False)
# enemy.spawn_locations = [Vec3(27, 0, 27), Vec3(-12, 0, 25), Vec3(-11, 0, -2), Vec3(-25, 0, -12)]
#
# flashlight_light.update_values()
#
#
# enemy.disable()
#
#
# def update():
#     flashlight_light.direction = camera.forward.normalized()
#     flashlight_light.update_values()
#
#     counter_text.text = f"{player.collected_souls} / {len(soul_positions)}"
#
#     if player.is_dead:
#         bgm.stop()
#
#
# bgm.play()
# window.vsync = True
# app.run()
