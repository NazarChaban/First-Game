import os
import pygame as p
from pygame.constants import QUIT, K_w, K_a, K_s, K_d, K_LSHIFT
import random as r

p.init()

#КОНСТАНТИ
HEIGHT = 700
WIDTH = 1200
FPS = p.time.Clock()
FONT = p.font.SysFont('Verdana', 20)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

bg = p.transform.scale(p.image.load(r'C:/Users/Admin/VS code/GoITGame/background.png'), (WIDTH, HEIGHT))
bg_x1 = 0
bg_x2 = bg.get_width()
bg_move = 3

main_display = p.display.set_mode((WIDTH, HEIGHT))

#ГРАВЕЦЬ
IMAGE_PATH = r'C:/Users/Admin/VS code/GoITGame/Goose'
PLAYER_IMAGES = os.listdir(IMAGE_PATH)
player_size = (182, 115)
player = p.image.load(r'C:/Users/Admin/VS code/GoITGame/player.png').convert_alpha()
player_rect = p.Rect((0, int((HEIGHT-player_size[1])/2), *player_size))
player_move_up = [0, -4]
player_move_up2 = [0, -6]
player_move_left = [-4, 0]
player_move_left2 = [-6, 0]
player_move_down = [0, 4]
player_move_down2 = [0, 6]
player_move_right = [4, 0]
player_move_right2 = [6, 0]
CHANGE_IMAGES = p.USEREVENT + 3
p.time.set_timer(CHANGE_IMAGES, 200)


#ВОРОГИ
def create_enemy():
    enemy_size = (120, 50)
    enemy = p.transform.scale(p.image.load(r'C:/Users/Admin/VS code/GoITGame/enemy.png').convert_alpha(), (enemy_size))
    enemy_rect = p.Rect((WIDTH, r.randint(0, HEIGHT-enemy_size[1]), *enemy_size))
    enemy_move = [r.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]
CREATE_ENEMY = p.USEREVENT + 1
p.time.set_timer(CREATE_ENEMY, 1000)
enemies = []

#БОНУСИ
def create_bonus():
    bonus_size = (80, 120)
    bonus = p.transform.scale(p.image.load(r'C:/Users/Admin/VS code/GoITGame/bonus.png').convert_alpha(), (bonus_size))
    bonus_rect = p.Rect((r.randint(-bonus_size[1], int(WIDTH-bonus_size[0])), 0, *bonus_size))
    bonus_move = [0, r.randint(4, 7)]
    return [bonus, bonus_rect, bonus_move]
CREATE_BONUS = p.USEREVENT + 2
p.time.set_timer(CREATE_BONUS, 3000)
bonuses = []

score = 0
game_over = 'GAME OVER'
image_index = 0
#ГРА
playing = True
while playing:

    FPS.tick(60)

    #ФОН
    bg_x1 -= bg_move
    bg_x2 -= bg_move

    if bg_x1 < -bg.get_width():
        bg_x1 = bg.get_width()

    if bg_x2 < -bg.get_width():
        bg_x2 = bg.get_width()

    main_display.blit(bg, (bg_x1,0))
    main_display.blit(bg, (bg_x2,0))
    
    #ІВЕНТИ
    for event in p.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGES:
            player = p.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0
    
    #ГРАВЕЦЬ
    keys = p.key.get_pressed()

    if keys[K_w] and player_rect.top >= 0:
        if keys[K_LSHIFT]:
            player_rect = player_rect.move(player_move_up2)
        else:
            player_rect = player_rect.move(player_move_up)

    if keys[K_a] and player_rect.left >= 0:
        if keys[K_LSHIFT]:
            player_rect = player_rect.move(player_move_left2)
        else:
            player_rect = player_rect.move(player_move_left)

    if keys[K_s] and player_rect.bottom <= HEIGHT:
        if keys[K_LSHIFT]:
            player_rect = player_rect.move(player_move_down2)
        else:
            player_rect = player_rect.move(player_move_down)

    if keys[K_d] and player_rect.right <= WIDTH:
        if keys[K_LSHIFT]:
            player_rect = player_rect.move(player_move_right2)
        else:
            player_rect = player_rect.move(player_move_right)

    main_display.blit(player, player_rect)

    #ВОРОГИ
    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            playing = False

    for enemy in enemies:
        if enemy[1].right < 0:
            enemies.pop(enemies.index(enemy))
    
    #БОНУСИ
    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            score += 1


    for bonus in bonuses:
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))

    #БАЛИ
    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH-50, 20))

s    p.display.flip()