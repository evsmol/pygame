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
    if LEVEL[0]:
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


# сохранение результата игры
def save_result():
    print("[#] сохранение результатов")
    con = sqlite3.connect("records_db.db")
    cur = con.cursor()
    cur.execute(f"UPDATE records "
                f"SET last = False "
                f"WHERE last = True").fetchall()
    cur.execute(f"INSERT INTO records(level,result,last) "
                f"VALUES({LEVEL[0]},{POINTS[0] // 10},True)").fetchall()
    con.commit()
    con.close()


# получить результаты игр
def get_results():
    print("[#] получение результатов")
    con = sqlite3.connect("records_db.db")
    cur = con.cursor()
    result_level1 = cur.execute(f"SELECT result "
                                f"FROM records "
                                f"WHERE level = 1").fetchall()
    result_level2 = cur.execute(f"SELECT result "
                                f"FROM records "
                                f"WHERE level = 2").fetchall()
    result_level3 = cur.execute(f"SELECT result "
                                f"FROM records "
                                f"WHERE level = 3").fetchall()
    result_last = cur.execute(f"SELECT level, result "
                              f"FROM records "
                              f"WHERE last = True").fetchall()
    con.close()

    res_lev1 = []
    for res in result_level1:
        res_lev1.append(res[0])
    res_lev2 = []
    for res in result_level2:
        res_lev2.append(res[0])
    res_lev3 = []
    for res in result_level3:
        res_lev3.append(res[0])
    res_last = result_last[0]

    res_lev1.sort(reverse=True)
    res_lev2.sort(reverse=True)
    res_lev3.sort(reverse=True)
    last_place = None
    if res_last[0] == 1:
        last_place = res_lev1.index(res_last[1]) + 1
    elif res_last[0] == 2:
        last_place = res_lev2.index(res_last[1]) + 1
    elif res_last[0] == 3:
        last_place = res_lev3.index(res_last[1]) + 1
    res_last = (res_last[0], res_last[1], last_place)  # уровень, очки, место

    return res_lev1[0], res_lev2[0], res_lev3[0], res_last
