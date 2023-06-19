import pygame
from sys import exit
from random import randint, choice


# Classes
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


# Helper Functions
def display_score():
    curr_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f"{curr_time}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return curr_time


def collision_sprite():
    # sprite collide returns list
    if pygame.sprite.spritecollide(player.sprite, obstacles, False):
        obstacles.empty()
        return False
    else:
        return True


# Initialize Game
pygame.init()
# takes in width, height
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf", 50)  # take font type and size
game_active = False
start_time = 0
score = 0
ingame_music = pygame.mixer.Sound("audio/music.wav")
ingame_music.set_volume(0.5)


# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacles = pygame.sprite.Group()


# Dispaly Surfaces:
sky_surface = pygame.image.load(
    "graphics/Sky.png"
).convert()  # converts to image that pygame can run easier
ground_surface = pygame.image.load("graphics/ground.png").convert()


# Intro Screen
player_stand = pygame.image.load("graphics/Player/player_stand.png")
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(300, 200))

game_title_surface = test_font.render("Pixel Runner", False, (64, 64, 64))
game_title_rect = game_title_surface.get_rect(center=(400, 75))
instruction_surf = test_font.render('Press "r" to run', False, (64, 64, 64))
instruction_rect = instruction_surf.get_rect(midleft=(400, 220))


# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

# keep screen open/play game
while True:
    ingame_music.play(-1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # set to the x on the display screen
            pygame.quit()
            exit()  # similar to a break but more secure

        if not game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # player_rect.left = 80
                    game_active = not game_active
                    start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:
            if event.type == obstacle_timer:
                obstacles.add(Obstacle(choice(["fly", "snail", "snail", "snail"])))

    if game_active:
        # pygame draws images in the order in which they appear in
        screen.blit(ground_surface, (0, 300))
        screen.blit(sky_surface, (0, 0))  # 0,0 (origin) is in top left

        score = display_score()

        # PLAYER
        player.draw(screen)
        player.update()

        # OBSTACLES
        obstacles.draw(screen)
        obstacles.update()

        # COLLISIONS
        game_active = collision_sprite()

    # Game Ends
    else:
        player.sprite.restart()
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(game_title_surface, game_title_rect)
        end_score_surf = test_font.render(f"Score: {score}", False, (64, 64, 64))
        end_score_rect = end_score_surf.get_rect(midleft=(400, 180))
        if score == 0:
            instruction_rect.midleft = 400, 200
            screen.blit(instruction_surf, instruction_rect)
        else:
            instruction_rect.midleft = 400, 220
            screen.blit(end_score_surf, end_score_rect)
            screen.blit(instruction_surf, instruction_rect)
        pygame.display.flip()

    pygame.display.update()  # updates the display

    # this while true loop should not run faster than 60 times per second (control frame rate) = ceiling
    clock.tick(60)
