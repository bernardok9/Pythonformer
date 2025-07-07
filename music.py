import pygame
import os
import settings

MUSIC_FOLDER = "assets/soundtrack"
MUSIC_FILES = sorted([
    f for f in os.listdir(MUSIC_FOLDER)
    if f.startswith("jingles_NES") and f.endswith(".ogg")
])

current_music_index = 0

def init_music(volume=0.5):
    if not settings.music_enabled or not MUSIC_FILES:
        return
    pygame.mixer.music.set_volume(volume)
    play_next_music()

def play_next_music():
    global current_music_index
    if not settings.music_enabled or not MUSIC_FILES:
        return
    if current_music_index >= len(MUSIC_FILES):
        current_music_index = 0
    pygame.mixer.music.load(os.path.join(MUSIC_FOLDER, MUSIC_FILES[current_music_index]))
    pygame.mixer.music.play()
    current_music_index += 1

def update_music():
    if settings.music_enabled and not pygame.mixer.music.get_busy():
        play_next_music()
    elif not settings.music_enabled:
        pygame.mixer.music.stop()
