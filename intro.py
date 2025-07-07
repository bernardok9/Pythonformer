import pygame
import sys

pygame.init()

# Screen Config
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Test Block Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)

# Map Limits
LEFT_LIMIT = -300
RIGHT_LIMIT = 1600

# Sprites
player_idle = pygame.image.load("assets/character/character_yellow_idle.png").convert_alpha()
player_hit = pygame.image.load("assets/character/character_yellow_hit.png").convert_alpha()
player_walk_a = pygame.image.load("assets/character/character_yellow_walk_a.png").convert_alpha()
player_walk_b = pygame.image.load("assets/character/character_yellow_walk_b.png").convert_alpha()
player_jump = pygame.image.load("assets/character/character_yellow_jump.png").convert_alpha()

# Sprites Sizes
PLAYER_WIDTH, PLAYER_HEIGHT = 40, 60
player_idle = pygame.transform.scale(player_idle, (PLAYER_WIDTH, PLAYER_HEIGHT))
player_hit = pygame.transform.scale(player_hit, (PLAYER_WIDTH, PLAYER_HEIGHT))
player_walk_a = pygame.transform.scale(player_walk_a, (PLAYER_WIDTH, PLAYER_HEIGHT))
player_walk_b = pygame.transform.scale(player_walk_b, (PLAYER_WIDTH, PLAYER_HEIGHT))
player_jump = pygame.transform.scale(player_jump, (PLAYER_WIDTH, PLAYER_HEIGHT))

# Plataforms
platforms = [
    pygame.Rect(150, HEIGHT - 80, 100, 20),
    pygame.Rect(300, HEIGHT - 130, 100, 20),
    pygame.Rect(500, HEIGHT - 180, 100, 20),
    pygame.Rect(900, HEIGHT - 130, 100, 20),
    pygame.Rect(1200, HEIGHT - 180, 100, 20),
]

# Restart
def reset():
    global player, velocity_y, on_ground, camera_x, alive, win, enemies
    global walk_timer, walk_frame, player_image, death_velocity

    player = pygame.Rect(50, HEIGHT - 70, PLAYER_WIDTH, PLAYER_HEIGHT)
    velocity_y = 0
    on_ground = False
    camera_x = 0
    alive = True
    win = False

    walk_timer = 0
    walk_frame = 0
    player_image = player_idle
    death_velocity = 0

    enemies = [
        {"rect": pygame.Rect(200, HEIGHT - 80 - 40, 40, 40), "dir": 1, "platform": platforms[0]},
        {"rect": pygame.Rect(550, HEIGHT - 180 - 40, 40, 40), "dir": -1, "platform": platforms[2]},
        {"rect": pygame.Rect(950, HEIGHT - 130 - 40, 40, 40), "dir": 1, "platform": platforms[3]},
    ]

# Cam
camera_x = 0

# Fields
grounds = [
    pygame.Rect(LEFT_LIMIT, HEIGHT - 20, 2000, 20),
]

holes = [
    pygame.Rect(400, HEIGHT - 20, 150, 20),
]

deaths = [
    pygame.Rect(400, HEIGHT - 5, 150, 10),
]

finish_line = pygame.Rect(1400, HEIGHT - 100, 20, 100)

reset()

# Main Loop Game
while True:
    screen.fill(WHITE)
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    # RESTART
    if keys[pygame.K_r] and (not alive or win):
        reset()

    if alive and not win:
        if keys[pygame.K_LEFT]:
            player.x -= 5
        if keys[pygame.K_RIGHT]:
            player.x += 5

        if player.x < LEFT_LIMIT:
            player.x = LEFT_LIMIT
        if player.right > RIGHT_LIMIT:
            player.right = RIGHT_LIMIT

        camera_x = max(LEFT_LIMIT, min(RIGHT_LIMIT - WIDTH, player.x - WIDTH // 2))

        # JUMP
        if keys[pygame.K_SPACE] and on_ground:
            velocity_y = -15
            on_ground = False

        velocity_y += 0.8
        player.y += velocity_y

        on_ground = False

        for g in grounds:
            if player.colliderect(g):
                player.bottom = g.top
                velocity_y = 0
                on_ground = True

        for plat in platforms:
            if player.colliderect(plat) and velocity_y > 0:
                if player.bottom - velocity_y <= plat.top + 5:
                    player.bottom = plat.top
                    velocity_y = 0
                    on_ground = True

        # ANIMATIONS
        if not on_ground:
            player_image = player_jump
        elif keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            walk_timer += 1
            if walk_timer >= 10:
                walk_timer = 0
                walk_frame = 1 - walk_frame
            player_image = player_walk_a if walk_frame == 0 else player_walk_b
        else:
            player_image = player_idle

        # ENEMIES
        for e in enemies:
            enemy = e["rect"]
            plat = e["platform"]
            enemy.x += e["dir"] * 2
            if enemy.left < plat.left:
                enemy.left = plat.left
                e["dir"] *= -1
            elif enemy.right > plat.right:
                enemy.right = plat.right
                e["dir"] *= -1

        # COLLISIONS
        for e in enemies[:]:
            enemy = e["rect"]
            if player.colliderect(enemy):
                if velocity_y > 0 and player.bottom - velocity_y <= enemy.top:
                    enemies.remove(e)
                    velocity_y = -7
                else:
                    alive = False

        # DEATH
        for death in deaths:
            if player.colliderect(death):
                alive = False

        # WIN
        if player.colliderect(finish_line):
            win = True

    elif not alive:
        death_velocity += 0.5
        player.y += death_velocity
        player_image = player_hit

    cam = camera_x

    for g in grounds:
        pygame.draw.rect(screen, GREEN, pygame.Rect(g.x - cam, g.y, g.width, g.height))

    for plat in platforms:
        pygame.draw.rect(screen, GREEN, pygame.Rect(plat.x - cam, plat.y, plat.width, plat.height))

    for hole in holes:
        pygame.draw.rect(screen, BLACK, pygame.Rect(hole.x - cam, hole.y, hole.width, hole.height))

    for death in deaths:
        pygame.draw.rect(screen, ORANGE, pygame.Rect(death.x - cam, death.y, death.width, death.height))

    for e in enemies:
        enemy = e["rect"]
        pygame.draw.rect(screen, RED, pygame.Rect(enemy.x - cam, enemy.y, enemy.width, enemy.height))

    pygame.draw.rect(screen, BLUE, pygame.Rect(finish_line.x - cam, finish_line.y, finish_line.width, finish_line.height))

    screen.blit(player_image, (player.x - cam, player.y))

    # MESSAGES
    font = pygame.font.SysFont(None, 48)
    if not alive and player.y > HEIGHT:
        text = font.render("Game Over! Press R", True, (255, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    if win:
        text = font.render("You Win! Press R", True, (0, 255, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()
