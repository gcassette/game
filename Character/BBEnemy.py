import pygame
import random
from Character.Character import Character
import Weapon.ProjectileType as ProjectileType
import math
import numpy as np

IMG_CEnemy = 'assets//gachigire.png'

class BBEnemy(Character):
    def __init__(self, screen, all_sprites, enemy_projectiles, get_player_pos, update_interval=2400):
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
        self.last_print_time = 0  # ← 最後に出力した時刻（ミリ秒）

        # 初期位置はランダム
        start_pos = (random.randint(100, 700), random.randint(100, 500))
        super().__init__(IMG_CEnemy, start_pos, all_sprites, enemy_projectiles, speed=0.5, max_hp=3)

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

        # 一定フレームごとに方向更新（評価関数に基づいて）
        if self.update_counter >= self.update_interval:
            target_pos = pygame.math.Vector2(self.get_player_pos())

            distance = (target_pos - self.pos).length()  # ここを追加
            step = 1.0

            # 評価関数で次の方向を決める
            move_dx, move_dy = self.choose_move_direction(
                x=self.pos.x,
                y=self.pos.y,
                px=target_pos.x,
                py=target_pos.y,
                dx=1.0, dy=0.0,        # ターゲットの正面方向（ここでは右向き仮定）
                sigma=200.5,
                t=1.0,
                step=step             # 1回の移動評価ステップサイズ（ピクセル）
            )
            self.direction = pygame.math.Vector2(move_dx, move_dy)
            self.update_counter = 0
            
             # ★ 0.5秒ごとに出力（＝500ms）
            now = pygame.time.get_ticks()
            if now - self.last_print_time >= 500:
                print("move_dx,move_dy", move_dx, "  ", move_dy)
                self.last_print_time = now  # 次回用に記録

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



    # 評価関数（前述の修正版）
    def f_modified(self,x, y, px, py, dx, dy, sigma=1.0, t=0.5):
        rx = x - px
        ry = y - py
        r_len = math.hypot(rx, ry)
        w = math.exp(-r_len**2 / (sigma**2))

        d_len = math.hypot(dx, dy)
        dot = rx * dx + ry * dy
        cos_theta = dot / (r_len * d_len + 1e-8)

        # 背後（cosθ ≈ -1）を最大評価とするガウス型角度評価
        b = math.exp(-((cos_theta + 1)**2) / (2 * 0.4**2))  # μ = -1, σ = 0.4

        return w * b



    # 移動方向決定
    def choose_move_direction(self,x, y, px, py, dx, dy, sigma=10.0, t=1.0, step=0.1):
        # 8方向の移動候補
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

        best_f = float('-100')
        best_dir = (0, 0)

        for dx_step, dy_step in directions:
            nx = x + dx_step * step
            ny = y + dy_step * step
            val = self.f_modified(nx, ny, px, py, dx, dy, sigma, t)
            # if now - self.last_print_time >= 500:
            #     print("dx:",dx_step,"dy:",dy_step,"bestf - val:",best_f - val,"step:",step)
            if val > best_f:
                best_f = val
                best_dir = (dx_step, dy_step)

        # 正規化して単位ベクトルとして返す
        length = math.sqrt(best_dir[0]**2 + best_dir[1]**2)
        if length == 0:
            return (0.0, 0.0)
        return (best_dir[0]/length, best_dir[1]/length)

