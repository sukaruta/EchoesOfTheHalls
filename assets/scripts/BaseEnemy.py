from ursina import *
from prefabs.entity import cEntity


class BaseEnemy(cEntity):
    def __init__(self, **kwargs):
        self.direction = None

        super().__init__()
        self.speed = 5
        self.height = 2
        self.gravity = 1

        self.traverse_target = scene  # by default, it will collide with everything.
        self.ignore_list = [self]

        for key, value in kwargs.items():
            setattr(self, key, value)

        # make sure we don't fall through the ground if we start inside it
        if self.gravity:
            ray = raycast(self.world_position + (0, self.height, 0), self.down, traverse_target=self.traverse_target,
                          ignore=self.ignore_list)
            if ray.hit:
                self.y = ray.world_point.y

    def update(self):
        return

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

    def is_moving(self):
        if self.direction is None:
            return False
        elif self.direction.x + self.direction.y + self.direction.z != 0:
            return True
        return False
