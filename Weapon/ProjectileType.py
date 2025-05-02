from abc import ABC, abstractmethod
import pygame
import math

SE_BULLET_LINER = "assets/\u30d3\u30fc\u30e0\u97f3.mp3"
SE_VOLUME = 0.05

NAME_PROJECTILE_LINER = "Liner"
NAME_PROJECTILE_FIRE = "FireBall"

#投射物の抽象クラス
class Projectile(ABC, pygame.sprite.Sprite):
    def __init__(self, _name, get_position_func, get_direction_func, screen):
        super().__init__()
        self._name = _name
        self.screen = screen
        self.velocity = pygame.math.Vector2(0,0)

        #このクラスを保持しているcharacterの pos/angle 参照関数
        self.get_position = get_position_func
        self.get_direction = get_direction_func
        
        self.enable: bool = False
    
    #表示画像を生成する
    @abstractmethod
    def create_image(self) -> pygame.Surface:
        pass

    #弾の初速 velocity
    @abstractmethod
    def get_init_velocity(self) -> pygame.math.Vector2:
        pass
    #弾の次フレームの移動ベクトルを計算
    @abstractmethod
    def get_next_velocity(self) -> pygame.math.Vector2:
        pass

    @abstractmethod
    def clone(self) -> pygame.Surface:
        pass

    #自身を描画、運動を与える
    def shoot(self):
        self.enable = True
        #position, direction を取得・固定
        self.pos = self.get_position()
        self.direction = self.get_direction()

        #self.pos = pygame.math.Vector2(pos)
        self.image = self.create_image()
        self.rect = self.image.get_rect(center=self.pos)
        self.velocity = self.get_init_velocity()

    def update(self):
        if(not self.enable): return
        print(self.pos)
        print(self.velocity)
        self.pos += self.velocity
        self.velocity = self.get_next_velocity()
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        if not self.screen.get_rect().colliderect(self.rect):
            self.kill()

class BulletLinerly(Projectile):
    SPEED = 10
    SIZE = (10,10)
    COLOR = (255, 255, 0)

    def __init__(self, get_position_func, get_angle_func, screen):
        super().__init__(NAME_PROJECTILE_LINER, get_position_func, get_angle_func, screen)
        self.screen = screen

        self.beam_sound = pygame.mixer.Sound(SE_BULLET_LINER)
        self.beam_sound.set_volume(SE_VOLUME)

    def create_image(self) -> pygame.Surface:
        super().create_image()
        image = pygame.Surface(self.SIZE)
        image.fill(self.COLOR)
        return image

    def get_init_velocity(self):
        super().get_init_velocity()
        return self.direction * self.SPEED
    
    def get_next_velocity(self) -> pygame.math.Vector2:
        super().get_next_velocity()
        #等速直線運動のため変更なし
        return self.velocity
    
    def clone(self):
        return BulletLinerly(self.get_position, self.get_direction, self.screen)

    def shoot(self):
        self.beam_sound.play()
        super().shoot()

    def update(self):
        super().update()

class Fireball(Projectile):
    SPEED = 5
    SIZE = (12, 12)
    COLOR = (255, 100, 0)

    SPRITE_COORDINATE = (6, 6)
    SPRITE_RADIUS = 6
    #beam_sound = pygame.mixer.Sound(SE_BULLET_LINER)
    #beam_sound.set_volume(SE_VOLUME)

    def __init__(self, get_position_func, get_direction_func, screen):
        #
        super().__init__(NAME_PROJECTILE_FIRE, get_position_func, get_direction_func, screen)
        self.screen = screen

    def create_image(self) -> pygame.Surface:
        super().create_image()
        image = pygame.Surface(self.SIZE, pygame.SRCALPHA)
        image.fill(self.COLOR)
        pygame.draw.circle(image, self.COLOR, self.SPRITE_COORDINATE, self.SPRITE_RADIUS)  # 赤オレンジの火の玉
        
        return image

    def get_init_velocity(self):
        super().get_init_velocity()
        return self.velocity * self.SPEED

    def get_next_velocity(self) -> pygame.math.Vector2:
        super().get_next_velocity()
        #等速直線運動のため変更なし
        return self.velocity
    
    def clone(self) -> pygame.Surface:
        return Fireball(self.get_position, self.get_angle, self.screen)

    def shoot(self):
        self.beam_sound.play()
        super().shoot()

    def update(self):
        super().update()
