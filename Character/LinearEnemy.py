import pygame
from Character.Character import Character
import random

IMG_LIN_ENEMY = 'assets//enemy_sake_belts.png'  # ← 適当な画像に置き換えてください

class LinearEnemy(Character):
    def __init__(self, screen, projectile_manager, get_player_pos):
        self.screen = screen
        self.get_player_pos = get_player_pos

        # 初期位置は画面内ランダム（必要に応じて調整）
        start_pos = (random.randint(100, 700), random.randint(100, 500))

        super().__init__(IMG_LIN_ENEMY, start_pos, projectile_manager, speed=2.0, max_hp=1)

        # プレイヤーの方向を測って初期方向を設定（ここだけ）
        target_pos = pygame.math.Vector2(self.get_player_pos())
        direction = target_pos - self.pos
        self.direction = direction.normalize() if direction.length_squared() > 0 else pygame.math.Vector2(0, 0)

    def set_bullets(self):
        pass  # 攻撃なしの敵

    def update(self):
        # 毎フレーム移動（方向は変えない）
        self.move()

        # 画面外に出たら消滅
        if not self.screen.get_rect().colliderect(self.rect):
            self.kill()
