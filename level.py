import pygame

#Level configuration

WIDTH, HEIGHT = 800, 400

TILE_SIZE = 32
ground = pygame.Rect(0, HEIGHT - TILE_SIZE, WIDTH * 2 + (WIDTH/2), TILE_SIZE)

platforms = [
    pygame.Rect(200, HEIGHT - TILE_SIZE * 4, TILE_SIZE * 3, TILE_SIZE),
    pygame.Rect(400, HEIGHT - TILE_SIZE * 3, TILE_SIZE * 3, TILE_SIZE),
    pygame.Rect(600, HEIGHT - TILE_SIZE * 5, TILE_SIZE * 3, TILE_SIZE),
    pygame.Rect(800, HEIGHT - TILE_SIZE * 4, TILE_SIZE * 3, TILE_SIZE),
    pygame.Rect(1000, HEIGHT - TILE_SIZE * 3, TILE_SIZE * 3, TILE_SIZE),
    pygame.Rect(1200, HEIGHT - TILE_SIZE * 5, TILE_SIZE * 3, TILE_SIZE),
]

holes = [
    pygame.Rect(350, HEIGHT - TILE_SIZE, TILE_SIZE * 3, TILE_SIZE),
    pygame.Rect(950, HEIGHT - TILE_SIZE, TILE_SIZE * 3, TILE_SIZE),
]

deaths = [
    pygame.Rect(350, HEIGHT - 5, TILE_SIZE * 3, 10),
    pygame.Rect(950, HEIGHT - 5, TILE_SIZE * 3, 10),
]

finish_line = pygame.Rect(1800, HEIGHT - TILE_SIZE * 4, 20, TILE_SIZE * 3)
