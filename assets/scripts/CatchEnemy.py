from ursina import *
from prefabs.entity import cEntity


class CatchEnemy(cEntity, Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.jumpscare_timer = None
        self.player_vision = None
        self.vision = None
        self.speed = 5
        self.gravity = 1
        self.pursuing_player = False
        self.jumpscare_texture = ""
        self.player_path = []
        self.spawn_locations = []
        self.screech = None
        self.in_caught_sequence = False
        self.in_jumpscare_warn_sequence = False

        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        self.look_at_2d(self.target.position, 'y')
        vision_range = 50
        self_vision_range = 50

        self.player_vision = raycast(
            (self.target.world_position.x, 0, self.target.world_position.z) + (
                self.target.up.x, self.target.height, self.target.up.z),
            self.target.forward, distance=vision_range, ignore=[self.target])
        if ((self.player_vision.hit and (self.player_vision.entities[0] == self)) and not self.target.is_dead) and not self.in_caught_sequence:
            self.in_caught_sequence = True
            if self.jumpscare_timer is not None:
                self.jumpscare_timer.kill()
                self.jumpscare_timer = None
            self.screech.play()
            invoke(self.run_away, delay=2)

        self.vision = raycast(
                (self.world_position.x, 0, self.world_position.z) + (self.up.x, self.target.height, self.up.z),
                self.forward, distance=self_vision_range, ignore=[self])

        if (((self.vision.hit and (self.vision.entities[0] == self.target)) and not self.pursuing_player) and not self.target.is_dead) and not self.in_caught_sequence:
            self.pursuing_player = True
            self.player_path.append(self.target.world_position)
            self.pursuit()
            return

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
        if self.in_caught_sequence:
            return

        for playerPos in self.player_path:
            self.world_position = lerp(
                self.world_position,
                Vec3(playerPos.x, self.world_position.y, playerPos.z),
                time.dt * 1)
            self.player_path.pop()

        if distance(self.position, self.target.position) < 0.5 and self.jumpscare_timer is None:
            self.jumpscare_warn()

    def run_away(self):
        def enable_flashlight():
            self.flashlight.world_position = self.target.world_position
            self.flashlight.add_script(SmoothFollow(self.target, offset=(0, self.target.height, 0)))

        def disable_flashlight():
            self.flashlight.scripts = []
            self.flashlight.world_position = Vec3(0, -10, 0)

        if not self.target.is_dead:
            self.player_path = []
            self.pursuing_player = False
            disable_flashlight()
            invoke(enable_flashlight, delay=1)
            new_spawn = random.choice(self.spawn_locations)
            self.world_position = (new_spawn.x, self.world_position.y, new_spawn.z)

        self.in_caught_sequence = False

    def jumpscare_warn(self):
        self.jumpscare_warn_sound.play()
        self.jumpscare_timer = invoke(self.jumpscare, delay=self.jumpscare_warn_sound.length)

    def jumpscare(self):
        self.target.is_dead = True
        self.pursuing_player = False
        scene.clear()
        Entity(model="quad", texture=self.jumpscare_texture, parent=camera.ui, scale=(2, 1))
        self.jumpscare_sound.play()
        invoke(self.jumpscare_sound.stop, delay=self.jumpscare_sound.length)
        invoke(self.death_screen, delay=self.jumpscare_sound.length)

    @staticmethod
    def death_screen():
        scene.clear()
        Entity(model="quad", parent=camera.ui, texture="assets/videos/catchcustomdeath.mov", scale=(2, 1))
        catch_jump_sound = Audio("sfx/monsters/catch/catchcustomdeath.wav", auto_destroy=True)
        print(
            "IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT. IT'S YOUR FAULT.")
        invoke(application.quit, delay=catch_jump_sound.length)
