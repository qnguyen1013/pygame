import pygame
from sys import exit

pygame.init()

# takes in width, height
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf", 50)  # take font type and size

# surfaces: takes a width and height, if not an imported image
sky_surface = pygame.image.load(
    "graphics/Sky.png"
).convert()  # converts to image that pygame can run easier
ground_surface = pygame.image.load("graphics/ground.png").convert()

# text_surface = test_font.render("My game", False, "Black").convert()
score_text_surface = test_font.render("Score", False, "Black").convert()
score_text_rect = score_text_surface.get_rect(center=(400, 70))
outer_rect = pygame.Rect(400, 70, 110, 40)
outer_rect.center = (400, 67)


snail_surface = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_rect = snail_surface.get_rect(midbottom=(600, 300))

player_surface = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
# get_rect draws rectangle around image => can do this in one operation by making a class that combines both surf & rect
player_rect = player_surface.get_rect(midbottom=(80, 300))

# keep screen open
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # set to the x on the display screen
            pygame.quit()
            exit()  # similar to a break but more secure
        # if event.type == pygame.MOUSEMOTION:
        # if player_rect.collidepoint(event.pos):
        #     print("collides")

    # pygame draws images in the order in which they appear in
    screen.blit(ground_surface, (0, 300))
    screen.blit(sky_surface, (0, 0))  # 0,0 (origin) is in top left
    # screen.blit(text_surface, (350, 20))
    # pygame.draw.rect(screen, "Pink", score_text_rect)
    # pygame.draw.rect(screen, "Pink", score_text_rect)
    pygame.draw.rect(screen, "Pink", score_text_rect)
    pygame.draw.rect(screen, "Pink", outer_rect, border_radius=10)
    # pygame.draw.rect(screen, "Pink", outer_rect, 10)
    screen.blit(score_text_surface, score_text_rect)

    snail_rect.left -= 2  # could also use snail_rect.x
    if snail_rect.right <= 0:
        snail_rect.left = 800
    screen.blit(snail_surface, snail_rect)

    screen.blit(player_surface, player_rect)

    # python auto converts 0 to false, but this is more readable imo
    if player_rect.colliderect(snail_rect) == 1:
        print("collision")

    pygame.display.update()  # updates the display

    # this while true loop should not run faster than 60 times per second (control frame rate) = ceiling
    clock.tick(60)
