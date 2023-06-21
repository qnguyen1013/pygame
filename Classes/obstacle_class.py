import pygame
from random import randint, choice


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type
        if self.type == "fly":
            fly_frame1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
            fly_frame2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
            self.frames = [fly_frame1, fly_frame2]
            y_pos = 200

        if self.type == "snail":
            snail_frame1 = pygame.image.load(
                "graphics/snail/snail1.png"
            ).convert_alpha()

            snail_frame2 = pygame.image.load(
                "graphics/snail/snail2.png"
            ).convert_alpha()

            self.frames = [snail_frame1, snail_frame2]
            y_pos = 300 

        self.animation_index = 0 
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        if self.type == "snail":
            self.animation_index += 0.1
        if self.type == "fly":
            self.animation_index += 0.25
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
