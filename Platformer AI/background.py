import pygame
from imports import *
pygame.init()

class Background:
    WIDTH = BGIMG.get_width()
    def __init__(self):
        self.speed = 3
        self.y = 0
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self, screen):
        self.x1 -= self.speed
        self.x2 -= self.speed
        
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
        self.draw(screen)

    def draw(self, screen):
        screen.blit(BGIMG, (self.x1, self.y))
        screen.blit(BGIMG, (self.x2, self.y))