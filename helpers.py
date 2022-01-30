# вспомогательные функции

import pygame
import sys
import os
import sqlite3

from config import tile_width, tile_height
from config import POINTS, LEVEL


# выход из программы
def terminate():
    print("[!] выход из программы")
    save_result()
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


# сохранение результата
def save_result():
    print("[#] сохранение результатов")
    con = sqlite3.connect("records_db.db")
    cur = con.cursor()
    cur.execute(f"UPDATE records "
                f"SET last = False "
                f"WHERE last = True").fetchall()
    cur.execute(f"INSERT INTO records(level,result,last) "
                f"VALUES({LEVEL[0]},{POINTS[0] // 10},"
                f"True)").fetchall()
    con.commit()
