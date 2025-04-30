import pygame
import math

Enemy_IMG_PATH = "Assets\\skull.png"
DISTANCE_ARRIVAL_PERMISSION = 5.0
FPS = 60

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.image = pygame.image.load(Enemy_IMG_PATH).convert_alpha()
        self.rect = self.image.get_rect()
        self.screen = screen

        self.speed = 3.0
        self.vx = 0
        self.vy = 0
        self.distance = 0.0

        self.appearancePosition = (self.screen.get_width() + 10, self.screen.get_height() / 2)
        self.attackPosition = (self.screen.get_width() / 2, self.screen.get_height() / 2)
        self.dissapearancePosition = (self.screen.get_width() / 2, -100)

        self.target_pos = None
        self.rect.center = self.appearancePosition

        # 状態変数（entry/attack/exit）
        self.phase = "entry"

        # 行動スクリプト生成
        self.script = self.behavior_script()
        next(self.script)

    def setTarget(self, position):
        dx = position[0] - self.rect.centerx
        dy = position[1] - self.rect.centery
        self.distance = math.hypot(dx, dy)
        if self.distance != 0:
            self.vx = dx / self.distance * self.speed
            self.vy = dy / self.distance * self.speed
        else:
            self.vx = self.vy = 0
        self.target_pos = position

    def update(self):
        try:
            next(self.script)
        except StopIteration:
            pass

    def behavior_script(self):
        # フェーズ: entry（出現 → 移動）
        self.phase = "entry"
        self.setTarget(self.attackPosition)
        while not self.isArrived():
            self.moveStep()
            yield

        # フェーズ: attack（停止 → 2秒待機）
        self.phase = "attack"
        self.vx = self.vy = 0
        yield from self.wait_frames(FPS * 2)  # 2秒

        # フェーズ: exit（退場）
        self.phase = "exit"
        self.setTarget(self.dissapearancePosition)
        while not self.isArrived():
            self.moveStep()
            yield

        self.kill()

    def moveStep(self):
        self.rect.centerx += self.vx
        self.rect.centery += self.vy
        dx = self.target_pos[0] - self.rect.centerx
        dy = self.target_pos[1] - self.rect.centery
        self.distance = math.hypot(dx, dy)

    def wait_frames(self, frames):
        for _ in range(frames):
            yield

    def isArrived(self) -> bool:
        return self.distance <= DISTANCE_ARRIVAL_PERMISSION

    def draw(self, screen):
        screen.blit(self.image, self.rect)
