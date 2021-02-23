import pygame
pygame.init()

BGIMG = pygame.transform.scale2x(pygame.image.load("Sprites\Background.jpg"))
PLATFORMIMG = pygame.image.load("Sprites\Platform.PNG")
PLATFORMIMG = pygame.transform.scale(PLATFORMIMG, (PLATFORMIMG.get_width() // 2, PLATFORMIMG.get_height() // 2))
PLAYERRUN1 = pygame.transform.scale2x(pygame.image.load("Sprites\\run1.png"))
PLAYERRUN2 = pygame.transform.scale2x(pygame.image.load("Sprites\\run2.png"))
PLAYERIMG = PLAYERRUN1