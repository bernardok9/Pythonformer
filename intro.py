import pygame
import sys
import random

pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Players vars
player = pygame.Rect(200, 540, 40, 40)
velocity_y = 0
gravity = 0.4
boost_strength = -13
alive = True
launched = False

# Ground
launch_pad = pygame.Rect(0, 580, WIDTH, 20)

# Starter Portals
portals = []
for i in range(10):
    x = random.randint(50, 300)
    y = 550 - i * 60
    portals.append(pygame.Rect(x, y, 100, 15))

# UI / Camera
camera_offset = 0
font = pygame.font.SysFont(None, 48)
reset_button = pygame.Rect(WIDTH // 2 - 60, HEIGHT // 2 + 50, 120, 40)
score = 0
CAMERA_FOLLOW_Y = int(HEIGHT * 0.6)


# Main Loop
running = True
while running:
    screen.fill((20, 20, 30))
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if alive:
        keys = pygame.key.get_pressed()

        # Left Right
        if keys[pygame.K_LEFT]:
            player.x -= 5
        if keys[pygame.K_RIGHT]:
            player.x += 5

        # Space to Launch
        if not launched:
            if keys[pygame.K_SPACE]:
                launched = True
                velocity_y = boost_strength
        else:
            velocity_y += gravity
            player.y += velocity_y

            # Collision: DOWN-UP (Boost) UP-DOWN (DEATH)
            for portal in portals:
                if (player.colliderect(portal) and velocity_y < 0):
                    velocity_y = boost_strength
                elif (
                    player.colliderect(portal)
                    and velocity_y > 0
                    and player.bottom - velocity_y <= portal.top
                ):
                    alive = False

            # CAMERA
            if player.y < CAMERA_FOLLOW_Y:
                dy = CAMERA_FOLLOW_Y - player.y
                player.y = CAMERA_FOLLOW_Y
                camera_offset += dy
                for p in portals:
                    p.y += dy

            score = max(score, int(camera_offset))

            # REMOVE PORTALS ON CAMERA UP
            while portals and portals[0].y > HEIGHT:
                portals.pop(0)

            # ADD PORTALS ON CAMERA UP
            while len(portals) < 10:
                last_y = portals[-1].y if portals else 0
                x = random.randint(40, 300)
                y = last_y - random.randint(60, 100)
                portals.append(pygame.Rect(x, y, 100, 15))

    # DRAW - LAUNCHPAD
    pygame.draw.rect(screen, (80, 80, 80), launch_pad)

    # DRAW - PORTAL
    for portal in portals:
        pygame.draw.rect(screen, (0, 255, 255), portal)

    # DRAW - PLAYER
    pygame.draw.rect(screen, (255, 100, 0), player)

    if not launched:
        txt = font.render("Pressione espaço para lançar!", True, (255, 255, 255))
        screen.blit(txt, (WIDTH // 2 - txt.get_width() // 2, 200))

    if not alive:
        text = font.render("Você caiu!", True, (255, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
    
        # RESET
        pygame.draw.rect(screen, (50, 150, 50), reset_button)
        reset_text = font.render("Reset", True, (255, 255, 255))
        screen.blit(reset_text, (reset_button.x + (reset_button.width - reset_text.get_width()) // 2,
                                reset_button.y + (reset_button.height - reset_text.get_height()) // 2))

        # RESET - ONCLICK
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0] and reset_button.collidepoint(mouse_pos):
            # Resetar o jogo
            player.x = 200
            player.y = 540
            velocity_y = 0
            alive = True
            launched = False
            camera_offset = 0
            score = 0
            portals.clear()
            for i in range(10):
                x = random.randint(50, 300)
                y = 550 - i * 60
                portals.append(pygame.Rect(x, y, 100, 15))

    # SCORE
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
