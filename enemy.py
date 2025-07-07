import pygame
import math

class Enemy:
    def __init__(self, x, y, images, platform=None, is_fly=False, patrol_start=None, patrol_end=None):
        self.size = 32
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.images = images
        self.image_index = 0
        self.timer = 0
        # enemy dirlook
        self.dir = -1
        self.platform = platform
        self.is_fly = is_fly
        self.y_base = y
        self.alive = True
        self.spawn_x = x
        self.spawn_y = y
        self.velocity_y = 0
        self.patrol_start = patrol_start
        self.patrol_end = patrol_end

    def update(self):
        if not self.alive:
            self.velocity_y += 0.5
            self.rect.y += self.velocity_y
            return

        self.timer += 1
        if self.timer >= 10:
            self.timer = 0
            self.image_index = (self.image_index + 1) % len(self.images["walk"])

        self.rect.x += self.dir * 2

        # patrol
        if self.patrol_start is not None and self.patrol_end is not None:
            if self.rect.left <= self.patrol_start:
                self.dir = 1
            elif self.rect.right >= self.patrol_end:
                self.dir = -1
        elif self.platform and not self.is_fly:
            if self.rect.left < self.platform.left or self.rect.right > self.platform.right:
                self.dir *= -1

        if self.is_fly:
            self.rect.y = self.y_base + int(10 * math.sin(pygame.time.get_ticks() / 300))

    def get_image(self):
        if not self.alive:
            return self.images["rest"]
        base_image = self.images["walk"][self.image_index]
        return pygame.transform.flip(base_image, True, False) if self.dir == 1 else base_image

    def reset(self):
        self.rect.x = self.spawn_x
        self.rect.y = self.spawn_y
        self.velocity_y = 0
        self.alive = True
        self.image_index = 0
        self.timer = 0


def load_enemy_images(enemy_type, scale=(32, 32)):
    def load(path):
        return pygame.transform.scale(pygame.image.load(path).convert_alpha(), scale)

    if enemy_type == "fly":
        return {
            "walk": [load("assets/enemies/fly/fly_a.png"), load("assets/enemies/fly/fly_b.png")],
            "rest": load("assets/enemies/fly/fly_rest.png")
        }
    elif enemy_type == "ladybug":
        return {
            "walk": [load("assets/enemies/ladybug/ladybug_walk_a.png"), load("assets/enemies/ladybug/ladybug_walk_b.png")],
            "rest": load("assets/enemies/ladybug/ladybug_rest.png")
        }
    elif enemy_type == "slime_f":
        return {
            "walk": [load("assets/enemies/slime_f/slime_fire_walk_a.png"), load("assets/enemies/slime_f/slime_fire_walk_b.png")],
            "rest": load("assets/enemies/slime_f/slime_fire_rest.png")
        }
    elif enemy_type == "slime_n":
        return {
            "walk": [load("assets/enemies/slime_n/slime_normal_walk_a.png"), load("assets/enemies/slime_n/slime_normal_walk_b.png")],
            "rest": load("assets/enemies/slime_n/slime_normal_rest.png")
        }
    elif enemy_type == "snail":
        return {
            "walk": [load("assets/enemies/snail/snail_walk_a.png"), load("assets/enemies/snail/snail_walk_b.png")],
            "rest": load("assets/enemies/snail/snail_rest.png")
        }
    else:
        raise ValueError(f"Unknown enemy type: {enemy_type}")
