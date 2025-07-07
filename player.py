import pygame
import assets
import settings

class Player:
    def __init__(self, x, y):
        self.width = 40
        self.height = 60

        # hitbox
        self.hitbox_width = 30
        self.hitbox_height = 50
        self.hitbox_offset_x = (self.width - self.hitbox_width) // 2  # 5
        self.hitbox_offset_y = (self.height - self.hitbox_height) // 2  # 5

        # pos.x pos.y
        self.x = x
        self.y = y

        self.rect = pygame.Rect(self.x + self.hitbox_offset_x, self.y + self.hitbox_offset_y, 
                                self.hitbox_width, self.hitbox_height)

        self.velocity_y = 0
        self.gravity = 0.8
        self.jump_power = -15
        self.on_ground = False
        self.death_velocity = 0

        # player dirlook
        self.facing = 1

        # spr actions
        self.sprites = {
            "idle": pygame.transform.scale(pygame.image.load("assets/character/character_yellow_idle.png"), (self.width, self.height)),
            "jump": pygame.transform.scale(pygame.image.load("assets/character/character_yellow_jump.png"), (self.width, self.height)),
            "hit": pygame.transform.scale(pygame.image.load("assets/character/character_yellow_hit.png"), (self.width, self.height)),
            "walk": [
                pygame.transform.scale(pygame.image.load("assets/character/character_yellow_walk_a.png"), (self.width, self.height)),
                pygame.transform.scale(pygame.image.load("assets/character/character_yellow_walk_b.png"), (self.width, self.height)),
            ]
        }

        self.walk_timer = 0
        self.walk_frame = 0
        self.image = self.sprites["idle"]

    def update_rect(self):
        self.rect.x = self.x + self.hitbox_offset_x
        self.rect.y = self.y + self.hitbox_offset_y

    def handle_input(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= 5
            self.facing = -1
        if keys[pygame.K_RIGHT]:
            self.x += 5
            self.facing = 1
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False
            if settings.sfx_enabled:
                assets.sfx_jump.play()

        self.update_rect()

    def apply_gravity(self):
        self.velocity_y += self.gravity
        self.y += self.velocity_y
        self.update_rect()

    def update(self, platforms, grounds):
        self.on_ground = False

        # ground collider
        for g in grounds:
            if self.rect.colliderect(g):
                self.y = g.top - self.hitbox_height - self.hitbox_offset_y
                self.velocity_y = 0
                self.on_ground = True
                self.update_rect()

        for plat in platforms:
            if self.rect.colliderect(plat) and self.velocity_y > 0:
                if self.rect.bottom - self.velocity_y <= plat.top + 5:
                    self.y = plat.top - self.hitbox_height - self.hitbox_offset_y
                    self.velocity_y = 0
                    self.on_ground = True
                    self.update_rect()

        # "animation switch"
        if not self.on_ground:
            self.image = self.sprites["jump"]
        elif pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.walk_timer += 1
            if self.walk_timer >= 10:
                self.walk_timer = 0
                self.walk_frame = 1 - self.walk_frame
            self.image = self.sprites["walk"][self.walk_frame]
        else:
            self.image = self.sprites["idle"]

    def animate_death(self):
        self.death_velocity += 0.5
        self.y += self.death_velocity
        self.update_rect()
        self.image = self.sprites["hit"]

    def get_image(self):
        if self.facing == -1:
            return pygame.transform.flip(self.image, True, False)
        return self.image

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.velocity_y = 0
        self.on_ground = False
        self.walk_timer = 0
        self.walk_frame = 0
        self.death_velocity = 0
        self.image = self.sprites["idle"]
        self.update_rect()
