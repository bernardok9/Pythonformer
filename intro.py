import pygame
import sys
from enemy import Enemy, load_enemy_images
import level
from player import Player
import assets

pygame.init()

WIDTH, HEIGHT = level.WIDTH, level.HEIGHT
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

fly_images = load_enemy_images("fly")
ladybug_images = load_enemy_images("ladybug")
slimef_images = load_enemy_images("slime_f")
slimen_images = load_enemy_images("slime_n")
snail_images = load_enemy_images("snail")

flag_images = [
    pygame.image.load("assets/flag/flag_blue_a.png").convert_alpha(),
    pygame.image.load("assets/flag/flag_blue_b.png").convert_alpha()
]
flag_anim_index = 0
flag_anim_timer = 0
flag_anim_speed = 10

player = Player(50, HEIGHT - 70)

def create_enemies():
    return [
        Enemy(200, level.platforms[0].top - 32, ladybug_images, level.platforms[0]),
        Enemy(400, level.platforms[1].top - 32, slimef_images, level.platforms[1]),
        Enemy(600, level.platforms[2].top - 32, slimen_images, level.platforms[2]),
        Enemy(800, level.platforms[3].top - 32, snail_images, level.platforms[3]),
        Enemy(1100, 100, fly_images, is_fly=True),

        Enemy(800, level.ground.top - 32, snail_images, patrol_start=470, patrol_end=900),
        Enemy(840, level.ground.top - 32, snail_images, patrol_start=470, patrol_end=900),
        Enemy(880, level.ground.top - 32, snail_images, patrol_start=470, patrol_end=900),
        Enemy(920, level.ground.top - 32, snail_images, patrol_start=470, patrol_end=900),
    ]

enemies = create_enemies()

alive = True
win = False

def reset_game():
    global alive, win, enemies
    alive = True
    win = False
    player.reset(50, HEIGHT - 70)
    enemies = create_enemies()

while True:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()

    keys = pygame.key.get_pressed()

    if alive and not win:
        player.handle_input(keys)
        player.apply_gravity()
        player.update(level.platforms, [level.ground])

        for enemy in enemies:
            enemy.update()
            if player.rect.colliderect(enemy.rect) and enemy.alive:
                if player.velocity_y > 0 and player.rect.bottom - player.velocity_y <= enemy.rect.top:
                    enemy.alive = False
                    player.velocity_y = player.jump_power / 2
                else:
                    alive = False

        for death in level.deaths:
            if death.left < player.rect.centerx < death.right:
                if player.rect.bottom >= level.ground.top:
                    alive = False

        if player.rect.colliderect(level.finish_line):
            win = True
    else:
        player.animate_death()

    # cam player lock
    player.x = max(0, min(player.x, level.ground.width - player.width))

    # cam
    camera_offset = player.rect.x - WIDTH // 2
    camera_offset = max(0, min(camera_offset, level.ground.width - WIDTH))

    # background replicated
    for x in range(0, level.ground.width, assets.background.get_width()):
        screen.blit(assets.background, (x - camera_offset, 0))

    # ground
    for x in range(0, level.ground.width, 32):
        if x == 0:
            screen.blit(assets.ground_top_left, (x - camera_offset, level.ground.top))
        elif x + 32 >= level.ground.width:
            screen.blit(assets.ground_top_right, (x - camera_offset, level.ground.top))
        else:
            screen.blit(assets.ground_top, (x - camera_offset, level.ground.top))

        screen.blit(assets.ground_center, (x - camera_offset, level.ground.top + 32))
        screen.blit(assets.ground_center, (x - camera_offset, level.ground.top + 64))

    # plat
    for plat in level.platforms:
        x, y, w, h = plat.move(-camera_offset, 0)
        screen.blit(assets.platform_left, (x, y - 8))
        for i in range(1, (w // 32) - 1):
            screen.blit(assets.platform_middle, (x + i * 32, y - 8))
        screen.blit(assets.platform_right, (x + w - 32, y - 8))

    # holes
    for hole in level.holes:
        pygame.draw.rect(screen, (0, 0, 0), hole.move(-camera_offset, 0))
        for x in range(hole.left, hole.right, 32):
            screen.blit(assets.spike, (x - camera_offset, level.ground.top - 1))

    # spikes
    for death in level.deaths:
        pygame.draw.rect(screen, (0, 0, 0), death.move(-camera_offset, 0))
        for x in range(death.left, death.right, 32):
            screen.blit(assets.spike, (x - camera_offset, level.ground.top - 1))

    # enemies
    for enemy in enemies:
        screen.blit(enemy.get_image(), enemy.rect.move(-camera_offset, 0))

    # flag
    flag_anim_timer += 1
    if flag_anim_timer >= flag_anim_speed:
        flag_anim_timer = 0
        flag_anim_index = (flag_anim_index + 1) % len(flag_images)

    flag_img = pygame.transform.scale(flag_images[flag_anim_index], (32, 32 * 3))
    flag_pos = (level.finish_line.x - camera_offset, level.finish_line.y - flag_img.get_height() + level.finish_line.height)
    screen.blit(flag_img, flag_pos)

    # player
    screen.blit(player.get_image(), player.rect.move(-camera_offset, 0))

    # messages
    font = pygame.font.SysFont(None, 48)
    if not alive:
        text = font.render("Game Over! Press R to Restart", True, (255, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    if win:
        text = font.render("You Win! Press R to Restart", True, (0, 255, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))

    pygame.display.flip()
