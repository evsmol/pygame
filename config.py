# определение главных переменных

import pygame


# константы
size = width, height = 450, 350  # размеры поля
screen = pygame.display.set_mode(size)  # экран
fps = 50  # частота обновления кадров
clock = pygame.time.Clock()  # обновление кадров
tile_width = tile_height = 50  # размеры клетки

# игровые переменные
LEVEL = [0]  # выбранный уровень
BOARD = [[0] * 9 for x in range(5)]  # NPC на поле
MONEY = [3000]  # валюта
POINTS = [0]  # очки
MUSIC = [False]  # музыка

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
evil_group = pygame.sprite.Group()
npc_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
lose_group = pygame.sprite.Group()
stop_bullet_group = pygame.sprite.Group()


# инициализация музыки
sound_start = ['data/start.mp3']
sound_characters = ['data/characters.mp3']
sound_main = ['data/main.mp3']
