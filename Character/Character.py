import pygame
from abc import ABC, abstractmethod
import CommonSystem
import Weapon

class Character(pygame.sprite.Sprite, ABC):
    def __init__(self, image_path, start_pos, sprite_manager, speed=1, max_hp=1):
        super().__init__()
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = self.original_image.copy()
        #characterのscreen上の位置をrectで管理する、
        self.rect = self.image.get_rect(center=start_pos)
        #characterの本当の位置をposで管理する、
        self.pos = pygame.math.Vector2(self.rect.center)
        #directionは移動方向を表すベクトル、speedは移動速度を表す。characterの移動距離はspeed * directionで決まる。
        self.speed = speed
        self.direction = CommonSystem.DirectionUnit(1, 0)

        self.max_hp = max_hp
        self.hp = max_hp

        #武器の装備
        self.weapon = Weapon.Weapon(sprite_manager)
        self.set_bullets()

    @abstractmethod
    def set_bullets(self):
        pass

    def move(self):
        #directionは移動方向を表すベクトルのため正規化を行い、長さを1にする。
        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()
        else:
            self.direction.update(0, 0)
        self.pos += self.direction * self.speed
        self.rect.center = (round(self.pos.x), round(self.pos.y))

    def take_damage(self, damage=1):
        self.hp -= damage
        if self.hp <= 0:
            self.kill()
     