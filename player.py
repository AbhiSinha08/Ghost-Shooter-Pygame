if __name__ == '__main__':
    print("Run the game.py script to run the game.")
    exit()

from time import time
import pygame as game

class Player:
    def __init__(self, model, spawn):
        self.still = game.image.load(f"{model} still.png")
        self.up = game.image.load(f"{model} up.png")
        self.upmove = game.image.load(f"{model} upmove.png")
        self.walk = game.image.load(f"{model} walk.png")
        self.current = self.still
        self.bullet = game.image.load('graphics/bullet.png')
        self.bullet = game.transform.scale(self.bullet, (25,25)) 
        self.ground = spawn[1]
        self.position = spawn
        self.health = 5
        self.walkTimer = time()
        self.dirR = True
        self.activeBullets = []

    def flip(self):
        self.still = game.transform.flip(self.still, True, False)
        self.up = game.transform.flip(self.up, True, False)
        self.upmove = game.transform.flip(self.upmove, True, False)
        self.walk = game.transform.flip(self.walk, True, False)
        self.bullet = game.transform.flip(self.bullet, True, False)
        self.dirR = not self.dirR

    def toggleWalk(self, current):
        if current == self.still:
            self.position[1] -= 4
            return self.walk
        self.position[1] += 4
        return self.still

    def gravity(self):
        if self.position[1] >= self.ground:
            self.position[1] = self.ground
        else:
            self.position[1] += 4

    def moveHorizontal(self, pixels):
        if (pixels > 0 and self.dirR == False) or (pixels < 0 and self.dirR == True):
            self.flip()
        self.position[0] += pixels
        if self.position[0] < -25:
            self.position[0] = -25
        elif self.position[0] > 1165:
            self.position[0] = 1165
        if pixels:
            if self.position[1] < self.ground - 10:
                self.current = self.upmove
                return None
            if time() > self.walkTimer + 0.15:
                self.current = self.toggleWalk(self.current)
                self.walkTimer = time()
        else:
            self.current =self.still

    def moveVertical(self, pixels):
        self.position[1] += pixels
        if self.position[1] < -125:
            self.position[1] = -125
        if pixels:
            self.current = self.up
        self.gravity()
        
    def fire(self):
        if self.dirR:
            self.activeBullets.append([self.dirR, [self.position[0] + 100, self.position[1] + 73], self.bullet])
        else:
            self.activeBullets.append([self.dirR, [self.position[0] +5, self.position[1] + 73], self.bullet])

    def bulletMove(self):
        for bullet in self.activeBullets:
            if bullet[0]:
                bullet[1][0] += 15
            else:
                bullet[1][0] -= 15
            if bullet[1][0] > 1280:
                self.activeBullets.remove(bullet)
