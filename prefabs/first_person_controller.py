from ursina import *


class FirstPersonController(Entity):
    def __init__(self, **kwargs):
        self.direction = None
        self.cursor = Entity(parent=camera.ui, model='quad', color=color.pink, scale=.008, rotation_z=45)
        self.stamina_bar = Entity(parent=camera.ui, model='quad', color=color.gray, scale=(4, .05, 0), x=-1, y=-.48)

        super().__init__()
        self.speed = 5
        self.height = 2
        self.sprinting = False
        self.crouching = False
        self.stamina = 95
        self.camera_pivot = Entity(parent=self, y=self.height)

        camera.parent = self.camera_pivot
        camera.position = (0, 0, 0)
        camera.rotation = (0, 0, 0)
        camera.fov = 90
        mouse.locked = True
        self.mouse_sensitivity = Vec2(40, 40)

        self.gravity = 1
        self.grounded = False
        self.jump_height = 2
        self.jump_up_duration = .5
        self.fall_after = .35  # will interrupt jump up
        self.jumping = False
        self.air_time = 0

        self.traverse_target = scene  # by default, it will collide with everything.
        self.ignore_list = [self, ]
        self.on_destroy = self.on_disable

        for key, value in kwargs.items():
            setattr(self, key, value)

        # make sure we don't fall through the ground if we start inside it
        if self.gravity:
            ray = raycast(self.world_position + (0, self.height, 0), self.down, traverse_target=self.traverse_target,
                          ignore=self.ignore_list)
            if ray.hit:
                self.y = ray.world_point.y

    def update(self):
        if (not self.sprinting or (self.is_moving() is False)) and self.stamina < 100:
            self.stamina += .2
        elif self.sprinting and (held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d']):
            if self.stamina > 0:
                self.stamina -= .2

            elif self.stamina <= 0:
                self.stamina = 0
                self.stop_sprint()

        self.stamina_bar.scale = (4 * self.stamina / 100, .05, 0)

        if self.camera_pivot.y > self.height:
            self.camera_pivot.y = self.height
        elif self.camera_pivot.y < 0:
            self.camera_pivot.y = 0

        self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]
        self.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
        self.camera_pivot.rotation_x = clamp(self.camera_pivot.rotation_x, -90, 90)

        self.direction = Vec3(
            self.forward * (held_keys['w'] - held_keys['s'])
            + self.right * (held_keys['d'] - held_keys['a'])
        ).normalized()

        feet_ray = raycast(self.position + Vec3(0, 0.5, 0), self.direction, traverse_target=self.traverse_target,
                           ignore=self.ignore_list, distance=.5, debug=False)
        head_ray = raycast(self.position + Vec3(0, self.height - .1, 0), self.direction,
                           traverse_target=self.traverse_target, ignore=self.ignore_list, distance=.5, debug=False)
        if not feet_ray.hit and not head_ray.hit:
            move_amount = self.direction * time.dt * self.speed

            if raycast(self.position + Vec3(-.0, 1, 0), Vec3(1, 0, 0), distance=.5,
                       traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[0] = min(move_amount[0], 0)
            if raycast(self.position + Vec3(-.0, 1, 0), Vec3(-1, 0, 0), distance=.5,
                       traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[0] = max(move_amount[0], 0)
            if raycast(self.position + Vec3(-.0, 1, 0), Vec3(0, 0, 1), distance=.5,
                       traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[2] = min(move_amount[2], 0)
            if raycast(self.position + Vec3(-.0, 1, 0), Vec3(0, 0, -1), distance=.5,
                       traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[2] = max(move_amount[2], 0)
            self.position += move_amount

            # self.position += self.direction * self.speed * time.dt

        if self.gravity:
            # gravity
            ray = raycast(self.world_position + (0, self.height, 0), self.down, traverse_target=self.traverse_target,
                          ignore=self.ignore_list)
            # ray = boxcast(self.world_position+(0,2,0), self.down, ignore=self.ignore_list)

            if ray.distance <= self.height + .1:
                if not self.grounded:
                    self.land()
                self.grounded = True
                # make sure it's not a wall and that the point is not too far up
                if ray.world_normal.y > .7 and ray.world_point.y - self.world_y < .5:  # walk up slope
                    self.y = ray.world_point[1]
                return
            else:
                self.grounded = False

            # if not on ground and not on way up in jump, fall
            self.y -= min(self.air_time, ray.distance - .05) * time.dt * 100
            self.air_time += time.dt * .25 * self.gravity

    def input(self, key):
        if key == 'space':
            self.jump()
        if key == 'left shift':
            self.sprint()
        if key == 'left shift up':
            self.stop_sprint()
        if key == 'left control':
            self.crouch()
        if key == "left control up":
            self.uncrouch()

    def jump(self):
        if not self.grounded:
            return

        self.stamina -= 5
        self.grounded = False
        self.animate_y(self.y + self.jump_height, self.jump_up_duration, resolution=int(1 // time.dt),
                       curve=curve.out_expo)
        invoke(self.start_fall, delay=self.fall_after)

    def crouch(self):
        if self.crouching:
            return
        self.crouching = True
        self.speed -= 1
        self.height = clamp(self.height / 2, 1, 2)
        self.camera_pivot.animate_y(self.camera_pivot.y / 2, .5, resolution=int(1 // time.dt), curve=curve.out_expo)

    def uncrouch(self):
        if not self.crouching:
            return
        self.crouching = False
        self.speed += 1
        self.height = clamp(self.height * 2, 1, 2)
        self.camera_pivot.animate_y(self.camera_pivot.y * 2, .5, resolution=int(1 // time.dt), curve=curve.out_expo)

    def sprint(self):
        if self.sprinting:
            return
        if self.stamina <= 0:
            return
        self.sprinting = True
        self.speed *= 2

    def stop_sprint(self):
        if not self.sprinting:
            return
        self.sprinting = False
        self.speed /= 2

    def start_fall(self):
        self.y_animator.pause()
        self.jumping = False

    def land(self):
        # print('land')
        self.air_time = 0
        self.grounded = True

    def on_enable(self):
        mouse.locked = True
        self.cursor.enabled = True

    def on_disable(self):
        mouse.locked = False
        self.cursor.enabled = False

    def is_moving(self):
        if self.direction is None:
            return False
        elif self.direction.x + self.direction.y + self.direction.z != 0:
            return True
        return False
