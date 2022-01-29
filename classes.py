# классы спрайтов

import pygame
from random import random

from config import all_sprites, tiles_group, evil_group, npc_group, \
    bullet_group
from images import tile_images, npc_images, evil_images
from config import tile_width, tile_height, POINTS, MONEY, BOARD


# класс игрового поля
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


# класс гопника
class Gop(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(evil_group, all_sprites)
        self.image = evil_images['gop']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.health = 5
        self.speed_counter = 0

    def damage(self, type_sprite):
        if type_sprite == 'bullet':
            self.health -= 1
        elif type_sprite == 'cop':
            self.health -= 2
            self.rect.x += tile_width * (1 - random())
        elif type_sprite == 'sotochka':
            self.rect.x += tile_width * (2 - random())
        elif type_sprite == 'sign':
            self.health -= 1
            self.rect.x += tile_width * (3 - random())
        if self.health <= 0:
            self.kill()
            POINTS[0] += 1000
            MONEY[0] += 200
            print('[#] гопник убит')

    def update(self):
        if self.speed_counter == 3:
            self.speed_counter = 0
            self.rect.x -= 1
        else:
            self.speed_counter += 1


# класс попрошайки
class Beggar(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(evil_group, all_sprites)
        self.image = evil_images['beggar']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.health = 3
        self.speed_counter = 0

    def damage(self, type_sprite):
        if type_sprite == 'bullet':
            self.health -= 1
        elif type_sprite == 'cop':
            self.health -= 2
            self.rect.x += tile_width * (1 - random())
        elif type_sprite == 'sotochka':
            self.rect.x += tile_width * (2 - random())
        elif type_sprite == 'sign':
            self.health -= 1
            self.rect.x += tile_width * (3 - random())
        if self.health <= 0:
            self.kill()
            POINTS[0] += 1000
            MONEY[0] += 100
            print('[#] попрошайка убит')

    def update(self):
        if self.speed_counter == 1:
            self.speed_counter = 0
            self.rect.x -= 1
        else:
            self.speed_counter += 1


# класс пьяницы
class Drunk(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(evil_group, all_sprites)
        self.image = evil_images['drunk']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.health = 10
        self.speed_counter = 0

    def damage(self, type_sprite):
        if type_sprite == 'bullet':
            self.health -= 1
        elif type_sprite == 'cop':
            self.health -= 2
            self.rect.x += tile_width * (1 - random())
        elif type_sprite == 'sotochka':
            self.rect.x += tile_width * (3 - random())
        elif type_sprite == 'sign':
            self.health -= 1
            self.rect.x += tile_width * (2 - random())
        if self.health <= 0:
            self.kill()
            POINTS[0] += 1000
            MONEY[0] += 300
            print('[#] пьяница убит')

    def update(self):
        if self.speed_counter == 4:
            self.speed_counter = 0
            self.rect.x -= 1
        else:
            self.speed_counter += 1


# класс полицейского
class Cop(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(npc_group, all_sprites)
        self.image = npc_images['cop']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.x = pos_x
        self.y = pos_y
        self.health = 3
        self.speed_counter = 100

    def damage(self):
        self.health -= 1
        if self.health == 0:
            self.kill()
            BOARD[self.y - 2][self.x] = 0
            print('[#] полицейский убит')

    def get_name(self):
        return 'cop'

    def update(self):
        if self.speed_counter == 150:
            self.speed_counter = 0
            Bullet(self.x, self.y)
        else:
            self.speed_counter += 1


# класс пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(bullet_group, all_sprites)
        self.image = npc_images['bullet']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 28, tile_height * pos_y)

    def update(self):
        self.rect.x += 5


# класс соточки
class Sotochka(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(npc_group, all_sprites)
        self.image = npc_images['sotochka']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.x = pos_x
        self.y = pos_y

    def damage(self):
        self.kill()
        print(self.x,  self.y)
        BOARD[self.y - 2][self.x] = 0
        print('[#] соточку забрали')

    def get_name(self):
        return 'sotochka'


# класс ремонта дорог
class Sign(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(npc_group, all_sprites)
        self.image = npc_images['sign']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.x = pos_x
        self.y = pos_y
        self.health = 7

    def damage(self):
        self.health -= 1
        if self.health == 0:
            self.kill()
            BOARD[self.y - 2][self.x] = 0
            print('[#] дорогу починили')

    def get_name(self):
        return 'sign'
