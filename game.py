try:
    import pygame as game
except:
    print("PyGame module not found.\nUse 'pip install pygame' command to install")
    exit()
import os
from player import Player
from configparser import ConfigParser as cfg
os.chdir(__file__.replace(os.path.basename(__file__), ''))

game.init()
game.font.init()
font = game.font.SysFont('Comic Sans MS', 86)
size = (1280, 720)
icon = game.image.load('icon.png')
window = game.display.set_mode(size)
# game.display.toggle_fullscreen()
game.display.set_caption('Ghost Shooters')
game.display.set_icon(icon)
background = game.image.load('graphics/menu.jpg')
background = game.transform.scale(background, size)
selector = game.image.load('graphics/selector.png')
selector = game.transform.scale(selector, (128,72))
window.blit(background, (0,0))
window.blit(selector, (100, 165))
game.display.flip()

def menu():
    newGame = True
    while True:
        game.time.delay(16)
        for event in game.event.get():
            if event.type == game.QUIT:
                exit()
            if event.type == game.KEYUP:
                if event.key == game.K_UP:
                    newGame = True
                    window.blit(background, (0,0))
                    window.blit(selector, (100, 165))
                elif event.key == game.K_DOWN:
                    newGame = False
                    window.blit(background, (0,0))
                    window.blit(selector, (100, 465))
                elif event.key == game.K_RETURN or event.key == game.K_KP_ENTER or event.key == game.K_SPACE:
                    return newGame
            game.display.flip()

def charSel():
    avatar = 'graphics/guy'
    while True:
        game.time.delay(16)
        for event in game.event.get():
            if event.type == game.QUIT:
                exit()
            if event.type == game.KEYUP:
                if event.key == game.K_LEFT:
                    avatar = 'graphics/guy'
                    window.fill((204, 229, 255))
                    window.blit(avatar1, (256, 120))
                    window.blit(avatar2, (768, 120))
                    window.blit(selector, (80, 320))
                elif event.key == game.K_RIGHT:
                    avatar = 'graphics/girl'
                    window.fill((204, 229, 255))
                    window.blit(avatar1, (256, 120))
                    window.blit(avatar2, (768, 120))
                    window.blit(selector, (610, 320))
                elif event.key == game.K_RETURN or event.key == game.K_KP_ENTER or event.key == game.K_SPACE:
                    return avatar
            game.display.flip()

def loadLevel(n):
        global level
        if n == 1:
            import levels.level1 as level
        elif n == 2:
            import levels.level2 as level
        elif n == 3:
            import levels.level3 as level
        else:
            gameOver('Successfully Completed Game', 'More Levels to Come Soon!')

newGame = menu()
del background
data = cfg()
data.read('gamedata.ini')

if newGame:
    avatar1 = game.image.load('graphics/guy.png')
    avatar2 = game.image.load('graphics/girl.png')
    window.fill((204, 229, 255))
    window.blit(avatar1, (256, 120))
    window.blit(avatar2, (768, 120))
    window.blit(selector, (80, 320))
    game.display.flip()
    avatar = charSel()
    data.set('saved', 'player', avatar)
    data.set('saved', 'level', '1')
    with open('gamedata.ini', 'w') as save:
        data.write(save)
    del avatar, avatar1, avatar2
del selector

def gameOver(text, text2 = ''):
    overText = font.render(text, False, (0,0,0))
    window.blit(overText, (80, 40))
    if text2:
        overText2 = font.render(text2, False, (100,100,100))
        overText2 = game.transform.scale(overText2, (600, 50))
        window.blit(overText2, (80, 100))
    game.display.flip()
    if text2:
        data.set('saved', 'level', '1')
    else:
        data.set('saved', 'level', str(curLev))
    with open('gamedata.ini', 'w') as save:
        data.write(save)
    while True:
        game.time.delay(100)
        for event in game.event.get():
            if event.type == game.QUIT:
                exit()
            if event.type == game.KEYDOWN:
                exit()

def playerMov(x, y): 
    player.moveHorizontal(x)
    player.moveVertical(y)
    player.bulletMove()
    for bullet in player.activeBullets:
        window.blit(bullet[2], bullet[1])
    window.blit(player.current, player.position)

def enemyMove(active):
    for enemy in active:
        enemy[1][0] += enemy[2]
        window.blit(enemy[0], enemy[1])
        if enemy[1][0] < player.position[0] + 100 and enemy[1][0] > player.position[0] and enemy[1][1] > player.position[1] - 50 and enemy[1][1] < player.position[1] + 180:
            gameOver('GAME OVER!')
        if enemy[1][0] < -20:
            active.remove(enemy)
        for bullet in player.activeBullets:
            if bullet[1][0] > enemy[1][0] + 10 and bullet[1][0] < enemy[1][0] + 70 and bullet[1][1] > enemy[1][1] and bullet[1][1] < enemy[1][1] + 80:
                active.remove(enemy)
                level.enemy_count -= 1
                player.activeBullets.remove(bullet)
                break

obj = font.render("Don't Let the Ghosts come near", False, (0,0,0))
obj = game.transform.scale(obj,(300, 25))

while True:
    curLev = int(data.get('saved', 'level'))
    lv = font.render(f"LEVEL {curLev}", False, (0,0,0))
    lv = game.transform.scale(lv, (70, 25))
    loadLevel(curLev)
    player = Player(data.get('saved', 'player'), level.spawn)
    speedX, speedY = 0, 0

    while level.enemy_count:
        game.time.delay(16)
        for event in game.event.get():
            if event.type == game.QUIT:
                exit()
            if event.type == game.KEYDOWN:
                if event.key == game.K_RIGHT:
                    speedX = 5
                elif event.key == game.K_LEFT:
                    speedX = -5
                elif event.key == game.K_UP:
                    speedY = -10
                elif event.key == game.K_SPACE:
                    player.fire()
            if event.type == game.KEYUP:
                if event.key == game.K_RIGHT or event.key == game.K_LEFT:
                    speedX = 0
                if event.key == game.K_UP:
                    speedY = 0
        level.enemySpawn()
        window.blit(level.bg, (0,0))
        window.blit(obj, (10, 10))
        window.blit(lv, (1200, 10))
        enemyMove(level.active)
        playerMov(speedX, speedY)
        game.display.flip()
    
    del player
    del level
    data.set('saved', 'level', (str)(curLev + 1))
    with open('gamedata.ini', 'w') as save:
        data.write(save)
