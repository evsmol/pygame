import os
import sys

import pygame


pygame.init()
print('[!] инициализация pygame')
pygame.display.set_caption('УРАЛМАШ')
pygame.display.set_icon(pygame.image.load("data/icon.png"))
size = width, height = 450, 350  # размеры поля
screen = pygame.display.set_mode(size)
FPS = 40
tile_width = tile_height = 50  # размеры клетки
level = 0  # выбранный уровень
music = True  # состояние музыки

# музыка
# sound_start = pg.mixer.Sound('data/start.mp3')
# sound_start.set_volume(0.2)
# sound_main = pg.mixer.Sound('data/main.mp3')
# sound_main.set_volume(0.2)


# выход из программы
def terminate():
    print("[!] выход из программы")
    pygame.quit()
    sys.exit()


# загрузка изображения
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"[!] файл с изображением '{fullname}' не найден")
        print("[!] выход из программы")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    print(f'[#] загрузка изображения {name}')
    return image


# возвращает координаты клетки в виде кортежа
def get_cell(mouse_pos):
    if 0 <= mouse_pos[0] <= tile_width * 9:
        if tile_width * 2 <= mouse_pos[1] <= tile_width * 7:
            return (mouse_pos[0] - 0) // tile_width, \
                   (mouse_pos[1] - tile_height * 2) // tile_height
    return None


# стартовое окно
def start_screen():
    global level
    print("[!] открытие стартового окна")
    intro_text = ["Добро пожаловать на УРАЛМАШ", "",
                  "Выбрать уровень — «1», «2», «3»",
                  "Посмотреть управление — «F1»",
                  "Посмотреть статистику — «F2»", "",
                  "Приятной игры!"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    start_font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = start_font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    # sound_start.play()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    level = 1
                    print('[!] выбран 1 уровень')
                elif event.key == pygame.K_2:
                    level = 2
                    print('[!] выбран 2 уровень')
                elif event.key == pygame.K_3:
                    level = 3
                    print('[!] выбран 3 уровень')
                elif event.key == pygame.K_F1:
                    guide_screen()
            if level:
                # sound_start.stop()
                # sound_main.play()
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


# окно управления
def guide_screen():
    print("[!] открытие окна управления")
    intro_text = ["УПРАВЛЕНИЕ", "",
                  "Выбор NPC — «1», «2», «3»",
                  "Поставить NPC — «ЛКМ»",
                  "Выкл/вкл музыку — «ПРОБЕЛ»",
                  "Вернуться назад — «ESC»"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    start_font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = start_font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    start_screen()
        pygame.display.flip()
        clock.tick(FPS)


tile_images = {
    'level1': load_image('stonecutter.png'),
    'level2': load_image('piston.png'),
    'level3': load_image('netherite.png')
}

npc_images = {
    'cop': load_image('cop.png'),
    'sotochka': load_image('sotochka.png'),
    'sign': load_image('sign.png'),
    'bullet': load_image('bullet.png')
}

evil_images = {
    'gop': load_image('gop.png'),
    'beggar': load_image('beggar.png'),
    'drunk': load_image('drunk.png')
}


# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
evil_group = pygame.sprite.Group()
npc_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()


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

    def damage(self):
        self.health -= 1
        if self.health == 0:
            self.kill()

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
        self.health = 5
        self.speed_counter = 0

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
        self.health = 5
        self.speed_counter = 0

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
        self.health = 5
        self.speed_counter = 100

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
        self.health = 5


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
        self.health = 5


def generate_level():
    print('[#] генерация уровня')
    for y in range(5):
        for x in range(9):
            if level == 1:
                Tile('level1', x, y + 2)
            elif level == 2:
                Tile('level2', x, y + 2)
            elif level == 3:
                Tile('level3', x, y + 2)
    return 9, 5


Gop(9, 5)
Gop(10, 5)
Gop(11, 5)
Gop(12, 5)
Gop(13, 5)
Gop(14, 5)
Gop(15, 5)
Gop(16, 5)
Gop(17, 5)
Gop(18, 5)
Gop(19, 5)
Gop(20, 5)
Drunk(10, 4)
Gop(9, 3)
Beggar(11, 2)
Beggar(11, 6)

clock = pygame.time.Clock()
running = True
start_screen()  # открытие стартового окна

level_x, level_y = generate_level()  # генерация уровня

cache = 'cop'  # выбранный NPC
image_panel = ['data/cop_blur.png', 'data/sotochka.png', 'data/sign.png']
board = [[0] * 9 for x in range(5)]  # NPC на поле
font = pygame.font.Font(None, 20)
text_300 = font.render("300", True, [0, 0, 0])
text_100 = font.render("100", True, [0, 0, 0])
MONEY = 500
text_of_money = font.render("ВАЛЮТА:", True, [0, 0, 0])
POINTS = 0
text_of_points = font.render("ОЧКИ:", True, [0, 0, 0])
print('[!] начало игры')
while running:
    # отрисовка игровой панели
    screen.fill((128, 128, 128))
    screen.blit(pygame.image.load(image_panel[0]), (tile_width * 3, 10))
    screen.blit(pygame.image.load(image_panel[1]), (tile_width * 4, 10))
    screen.blit(pygame.image.load(image_panel[2]), (tile_width * 5, 10))
    screen.blit(text_300, (tile_width * 3 + 13, tile_height * 1 + 20))
    screen.blit(text_100, (tile_width * 4 + 13, tile_height * 1 + 20))
    screen.blit(text_300, (tile_width * 5 + 13, tile_height * 1 + 20))
    screen.blit(text_of_money, (tile_width * 1 - 5, tile_height * 0 + 35))
    text_money = font.render(str(MONEY), True, [0, 0, 0])
    screen.blit(text_money, (tile_width * 1 + 10, tile_height * 1 + 20))
    screen.blit(text_of_points, (tile_width * 7 + 3, tile_height * 0 + 35))
    text_points = font.render(str(POINTS // 10), True, [0, 0, 0])
    screen.blit(text_points, (tile_width * 7 + 5, tile_height * 1 + 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                print('[#] выбор `cop`')
                cache = 'cop'  # 1
                image_panel[0] = 'data/cop_blur.png'
                image_panel[1] = 'data/sotochka.png'
                image_panel[2] = 'data/sign.png'
            if event.key == pygame.K_2:
                print('[#] выбор `sotochka`')
                cache = 'sotochka'  # 2
                image_panel[0] = 'data/cop.png'
                image_panel[1] = 'data/sotochka_blur.png'
                image_panel[2] = 'data/sign.png'
            if event.key == pygame.K_3:
                print('[#] выбор `sign`')
                cache = 'sign'  # 3
                image_panel[0] = 'data/cop.png'
                image_panel[1] = 'data/sotochka.png'
                image_panel[2] = 'data/sign_blur.png'
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if get_cell(event.pos):
                    x, y = get_cell(event.pos)
                    if board[y][x] == 0:
                        if cache == 'cop' and MONEY >= 300:
                            print(f'[#] `cop` установлен на ({x}, {y})')
                            board[y][x] = 1
                            MONEY -= 300
                            Cop(x, y + 2)
                        elif cache == 'sotochka' and MONEY >= 100:
                            print(f'[#] `sotochka` установлен на ({x}, {y})')
                            board[y][x] = 2
                            MONEY -= 100
                            Sotochka(x, y + 2)
                        elif cache == 'sign' and MONEY >= 300:
                            print(f'[#] `sign` установлен на ({x}, {y})')
                            board[y][x] = 3
                            MONEY -= 300
                            Sign(x, y + 2)

    # столкновения
    bullet_collide = pygame.sprite.groupcollide(bullet_group, evil_group,
                                                False, False)
    npc_collide = pygame.sprite.groupcollide(npc_group, evil_group,
                                             True, True)

    for key, value in bullet_collide.items():
        key.kill()

    MONEY += 2
    POINTS += 1

    all_sprites.update()
    tiles_group.draw(screen)
    npc_group.draw(screen)
    bullet_group.draw(screen)
    evil_group.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
