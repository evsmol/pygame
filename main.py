import pygame

from screens import start_screen


pygame.init()
print('[!] инициализация pygame')
pygame.display.set_caption('УРАЛМАШ')
pygame.display.set_icon(pygame.image.load("data/icon.png"))

start_screen()  # открытие стартового окна
