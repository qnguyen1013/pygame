import pygame
from sys import exit
from random import randint


def display_score():
    curr_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f"{curr_time}", False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return curr_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            if obstacle_rect.bottom == 300:
                obstacle_rect.x -= 5
                screen.blit(snail_surface, obstacle_rect)
            else:
                obstacle_rect.x -= 7
                screen.blit(fly_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


def player_animation():
    global player_surface, player_index
    # play walking animation when on floor
    # play jump animation when not on floor
    if player_rect.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]


pygame.init()

# takes in width, height
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf", 50)  # take font type and size
game_active = False
start_time = 0
score = 0

# surfaces: takes a width and height, if not an imported image
sky_surface = pygame.image.load(
    "graphics/Sky.png"
).convert()  # converts to image that pygame can run easier
ground_surface = pygame.image.load("graphics/ground.png").convert()

# text_surface = test_font.render("My game", False, "Black").convert()
# score_text_surface = test_font.render("Score", False, (64, 64, 64)).convert()
# score_text_rect = score_text_surface.get_rect(center=(400, 70))
outer_rect = pygame.Rect(400, 70, 110, 40)
outer_rect.center = (400, 67)

# Obstacles
obstacle_rect_list = []
snail_frame1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_frame2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snail_frames = [snail_frame1, snail_frame2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

fly_frame1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
fly_frame2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
fly_frames = [fly_frame1, fly_frame2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]


player_walk1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_walk2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
player_walk = [player_walk1, player_walk2]
player_index = 0
player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()
player_surface = player_walk[player_index]
# get_rect draws rectangle around image => can do this in one operation by making a class that combines both surf & rect
player_rect = player_surface.get_rect(midbottom=(80, 300))
player_gravity = 0

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

# keep screen open
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # set to the x on the display screen
            pygame.quit()
            exit()  # similar to a break but more secure

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player_rect.bottom == 300:
                        player_gravity = -22
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    player_rect.left = 80
                    game_active = not game_active
                    start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(
                        snail_surface.get_rect(midbottom=(randint(900, 1100), 300))
                    )
                else:
                    obstacle_rect_list.append(
                        fly_surface.get_rect(midbottom=(randint(900, 1100), 180))
                    )
            if event.type == snail_animation_timer:
                if snail_frame_index:
                    snail_frame_index = 0
                else:
                    snail_frame_index = 1
                snail_surface = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index:
                    fly_frame_index = 0
                else:
                    fly_frame_index = 1
                fly_surface = fly_frames[fly_frame_index]

    if game_active:
        # pygame draws images in the order in which they appear in
        screen.blit(ground_surface, (0, 300))
        screen.blit(sky_surface, (0, 0))  # 0,0 (origin) is in top left

        # pygame.draw.rect(screen, "#c0e8ec", score_text_rect)
        # pygame.draw.rect(screen, "#c0e8ec", outer_rect, border_radius=10)
        # screen.blit(score_text_surface, score_text_rect)

        score = display_score()

        # snail_rect.left -= 6  # could also use snail_rect.x
        # if snail_rect.right <= 0:
        #     snail_rect.left = 800
        # screen.blit(snail_surface, snail_rect)

        # PLAYER
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300

        screen.blit(player_surface, player_rect)
        player_animation()

        # OBSTACLE MOVEMENT
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # COLLISIONS
        # python auto converts 0 to false, but this is more readable imo
        game_active = collisions(player_rect, obstacle_rect_list)
    else:
        obstacle_rect_list.clear()
        screen.fill((94, 129, 162))
        player_rect.midbottom = (80, 300)
        player_gravity = 0
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
