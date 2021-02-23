import pygame
from imports import *
pygame.init()

RUN = [PLAYERRUN1, PLAYERRUN2]

class Player:
    def __init__(self):
        self.speed = 3
        self.fallSpeed = 4
        self.jumpHeight = 300
        self.x = 100
        self.y = 600 - PLAYERIMG.get_height() - 20
        self.limit = self.y - self.jumpHeight
        self.playerimg = RUN[0]
        self.rect = RUN[0].get_rect(topleft=(self.x, self.y))

    def update(self):
        if self.playerimg == RUN[0]:
            self.playerimg = RUN[1]
        elif self.playerimg == RUN[1]:
            self.playerimg = RUN[0]

    def getRect(self):
        self.rect.y = self.y
        return self.rect

    def keyControl(self, event, isJump, jumping):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and jumping == False:
                isJump = True
                jumping = True
                self.limit = self.y - self.jumpHeight
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                isJump = False
        return isJump, self.limit, jumping

    def jump(self, isJump, top, i):
        if isJump[i]:
            if top[i] == False:
                self.y -= 9

    def fall(self):
        self.y += self.fallSpeed

    def draw(self, screen):
        screen.blit(self.playerimg, self.rect)