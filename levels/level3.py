if __name__ == '__main__':
    exit()

import pygame as game
from random import randint

spawn = [30, 500]
bg = game.image.load('levels/bg1.jpg')
enemy_intensity = 3
enemy_count = 50
enemy_speed = 6
enemy = []
active = []
enemy.append(game.image.load('graphics/enemy1.png')) # Icon made by "https://www.flaticon.com/authors/smashicons"
enemy.append(game.image.load('graphics/enemy2.png'))
enemy.append(game.image.load('graphics/enemy3.png'))
enemy.append(game.image.load('graphics/enemy4.png'))
for i in range(0, len(enemy)):
    enemy[i] = game.transform.scale(enemy[i], (80,80))

def enemySpawn():
    if randint(0,100) < enemy_intensity:
        e = randint(0, len(enemy)-1)
        active.append([enemy[e], [1280, randint(30,600)], -enemy_speed])