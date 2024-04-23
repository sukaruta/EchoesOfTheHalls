from prefabs.entity import cEntity
from ursina import *
import os


class SoulOrb(cEntity):
    def __init__(self, **kwargs):
        super().__init__()

        for key, value in kwargs.items():
            setattr(self, key, value)
        self.collection_text = Text(text="Collected soul orb", x=-0.1, y=-0.3, font=self.font)
        self.collection_text.fade_out(duration=0)

    def update(self):
        self.rotation_y += 1

        collision_info = self.intersects(self.player)
        if collision_info.hit:
            self.player.collected_souls += 1
            self.collection_text.enable()
            self.collection_text.fade_in(1, duration=0.5)
            invoke(self.collection_text.fade_out, delay=5)
            self.disable()
