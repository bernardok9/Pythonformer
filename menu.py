import pygame
import sys

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
                        assets.sfx_select.play()
                        if btn["label"] == "Jogar":
                            intro.run_game_loop()
                        elif btn["label"] == "Opções":
                            print("aaaaaaaaaaaaaa")
                        elif btn["label"] == "Sair":
                            pygame.quit()
                            sys.exit()
        clock.tick(60)

if __name__ == "__main__":
    main_menu()
