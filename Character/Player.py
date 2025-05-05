import pygame
from Character.Character import Character
import Weapon.ProjectileType as ProjectileType
import math
from Weapon.Weapon import Weapon


Player_IMG_PATH = 'assets//calcium.png'
POSITION_START = (400, 300)
SPEED_PLAYER = 1
MAXHP_PLAYER = 5
ROTATE_SPEED = 3  # 回転速度（度単位）


class Player(Character):
    def __init__(self, screen, all_sprites, enemy_projectiles):
        self.angle = 0
        self.screen = screen

        self.invincible = False         # ← 無敵状態フラグ
        self.invincible_timer = 0       # ← 無敵タイマー（フレーム数）
        self.facing_left = False        # ← 左右反転状態を記録する変数

        super().__init__(Player_IMG_PATH, POSITION_START, all_sprites, enemy_projectiles, SPEED_PLAYER, MAXHP_PLAYER)
        

    def move(self):
        super().move()  # Characterのmove()を呼び出し

        # 画面内に制限する処理だけを追加
        self.rect.clamp_ip(self.screen.get_rect())
        self.pos.x = max(0, min(self.screen.get_width(), self.pos.x))
        self.pos.y = max(0, min(self.screen.get_height(), self.pos.y))

    def update(self):

        # 無敵状態タイマーのカウントダウン

        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

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
        # 左右反転状態を記録
        if self.direction.x < 0:
            self.facing_left = True
        elif self.direction.x > 0:
            self.facing_left = False

        if self.facing_left:
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = self.image.copy()

        self.mask = pygame.mask.from_surface(self.image)  # ← 画像変更後に再生成

        self.rect = self.image.get_rect(center=self.rect.center)
        #座標を出力
        #print(f"Player Position: {self.pos.x}, {self.pos.y}")

    def shoot(self):
        self.weapon.shoot()

    @property
    def shoot_direction(self):
        angle_rad = math.radians(self.angle)
        direction = pygame.math.Vector2(math.cos(angle_rad), math.sin(angle_rad))
        if self.facing_left:
            direction *= -1  # 左向きなら逆方向に発射
        return direction

    def set_bullets(self):
        bullet_type = ProjectileType.BulletLinerly(
            lambda: self.rect.center,
            lambda: self.shoot_direction,
            self.screen
        )
        #self.weapon = Weapon(self.all)  # ← bullets_group を渡す
        self.weapon.resister_bullet(bullet_type)

    def trigger_invincibility(self, duration_frames=60):
        self.invincible = True
        self.invincible_timer = duration_frames  # 60フレーム = 約1秒 (60FPSの場合)
