from ursina import *
from prefabs.first_person_controller import FirstPersonController

app = Ursina()
player = FirstPersonController()
floor = Entity(model="cube", texture="grass", scale=(200, 0, 200), collider="box")
lebron = Entity(model="cube", texture="/textures/sunshine.png", scale=(0, 5, 5), collider="quad")
lebron.add_script(SmoothFollow(target=player, offset=[2, 0, 2], speed=100))
sunshine = Audio(add_to_scene_entities=lebron, sound_file_name="/sfx/sfx_sunshine.mp3", autoplay=True)

darkbron = Entity(model="cube", texture="/textures/darkshine.jpeg", scale=(0, 5, 5), collider="box")
darkbron.add_script(SmoothFollow(target=player, offset=[5, 0, 5], speed=0.5))
darkshine = Audio(add_to_scene_entities=darkbron, sound_file_name="/sfx/sfx_darkshine.mp3", autoplay=True)
darkshine.loop = True
darkshine.loops = 100
window.vsync = True
app.run()
