import pygame
import math

BULLET_SPEED = 10
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle, screen):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        self.velocity = pygame.math.Vector2(
            math.cos(math.radians(angle)),
            -math.sin(math.radians(angle))
        ) * BULLET_SPEED

        self.screen = screen

    def update(self):
        self.pos += self.velocity
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        if not self.screen.get_rect().colliderect(self.rect):
            self.kill()