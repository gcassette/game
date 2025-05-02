import pygame
from Character.Character import Character
import Weapon.ProjectileType as ProjectileType


Player_IMG_PATH = 'assets//calcium.png'
POSITION_START = (400, 300)
ANGLE_PLAYER = 0
SPEED_PLAYER = 1
MAXHP_PLAYER = 5

ROTATE_SPEED = 3  # 回転速度（度単位）

"""
class Player(Character):
    def __init__(self, screen):
        super().__init__()
        self.original_image = pygame.image.load(Player_IMG_PATH).convert_alpha()
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 1
        self.angle = 0  # 向いている角度（度）

        self.screen = screen
        self.weapon = Weapon(lambda: self.rect.center, self.angle, self.screen)
        self.direction = pygame.math.Vector2(0, 0)  # 移動方向はキー入力に基づく

    def update(self):
        keys = pygame.key.get_pressed()

        # 回転処理（W/Sキー）
        if keys[pygame.K_w]:
            self.angle += ROTATE_SPEED
        if keys[pygame.K_s]:
            self.angle -= ROTATE_SPEED

        # 移動処理（矢印キー）
        self.direction.x = 0
        self.direction.y = 0

        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.direction.x = 1

        if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
            self.direction.y = 1

        if self.direction.length() != 0:
            self.direction = self.direction.normalize()

        self.pos += self.direction * self.speed
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        # 画面内制限
        screen_rect = self.screen.get_rect()
        self.rect.clamp_ip(screen_rect)
        self.pos.x = max(0, min(self.screen.get_width(), self.pos.x))
        self.pos.y = max(0, min(self.screen.get_height(), self.pos.y))

        # 回転画像の再描画（angleだけに基づく）
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def shoot(self, all_sprites, bullets_sprites_group):
        self.weapon.shoot(all_sprites, bullets_sprites_group)
"""

class Player(Character):
    def __init__(self, screen, sprite_manager):
        self.angle = ANGLE_PLAYER
        self.screen = screen

        super().__init__(Player_IMG_PATH, POSITION_START, sprite_manager, SPEED_PLAYER, MAXHP_PLAYER)
        

    def move(self):
        super().move()  # Characterのmove()を呼び出し

        # 画面内に制限する処理だけを追加
        self.rect.clamp_ip(self.screen.get_rect())
        self.pos.x = max(0, min(self.screen.get_width(), self.pos.x))
        self.pos.y = max(0, min(self.screen.get_height(), self.pos.y))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.angle += ROTATE_SPEED
        if keys[pygame.K_s]:
            self.angle -= ROTATE_SPEED

        self.direction.update(0, 0)
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.direction.x = 1

        if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
            self.direction.y = 1

        self.move()
        self.image = pygame.transform.rotate(self.original_image, self.angle)
         # ← 左に向いてるときだけ左右反転
        if self.direction.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect(center=self.rect.center)

    def shoot(self):
        self.weapon.shoot()

    def set_bullets(self):
        bullet_type = ProjectileType.BulletLinerly(lambda: self.rect.center, lambda: self.direction, self.screen)
        self.weapon.resister_bullet(bullet_type)
