# классы спрайтов

import pygame
from random import random

from config import all_sprites, tiles_group, evil_group, npc_group, \
    bullet_group, lose_group, stop_bullet_group
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
        self.image = evil_images['gop0']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.health = 5
        self.speed_counter = 0
        self.animation_counter = 1

    def damage(self, type_sprite):
        if type_sprite == 'bullet':
            self.health -= 1
        elif type_sprite == 'cop':
            self.health -= 2
            self.rect.x += tile_width * (1 - random())
        elif type_sprite == 'sotochka':
            self.rect.x += tile_width * (2 - random())
        elif type_sprite == 'sign':
            self.rect.x += tile_width * (3 - random())
        if self.health <= 0:
            self.kill()
            POINTS[0] += 2000
            MONEY[0] += 200
            print('[#] гопник убит')

    def update(self):
        if self.speed_counter == 3:
            self.speed_counter = 0
            self.rect.x -= 1
        else:
            self.speed_counter += 1

        self.image = evil_images[f'gop{self.animation_counter // 5}']
        self.animation_counter += 1
        if self.animation_counter // 5 == 8:
            self.animation_counter = 0


# класс попрошайки
class Beggar(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(evil_group, all_sprites)
        self.image = evil_images['beggar0']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.health = 3
        self.speed_counter = 0
        self.animation_counter = 1

    def damage(self, type_sprite):
        if type_sprite == 'bullet':
            self.health -= 1
        elif type_sprite == 'cop':
            self.health -= 2
            self.rect.x += tile_width * (1 - random())
        elif type_sprite == 'sotochka':
            self.rect.x += tile_width * (2 - random())
        elif type_sprite == 'sign':
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

        self.image = evil_images[f'beggar{self.animation_counter // 5}']
        self.animation_counter += 1
        if self.animation_counter // 5 == 8:
            self.animation_counter = 0


# класс пьяницы
class Drunk(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(evil_group, all_sprites)
        self.image = evil_images['drunk0']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.health = 10
        self.speed_counter = 0
        self.animation_counter = 1

    def damage(self, type_sprite):
        if type_sprite == 'bullet':
            self.health -= 1
        elif type_sprite == 'cop':
            self.health -= 2
            self.rect.x += tile_width * (1 - random())
        elif type_sprite == 'sotochka':
            self.rect.x += tile_width * (3 - random())
        elif type_sprite == 'sign':
            self.rect.x += tile_width * (2 - random())
        if self.health <= 0:
            self.kill()
            POINTS[0] += 3000
            MONEY[0] += 300
            print('[#] пьяница убит')

    def update(self):
        if self.speed_counter == 4:
            self.speed_counter = 0
            self.rect.x -= 1
        else:
            self.speed_counter += 1

        self.image = evil_images[f'drunk{self.animation_counter // 5}']
        self.animation_counter += 1
        if self.animation_counter // 5 == 8:
            self.animation_counter = 0


# класс министра
class Minister(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(evil_group, all_sprites)
        self.image = evil_images['minister']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def damage(self, type_sprite):
        pass

    def update(self):
        self.rect.x -= 1


# класс полицейского
class Cop(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(npc_group, all_sprites)
        self.image = npc_images['cop5']
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
        if self.speed_counter == 141:
            self.image = npc_images['cop6']
        elif self.speed_counter == 144:
            self.image = npc_images['cop7']
        elif self.speed_counter == 147:
            self.image = npc_images['cop0']
        elif self.speed_counter == 2:
            self.image = npc_images['cop2']
        elif self.speed_counter == 5:
            self.image = npc_images['cop3']
        elif self.speed_counter == 8:
            self.image = npc_images['cop4']
        elif self.speed_counter == 11:
            self.image = npc_images['cop5']
        if self.speed_counter == 150:
            self.speed_counter = 0
            self.image = npc_images['cop1']
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
            tile_width * pos_x + 30, tile_height * pos_y)

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


# класс линии проигрыша
class Lose(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(lose_group, all_sprites)
        self.image = tile_images['level3']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.x = pos_x
        self.y = pos_y


# класс недолёта пуль
class StopBullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(stop_bullet_group, all_sprites)
        self.image = tile_images['level3']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.x = pos_x
        self.y = pos_y
