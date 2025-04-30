import pygame
import math

Enemy_IMG_PATH = 'assets//skull.png'

class Enemy(pygame.sprite.Sprite):
    ENEMY_RETREAT_EVENT = pygame.USEREVENT + 1

    def __init__(self, screen):
        super().__init__()
        self.image = pygame.image.load(Enemy_IMG_PATH).convert_alpha()
        self.rect = self.image.get_rect()
        self.screen = screen

        # 移動速度
        self.speed = 3.0
        self.vx = 0
        self.vy = 0

        # フェーズ管理
        self.phase = "entry"
        pygame.time.set_timer(self.ENEMY_RETREAT_EVENT, 2000)  # 2秒後に退場イベント発生

        # 各位置定義
        self.appearancePosition = (self.screen.get_width() / 2, -self.rect.height)
        self.attackPosition = (self.screen.get_width() / 2, self.screen.get_height() / 2)
        self.dissapearancePosition = (self.screen.get_width() / 2, -100)

        # 初期化
        self.rect.center = self.appearancePosition
        self.setTarget(self.attackPosition)

    def setTarget(self, position):
        dx = position[0] - self.rect.centerx
        dy = position[1] - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance != 0:
            self.vx = dx / distance * self.speed
            self.vy = dy / distance * self.speed
        else:
            self.vx = self.vy = 0
        self.target_pos = position

    def update(self):
        if self.target_pos:
            dx = self.target_pos[0] - self.rect.centerx
            dy = self.target_pos[1] - self.rect.centery
            if abs(dx) < abs(self.vx) and abs(dy) < abs(self.vy):
                self.rect.center = self.target_pos
                self.vx = self.vy = 0

                if self.phase == "entry":
                    self.phase = "wait"
                    pygame.time.set_timer(self.ENEMY_RETREAT_EVENT, 2000)  # 2秒待機後退場
                elif self.phase == "exit":
                    self.kill()
            else:
                self.rect.centerx += self.vx
                self.rect.centery += self.vy

    def exit(self):
        self.phase = "exit"
        self.setTarget(self.dissapearancePosition)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
