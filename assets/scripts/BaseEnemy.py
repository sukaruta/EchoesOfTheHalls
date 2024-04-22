from ursina import *
from prefabs.entity import cEntity


class BaseEnemy(cEntity):
    def __init__(self, **kwargs):
        super().__init__()
        self.speed = 5
        self.gravity = 1

        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        direction_to_player = self.target.position - self.position
        direction_to_player.y = 0
        direction_to_player.normalize()
        self.position += direction_to_player * 0.02
        self.look_at_2d(self.target.position, 'y')
        vision = raycast((self.world_position.x, 0, self.world_position.z) + (self.up.x, self.target.height - 1.5, self.up.z), self.forward, distance=50,
                         traverse_target=self.target, debug=True)
        if vision.hit:
            print("Seen")
            print(vision.entity)
        collision_info = self.intersects(self.walls)
        if collision_info.hit:
            collision_normal = collision_info.normal.normalized()
            slide_direction = Vec3(collision_normal.x, 0, collision_normal.z)
            self.position += slide_direction * 0.03

    def is_moving(self):
        if self.direction is None:
            return False
        elif self.direction.x + self.direction.y + self.direction.z != 0:
            return True
        return False
