import pygame

from classes import Cop, Bullet, Sotochka, Sign, Gop, Drunk, Beggar
from screens import start_screen

pygame.init()
print('[!] инициализация pygame')
pygame.display.set_caption('УРАЛМАШ')
pygame.display.set_icon(pygame.image.load("data/icon.png"))


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

start_screen()  # открытие стартового окна