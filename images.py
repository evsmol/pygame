# изображения спрайтов

from helpers import load_image


fon_images = {
    'start': load_image('fon_start.jpg'),
    'end': load_image('fon_end.jpg'),
    'results': load_image('fon_results.jpg'),
    'manual': load_image('fon_manual.jpg'),
    'story': load_image('fon_story.jpg'),
    'characters': load_image('fon_characters.jpg')
}
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
    'drunk': load_image('drunk.png'),
    'minister': load_image('minister.png')
}
