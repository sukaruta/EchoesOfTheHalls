from ursina import *
from prefabs.entity import cEntity


class BaseEnemy(cEntity, Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.vision = None
        self.speed = 5
        self.gravity = 1
        self.pursuing_player = False
        self.pursuit_timeout = None
        self.player_path = []
        self.spawn_locations = []

        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        self.look_at_2d(self.target.position, 'y')
        vision_range = 50
        if self.pursuing_player:
            vision_range = 10
        self.vision = raycast(
            (self.world_position.x, 0, self.world_position.z) + (self.up.x, self.target.height - 1.3, self.up.z),
            self.forward, distance=vision_range, ignore=[self])
        if ((self.vision.hit and (self.vision.entities[0] == self.target)) and not self.pursuing_player) and not self.target.is_dead:
            # Begin chase
            self.pursuing_player = True
            self.player_path.append(self.target.world_position)
            if not self.found_player_audio.playing and self.pursuing_player:
                self.found_player_audio.play()
                self.chase_audio.loops = 50
                self.chase_audio.loop = True
                invoke(self.chase_audio.play, delay=self.found_player_audio.length)
            self.pursuit()

        if self.pursuing_player:
            self.player_path.append(self.target.world_position)
            self.pursuit()

    def is_moving(self):
        if self.direction is None:
            return False
        elif self.direction.x + self.direction.y + self.direction.z != 0:
            return True
        return False

    def pursuit(self):
        self.set_volume_proximity()

        if self.pursuit_timeout is None or not self.pursuit_timeout.started:
            self.pursuit_timeout = invoke(self.stop_pursuit, delay=11)

        for playerPos in self.player_path:
            self.world_position = lerp(
                self.world_position,
                Vec3(playerPos.x, self.world_position.y, playerPos.z),
                time.dt * 1)
            self.player_path.pop()

        collision_info = self.intersects(self.target)
        if collision_info.hit and not self.target.is_dead:
            self.jumpscare()

        if not self.chase_audio.playing and self.pursuing_player:
            self.chase_audio.loops = 50
            self.chase_audio.loop = True
            self.chase_audio.play()

    def stop_pursuit(self):
        def enable_flashlight():
            self.flashlight.world_position = self.target.world_position
            self.flashlight.add_script(SmoothFollow(self.target, offset=(0, self.target.height, 0)))

        def disable_flashlight():
            self.flashlight.scripts.pop()
            self.flashlight.world_position = Vec3(0, -10, 0)

        self.pursuit_timeout = None
        if not self.target.is_dead:
            self.pursuing_player = False
            self.chase_audio.stop(destroy=False)
            self.chase_audio.loop = False
            disable_flashlight()
            invoke(enable_flashlight, delay=1)
            new_spawn = random.choice(self.spawn_locations)
            self.world_position = (new_spawn.x, self.world_position.y, new_spawn.z)

    def jumpscare(self):
        self.target.is_dead = True
        self.pursuing_player = False
        self.chase_audio.loop = False
        self.found_player_audio.stop()
        self.chase_audio.stop()
        scene.clear()
        Entity(model="quad", texture="textures/kimjump.png", parent=camera.ui, scale=(2, 1))
        jumpscare_sound = self.chase_scream_short
        jumpscare_sound.loop = True
        jumpscare_sound.loops = 100
        jumpscare_sound.play()
        invoke(self.death_screen, delay=5)

    def set_volume_proximity(self):
        volume = max(1 - distance(self.target.position, self.position) / 30, 0)
        self.chase_audio.volume = volume

    @staticmethod
    def death_screen():
        scene.clear()
        Entity(model="quad", parent=camera.ui, texture="videos/death_screen.mp4", scale=(2, 1))
        Audio("sfx/death_screen.wav", auto_destroy=True)
        print("IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT.")
        invoke(application.quit, delay=7)
