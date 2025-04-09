import os.path

import pygame

data_directory = ''
font_cache = {}
image_cache = {}
sound_cache = {}
data_cache = {}

def clear():
    global data_cache
    global font_cache
    global image_cache
    global sound_cache
    font_cache = {}
    image_cache = {}
    sound_cache = {}
    data_cache = {}


def get_font(filename, size):
    if (filename, size) in font_cache:
        return font_cache[(filename, size)]
    else:
        font = pygame.font.Font(os.path.join(data_directory, filename), size)
        font_cache[(filename, size)] = font
        return font


def get_image(filename):
    if filename in image_cache:
        return image_cache[filename]
    else:
        if isinstance(filename, tuple):
            (name, color) = filename
            surface = pygame.image.load(os.path.join(data_directory, name))
            index = surface.map_rgb((255, 0, 8))
            surface.set_palette_at(index, color)
        else:
            surface = pygame.image.load(os.path.join(data_directory, filename))
        surface = surface.convert_alpha()
        image_cache[filename] = surface
        return surface


def get_sound(filename):
    if filename in sound_cache:
        return sound_cache[filename]
    else:
        sound = pygame.mixer.Sound(os.path.join(data_directory, filename))
        sound_cache[filename] = sound
        return sound


def get_data(filename):
    if filename in data_cache:
        return data_cache[filename]
    else:
        namespace = {}
        exec(compile(open(os.path.join(data_directory, filename), "rb").read(), os.path.join(data_directory, filename), 'exec'), namespace)
        data = {}
        for name in namespace:
            if not name.startswith('_'):
                data[name] = namespace[name]

        data_cache[filename] = data
        return data
