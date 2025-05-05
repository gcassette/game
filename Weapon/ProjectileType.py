from abc import ABC, abstractmethod
import pygame
import math

SE_BULLET_LINER = "assets/\u30d3\u30fc\u30e0\u97f3.mp3"
SE_VOLUME = 0.05

NAME_PROJECTILE_LINER = "Liner"
NAME_PROJECTILE_FIRE = "FireBall"

#投射物の抽象クラス
class Projectile(ABC, pygame.sprite.Sprite):
    def __init__(self, _name, get_position_func, shoot_direction,screen):
        super().__init__()
        self._name = _name
        self.screen = screen
        self.velocity = pygame.math.Vector2(0,0)

        #このクラスを保持しているcharacterの pos/angle 参照関数
        self.get_position = get_position_func
        self.shoot_direction = shoot_direction
        
        self.enable: bool = False

        self.beam_sound = pygame.mixer.Sound(SE_BULLET_LINER)
        self.beam_sound.set_volume(SE_VOLUME)
        self.SPEED = 10
        
        
    
    #表示画像を生成する
    @abstractmethod
    def create_image(self) -> pygame.Surface:
        pass

    def get_init_velocity(self) -> pygame.math.Vector2:
        return self.shoot_direction() * self.SPEED



    @abstractmethod
    def clone(self) -> pygame.Surface:
        pass

    #自身を描画、運動を与える
    def drawing_shoot(self):
        self.enable = True
        #position, direction を取得・固定
        self.pos = self.get_position()

        #self.pos = pygame.math.Vector2(pos)
        self.image = self.create_image()
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image) #当たり判定用のマスクを作成
        self.velocity = self.get_init_velocity()
        self.beam_sound.play()
        print(f"shoot {self._name}")
        print(f"pos: {self.pos[0]}, {self.pos[1]}")

    def update(self):
        if(not self.enable): return
        self.pos += self.velocity
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        if not self.screen.get_rect().colliderect(self.rect):

            self.kill()

class BulletLinerly(Projectile):
    SIZE = (12,12)
    COLOR = (255, 100, 0)
    
    SPRITE_COORDINATE = (6, 6)
    SPRITE_RADIUS = 6
    

    def __init__(self, get_position_func, shoot_direction, screen):
        super().__init__(NAME_PROJECTILE_LINER, get_position_func, shoot_direction, screen)
        self.SPEED = 10

    # def create_image(self) -> pygame.Surface:
    #     image = pygame.Surface(self.SIZE, pygame.SRCALPHA)  # ← 重要：透過情報つき
    #     image.fill(self.COLOR)
    #     pygame.draw.circle(image, self.COLOR, self.SPRITE_COORDINATE, self.SPRITE_RADIUS)  # 赤オレンジの火の玉
    #     return image
    def create_image(self) -> pygame.Surface:
        image = pygame.Surface(self.SIZE, pygame.SRCALPHA)
        image.fill(self.COLOR)
        pygame.draw.circle(image, (255, 255, 0), self.SPRITE_COORDINATE, self.SPRITE_RADIUS)  # 弾本体を黄色に
        print("create_image")
        return image
    def clone(self):
        return BulletLinerly(self.get_position, self.shoot_direction, self.screen)




class Fireball(Projectile):
    SIZE = (12, 12)
    COLOR = (255, 100, 0)

    SPRITE_COORDINATE = (6, 6)
    SPRITE_RADIUS = 6
    #beam_sound = pygame.mixer.Sound(SE_BULLET_LINER)
    #beam_sound.set_volume(SE_VOLUME)

    def __init__(self, get_position_func, shoot_direction, screen):
        super().__init__(NAME_PROJECTILE_FIRE, get_position_func, shoot_direction, screen)

        self.SPEED = 5

    def create_image(self) -> pygame.Surface:
        super().create_image()
        image = pygame.Surface(self.SIZE, pygame.SRCALPHA)
        image.fill(self.COLOR)
        pygame.draw.circle(image, self.COLOR, self.SPRITE_COORDINATE, self.SPRITE_RADIUS)  # 赤オレンジの火の玉
        
        return image
    
    def clone(self) -> Projectile:
        return Fireball(self.get_position, self.shoot_direction, self.screen)

