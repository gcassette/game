import pygame
from Bullet import Bullet


Player_IMG_PATH = 'assets//robot.png'

# Constants
ROTATE_SPEED = 3  # 回転速度（度単位）


class Player(pygame.sprite.Sprite):
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
        bullet = Bullet(self.rect.center, self.angle, self.screen)
        all_sprites.add(bullet)
        bullets_sprites_group.add(bullet)
