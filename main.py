from ursina import *
import json
from assets.scripts.MainGame import MainGame


def start_game():
    scene.clear()
    data = json.load(open("assets/levels_info.json"))
    MainGame(level=1,
             obj_dir=data["room1"]["obj_dir"],
             room_audio=data["room1"]["room_audio"],
             player_pos=Vec3(data["room1"]["playerPos"][0], data["room1"]["playerPos"][1],
                             data["room1"]["playerPos"][2]),
             soul_positions=[
                 Vec3(data["room1"]["soul_positions"][0][0], data["room1"]["soul_positions"][0][1],
                      data["room1"]["soul_positions"][0][2]),
                 Vec3(data["room1"]["soul_positions"][1][0], data["room1"]["soul_positions"][1][1],
                      data["room1"]["soul_positions"][1][2]),
                 Vec3(data["room1"]["soul_positions"][2][0], data["room1"]["soul_positions"][2][1],
                      data["room1"]["soul_positions"][2][2]),
                 Vec3(data["room1"]["soul_positions"][3][0], data["room1"]["soul_positions"][3][1],
                      data["room1"]["soul_positions"][3][2])
             ],
             enemy_init_pos=Vec3(data["room1"]["enemy"]["init_pos"][0], data["room1"]["enemy"]["init_pos"][1],
                                 data["room1"]["enemy"]["init_pos"][2]),
             enemy_spawn_locations=[
                 Vec3(data["room1"]["enemy"]["spawn_locations"][0][0], data["room1"]["enemy"]["spawn_locations"][0][1],
                      data["room1"]["enemy"]["spawn_locations"][0][2]),
                 Vec3(data["room1"]["enemy"]["spawn_locations"][1][0], data["room1"]["enemy"]["spawn_locations"][1][1],
                      data["room1"]["enemy"]["spawn_locations"][1][2]),
                 Vec3(data["room1"]["enemy"]["spawn_locations"][2][0], data["room1"]["enemy"]["spawn_locations"][2][1],
                      data["room1"]["enemy"]["spawn_locations"][2][2]),
                 Vec3(data["room1"]["enemy"]["spawn_locations"][3][0], data["room1"]["enemy"]["spawn_locations"][3][1],
                      data["room1"]["enemy"]["spawn_locations"][3][2])
             ],
             enemy_texture=data["room1"]["enemy"]["texture"],
             enemy_found_player_audio=data["room1"]["enemy"]["found_player_audio"],
             enemy_chase_audio=data["room1"]["enemy"]["chase_audio"],
             chase_scream_short=data["room1"]["enemy"]["chase_scream_short"],
             jumpscare_texture=data["room1"]["enemy"]["jumpscare_texture"],
             data=data
             )


def init_game():
    scene.clear()
    Entity(parent=camera.ui, model='quad', texture="assets/videos/dialogue.mp4", scale=(2, 1), z=100)
    Audio("assets/sfx/death_screen.wav")
    invoke(start_game, delay=7)


app = Ursina(title="EotH", icon="assets/textures/echoes.ico", borderless=True, development_mode=False, fullscreen=True)
menu_video_sound = Audio("assets/sfx/neon_sounds.mp3")
menu_video_sound.loop = True
menu_video_sound.play()
menu_bg = Entity(parent=camera.ui, model='quad', texture="assets/videos/neon_flickering.mp4", scale=(2, 1), z=100)
start = Button(radius=0, text='Start', scale=(.2, .1), y=-0.1, on_click=init_game)
menu_icon = Entity(parent=camera.ui, model='quad', texture="assets/textures/echoes.png", scale=0.5, y=0.3)
start.alpha = 0.4

window.vsync = True
app.run()
