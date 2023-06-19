import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load(
            "graphics/Player/player_walk_1.png"
        ).convert_alpha()
        player_walk2 = pygame.image.load(
            "graphics/Player/player_walk_2.png"
        ).convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()
        # self.player_surface = player_walk[player_index]
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(100, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity -= 22
            pygame.mixer.Channel(0).play(self.jump_sound)

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            self.gravity = 0

    def animation_state(self):
        # play walking animation when on floor
        # play jump animation when not on floor
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.animation_state()
        self.player_input()
        self.apply_gravity()

    def restart(self):
        self.rect.y = 300
