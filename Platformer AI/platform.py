import pygame, random
from imports import *
pygame.init()

class Platform:
    PLATFORMHEIGHTS = [700, 600, 500]
    def __init__(self):
        self.speed = 3
        self.x = 1000
        self.y = self.PLATFORMHEIGHTS[random.randint(0,2)]

    def drawPlatforms(self, screen):
        screen.blit(PLATFORMIMG, (self.x, self.y))

    def movePlatform(self, screen):
        self.x -= self.speed
        self.drawPlatforms(screen)


class StartPlatform:
    def __init__(self, form):
        self.speed = 3
        self.x = 1 * (form * (PLATFORMIMG.get_width() - 100))
        self.y = 600

    def drawPlatforms(self, screen):
        screen.blit(PLATFORMIMG, (self.x, self.y))

    def movePlatform(self, screen):
        self.x -= self.speed
        self.drawPlatforms(screen)


def update(platforms, screen, startPlatforms):
    for p in platforms:
        p.movePlatform(screen)
    for p in startPlatforms:
        p.movePlatform(screen)
    if len(platforms) >= 15:
        platforms.pop(0)
        startPlatforms.clear()
    return platforms, startPlatforms

