import pygame
import random
from Character.Character import Character
import Weapon.ProjectileType as ProjectileType

IMG_CEnemy = 'assets//enemy_sake.png'

class ChaseEnemy(Character):
    def __init__(self, screen, projectile_manager, get_player_pos, update_interval=1):
        """
        player_pos_getter: プレイヤー位置を返す関数またはlambda
        update_interval: 方向を更新する間隔（フレーム数）。1なら毎フレーム更新。
        """
        self.screen = screen
        self.get_player_pos = get_player_pos
        self.update_interval = update_interval
        self.update_counter = 0
        self.cooldown_timer = 0  # ← クールダウン用のフレームカウント
        self.is_on_cooldown = False  # ← クールダウン中かどうかのフラグ

        # 初期位置はランダム
        start_pos = (random.randint(100, 700), random.randint(100, 500))
        super().__init__(IMG_CEnemy, start_pos, projectile_manager, speed=0.5, max_hp=3)

    def set_bullets(self):
        # 例：近づく敵なので攻撃しない、または後で火の玉追加可
        pass

    def update(self):
        if self.is_on_cooldown:
            self.cooldown_timer -= 1
            if self.cooldown_timer <= 0:
                self.is_on_cooldown = False
            return  # ← 動かない
        self.update_counter += 1

        # 指定フレームごとに方向を更新（追尾）
        if self.update_counter >= self.update_interval:
            target_pos = pygame.math.Vector2(self.get_player_pos())
            direction = target_pos - self.pos
            if direction.length_squared() > 0:
                self.direction = direction.normalize()
            else:
                self.direction.update(0, 0)
            self.update_counter = 0

        # 移動処理
        self.move()
        #座標を出力
        #print(f"ChaseEnemy Position: {self.pos.x}, {self.pos.y}")
        #playerとの距離を出力
        player_pos = pygame.math.Vector2(self.get_player_pos())
        distance = (player_pos - self.pos).length()
        #print(f"Distance to Player: {distance}")
        
    def trigger_cooldown(self, frames=120):
        """敵を一定時間行動不能（移動停止）にする"""
        self.is_on_cooldown = True
        self.cooldown_timer = frames
