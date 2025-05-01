from abc import ABC, abstractmethod
import pygame
import math

class Weapon:
    def __init__(self, get_position_func, _angle, screen):
        super().__init__()
        self.get_position = get_position_func
        self.angle = _angle
        self.screen = screen

    def shoot(self, all_sprites, bullets_sprites_group):
        pos = self.get_position()
        bullet = BulletLinerly(pos, self.angle, self.screen)
        all_sprites.add(bullet)
        bullets_sprites_group.add(bullet)

class Bullet(ABC, pygame.sprite.Sprite):
    def __init__(self, _name, _pos, screen):
        super().__init__()
        self._name = _name
        self.image = self.create_image()
        self.rect = self.image.get_rect(center=_pos)
        self.pos = pygame.math.Vector2(_pos)
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
class BulletLinerly(Bullet):
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

    def create_image(self) -> pygame.Surface:
        super().create_image()
        image = pygame.Surface((10, 10))
        image.fill((255, 255, 0))
        return image

    def next_velocity(self):
        super().next_velocity()

    def shoot(self, all_sprites, bullets_sprites_group):
        bullet = Bullet(self.rect.center, self.angle, self.screen)
        all_sprites.add(bullet)
        bullets_sprites_group.add(bullet)

    def update(self):
        self.pos += self.velocity
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        if not self.screen.get_rect().colliderect(self.rect):
            self.kill()