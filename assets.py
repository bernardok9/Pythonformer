import pygame

def scale_image(img, size=(32, 32)):
    return pygame.transform.scale(img, size)

# Background
background = pygame.image.load("assets/background/background_color_trees.png").convert()

# Ground
ground_center = scale_image(pygame.image.load("assets/tileset/ground/terrain_grass_block_center.png").convert_alpha())
ground_left = scale_image(pygame.image.load("assets/tileset/ground/terrain_grass_block_left.png").convert_alpha())
ground_right = scale_image(pygame.image.load("assets/tileset/ground/terrain_grass_block_right.png").convert_alpha())
ground_top_left = scale_image(pygame.image.load("assets/tileset/ground/terrain_grass_block_top_left.png").convert_alpha())
ground_top_right = scale_image(pygame.image.load("assets/tileset/ground/terrain_grass_block_top_right.png").convert_alpha())
ground_top = scale_image(pygame.image.load("assets/tileset/ground/terrain_grass_block_top.png").convert_alpha())

# Platforms
platform_left = scale_image(pygame.image.load("assets/tileset/plataform/terrain_grass_horizontal_left.png").convert_alpha())
platform_middle = scale_image(pygame.image.load("assets/tileset/plataform/terrain_grass_horizontal_middle.png").convert_alpha())
platform_right = scale_image(pygame.image.load("assets/tileset/plataform/terrain_grass_horizontal_right.png").convert_alpha())

# Spikes
spike = scale_image(pygame.image.load("assets/tileset/trap/spikes.png").convert_alpha())