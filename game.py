import pygame
from sys import exit

pygame.init()

# takes in width, height
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")

# keep screen open
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # set to the x on the window screen
            pygame.quit()
            exit()  # similar to a break but more secure

    # draw all our elements and update everything
    # update everything
    pygame.display.update()
