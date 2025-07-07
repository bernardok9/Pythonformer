import pygame
import sys
import settings

pygame.init()
pygame.mixer.init()

import assets
import intro

WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

# colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# buttons
buttons = [
    {"label": "Jogar", "rect": pygame.Rect(300, 120, 200, 50)},
    {"label": "Opções", "rect": pygame.Rect(300, 190, 200, 50)},
    {"label": "Sair", "rect": pygame.Rect(300, 260, 200, 50)}
]

def draw_menu():
    screen.fill((30, 30, 30))
    for btn in buttons:
        pygame.draw.rect(screen, GRAY, btn["rect"])
        text = font.render(btn["label"], True, DARK_GRAY)
        screen.blit(text, (btn["rect"].x + 60, btn["rect"].y + 10))
    pygame.display.flip()

def options_menu():
    opt_font = pygame.font.SysFont(None, 40)
    music_rect = pygame.Rect(300, 120, 200, 50)
    sfx_rect = pygame.Rect(300, 190, 200, 50)
    back_rect = pygame.Rect(300, 260, 200, 50)

    running = True
    while running:
        screen.fill((30, 30, 30))

        pygame.draw.rect(screen, GRAY, music_rect)
        pygame.draw.rect(screen, GRAY, sfx_rect)
        pygame.draw.rect(screen, DARK_GRAY, back_rect)

        music_text = f"Música: {'Ativado' if settings.music_enabled else 'Desativado'}"
        sfx_text = f"Efeitos: {'Ativado' if settings.sfx_enabled else 'Desativado'}"

        screen.blit(opt_font.render(music_text, True, WHITE), (music_rect.x + 10, music_rect.y + 10))
        screen.blit(opt_font.render(sfx_text, True, WHITE), (sfx_rect.x + 10, sfx_rect.y + 10))
        screen.blit(opt_font.render("Voltar", True, WHITE), (back_rect.x + 60, back_rect.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if music_rect.collidepoint(event.pos):
                    settings.music_enabled = not settings.music_enabled
                    pygame.mixer.music.stop()
                    assets.play_sfx(assets.sfx_coin)
                elif sfx_rect.collidepoint(event.pos):
                    settings.sfx_enabled = not settings.sfx_enabled
                    assets.play_sfx(assets.sfx_coin)
                elif back_rect.collidepoint(event.pos):
                    assets.play_sfx(assets.sfx_select)
                    running = False

        clock.tick(60)

def main_menu():
    while True:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for btn in buttons:
                    if btn["rect"].collidepoint(event.pos):
                        assets.play_sfx(assets.sfx_select)
                        if btn["label"] == "Jogar":
                            intro.run_game_loop()
                        elif btn["label"] == "Opções":
                            options_menu()
                        elif btn["label"] == "Sair":
                            pygame.quit()
                            sys.exit()
        clock.tick(60)

if __name__ == "__main__":
    main_menu()
