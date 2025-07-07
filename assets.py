import pygame


def scale_image(img, size=(32, 32)):
    return pygame.transform.scale(img, size)

# Background
background = pygame.image.load("assets/background/background_color_trees.png")

# Ground
ground_center = scale_image(pygame.image.load("assets/tileset/ground/terrain_grass_block_center.png"))
ground_left = scale_image(pygame.image.load("assets/tileset/ground/terrain_grass_block_left.png"))
ground_right = scale_image(pygame.image.load("assets/tileset/ground/terrain_grass_block_right.png"))
ground_top_left = scale_image(pygame.image.load("assets/tileset/ground/terrain_grass_block_top_left.png"))
ground_top_right = scale_image(pygame.image.load("assets/tileset/ground/terrain_grass_block_top_right.png"))
ground_top = scale_image(pygame.image.load("assets/tileset/ground/terrain_grass_block_top.png"))

# Platforms
platform_left = scale_image(pygame.image.load("assets/tileset/plataform/terrain_grass_horizontal_left.png"))
platform_middle = scale_image(pygame.image.load("assets/tileset/plataform/terrain_grass_horizontal_middle.png"))
platform_right = scale_image(pygame.image.load("assets/tileset/plataform/terrain_grass_horizontal_right.png"))

# Spikes
spike = scale_image(pygame.image.load("assets/tileset/trap/spikes.png"))

# Sons
sfx_disappear = pygame.mixer.Sound("assets/sounds/sfx_disappear.ogg")  # morrer
sfx_hurt = pygame.mixer.Sound("assets/sounds/sfx_hurt.ogg")            # matar inimigo
sfx_jump = pygame.mixer.Sound("assets/sounds/sfx_jump.ogg")            # pular
sfx_magic = pygame.mixer.Sound("assets/sounds/sfx_magic.ogg")          # pegar bandeira
sfx_select = pygame.mixer.Sound("assets/sounds/sfx_select.ogg")        # escolher opção
sfx_coin = pygame.mixer.Sound("assets/sounds/sfx_coin.ogg")            # selecionar opção