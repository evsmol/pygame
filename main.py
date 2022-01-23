import os
import sys

import pygame
import pygame as pg

pygame.init()
size = width, height = 450, 350
screen = pygame.display.set_mode(size)
FPS = 50
tile_width = tile_height = 50


# музыка
# sound_start = pg.mixer.Sound('data/start.mp3')
# sound_start.set_volume(0.5)
# sound_main = pg.mixer.Sound('data/main.mp3')
# sound_main.set_volume(0.5)


# загрузка изображения
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# возвращает координаты клетки в виде кортежа
def get_cell(mouse_pos):
    if 0 <= mouse_pos[0] <= tile_width * 9:
        if tile_width * 2 <= mouse_pos[1] <= tile_width * 7:
            return (mouse_pos[0] - 0) // tile_width, \
                   (mouse_pos[1] - tile_width * 2) // tile_width
    return None


# выход из программы
def terminate():
    pygame.quit()
    sys.exit()


# стартовое окно
def start_screen():
    intro_text = ["Добро пожаловать на УРАЛМАШ", "",
                  "Чтобы выбрать уровень,",
                  "нажмите «1», «2» или «3».", "",
                  "Чтобы посмотреть статистику,",
                  "нажмите «N»."]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
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
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                # sound_start.stop()
                # sound_main.play()
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


tile_images = {
    'level1': load_image('stonecutter.png'),
    'level2': load_image('piston.png'),
    'level3': load_image('netherite.png')
}

nps_images = {
    'cop': load_image('cop.png'),
    'sotochka': load_image('sotochka.png')
}

evil_images = {
    'gop': load_image('gop.png')
}


# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
evil_group = pygame.sprite.Group()
nps_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Evil(pygame.sprite.Sprite):
    def __init__(self, evil_type, pos_x, pos_y):
        super().__init__(evil_group, all_sprites)
        self.image = evil_images[evil_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Nps(pygame.sprite.Sprite):
    def __init__(self, nps_type, pos_x, pos_y):
        super().__init__(evil_group, all_sprites)
        self.image = nps_images[nps_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


# class AnimatedSprite(pygame.sprite.Sprite):
#     def __init__(self, sheet, columns, rows, pos_x, pos_y):
#         super().__init__(all_sprites)
#         self.frames = []
#         self.cut_sheet(sheet, columns, rows)
#         self.cur_frame = 0
#         self.image = self.frames[self.cur_frame]
#         self.rect = self.rect.move(tile_width * pos_x, tile_height * pos_y)
#
#     def cut_sheet(self, sheet, columns, rows):
#         self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
#                                 sheet.get_height() // rows)
#         for j in range(rows):
#             for i in range(columns):
#                 frame_location = (self.rect.w * i, self.rect.h * j)
#                 self.frames.append(sheet.subsurface(pygame.Rect(
#                     frame_location, self.rect.size)))
#
#     def update(self):
#         self.cur_frame = (self.cur_frame + 1) % len(self.frames)
#         self.image = self.frames[self.cur_frame]


def generate_level():
    for y in range(5):
        for x in range(9):
            Tile('level1', x, y + 2)
    return 9, 5


# AnimatedSprite(load_image("portal.png"), 1, 32, 5, 5)
level_x, level_y = generate_level()

clock = pygame.time.Clock()
running = True
start_screen()

cache = 'cop'
board = [[0] * 9 for x in range(5)]
while running:
    screen.fill((128, 128, 128))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                cache = 'cop'  # 1
            if event.key == pygame.K_2:
                cache = 'sotochka'  # 2
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if get_cell(event.pos):
                    x, y = get_cell(event.pos)
                    if board[y][x] == 0:
                        Nps(cache, x, y + 2)
                        if cache == 'cop':
                            board[y][x] = 1
                        elif cache == 'sotochka':
                            board[y][x] = 2
        all_sprites.update()
    tiles_group.draw(screen)
    nps_group.draw(screen)
    evil_group.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
