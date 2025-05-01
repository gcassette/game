from abc import ABC, abstractmethod
import pygame
import math

class Weapon(ABC, pygame.sprite.Sprite):
    def __init__(self, name, pos, screen):
        super().__init__()
        self._name = name
        self.image = self.create_image()
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        self.velocity = pygame.math.Vector2(0,0)
        self.screen = screen

    @abstractmethod
    def shoot(self, all_sprites, bullets_sprites_group):
        pass

    #表示画像を生成する
    @abstractmethod
    def create_image(self) -> pygame.Surface:
        pass

    #弾の次フレームの移動ベクトルを計算
    @abstractmethod
    def next_velocity(self):
        pass

    def update(self):
        self.pos += self.velocity
        
        if not self.screen.get_rect().colliderect(self.rect):
            self.kill()

BULLET_SPEED = 10
class Bullet(Weapon):
    def __init__(self, pos, angle, screen):
        super().__init__("", pos, screen)
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        self.velocity = pygame.math.Vector2(
            math.cos(math.radians(angle)),
            -math.sin(math.radians(angle))
        ) * BULLET_SPEED

        self.screen = screen

    def create_image(self):
        super().create_image()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 0))

    def update(self):
        self.pos += self.velocity
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        if not self.screen.get_rect().colliderect(self.rect):
            self.kill()