import pygame
from sys import exit
from random import randint, choice
from Classes.player_class import Player
from Classes.obstacle_class import Obstacle

import cv2
from pynput.keyboard import Key, Controller
from cvzone.HandTrackingModule import HandDetector


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
test_font1 = pygame.font.Font("font/Pixeltype.ttf", 30)  # take font type and size
game_active = False
start_time = 0
score = 0
ingame_music = pygame.mixer.Sound("audio/music.wav")
ingame_music.set_volume(0.2)


# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacles = pygame.sprite.Group()


# Display Surfaces:
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
instruction_surf = test_font1.render('Press "r" to run', False, (64, 64, 64))
instruction_surf1 = test_font1.render(
    "Pinch index and thumb fingers to jump", False, (64, 64, 64)
)
instruction_rect = instruction_surf.get_rect(midleft=(400, 220))
instruction_rect1 = instruction_surf1.get_rect(midleft=(400, 250))


# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 2600)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

# Computer Vision variables
keyboard = Controller()
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=1)
# keep screen open/play game
while True:
    # CV
    ret, frame = cap.read()
    height, width, layers = frame.shape

    frame = cv2.resize(frame, (width // 2, height // 2))
    hands, image = detector.findHands(frame)

    cv2.imshow("Frame", frame)

    ingame_music.play(-1)

    for event in pygame.event.get():
        # camera exits when game exits
        if event.type == pygame.QUIT:  # set to the x on the display screen
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            exit()  # similar to a break but more secure

        # can quit game with q key press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                cap.release()
                cv2.destroyAllWindows()
                pygame.quit()
                exit()

        if hands:
            lmList = hands[0]

            lmList2 = lmList["lmList"]

            length, info, image = detector.findDistance(
                [lmList2[4][0], lmList2[4][1]], [lmList2[8][0], lmList2[8][1]], image
            )

            if length <= 17:
                keyboard.press(Key.space)
            else:
                keyboard.release(Key.space)

        # restarts game
        if not game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_active = not game_active
                    start_time = int(pygame.time.get_ticks() / 1000)

        # adds enemies/obstacles
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
            screen.blit(instruction_surf1, instruction_rect1)
        else:
            instruction_rect.midleft = 400, 220
            screen.blit(end_score_surf, end_score_rect)
            screen.blit(instruction_surf, instruction_rect)
            screen.blit(instruction_surf1, instruction_rect1)

        pygame.display.flip()

    pygame.display.update()  # updates the display

    # this while true loop should not run faster than 60 times per second (control frame rate) = ceiling
    clock.tick(60)
