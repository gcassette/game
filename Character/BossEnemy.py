import pygame
import math
import random
from Character.Character import Character
from Weapon.ProjectileType import Projectile  # 自作のProjectile型を使ってる前提

IMG_BOSS = 'assets//gachigire.png'

class BossEnemy(Character):
    def __init__(self, screen, all_sprites, enemy_projectiles, get_player_pos):
        start_pos = (780, 300)  # 画面右端に出現
        super().__init__(IMG_BOSS, start_pos, all_sprites, enemy_projectiles, speed=1.5, max_hp=30)

        self.screen = screen
        self.get_player_pos = get_player_pos

        self.direction = pygame.math.Vector2(0, 1)
        self.move_range = 150  # 移動範囲の縦幅
        self.move_timer = 0
        self.move_interval = 60  # 1秒に1回方向反転（60fps前提）

        self.shoot_timer = 0
        self.shoot_interval = 90  # ホーミング弾を1.5秒ごとに撃つ
    def set_bullets(self):
        pass  # 今は攻撃に直接 FireBall を使っているので空でOK

    def update(self):
        # 上下に往復移動
        self.move_timer += 1
        if self.move_timer >= self.move_interval:
            self.direction.y *= -1
            self.move_timer = 0
        self.move()

        # 攻撃タイマー処理
        self.shoot_timer += 1
        if self.shoot_timer >= self.shoot_interval:
            self.shoot_timer = 0
            self.fire_homing()

    def fire_homing(self):
        """choose_move_directionを用いたホーミング弾の発射"""
        player_pos = pygame.math.Vector2(self.get_player_pos())
        # move_dx, move_dy = self.choose_move_direction(
        #     x=self.pos.x,
        #     y=self.pos.y,
        #     px=player_pos.x,
        #     py=player_pos.y,
        #     dx=1.0, dy=0.0,
        #     sigma=150.0, t=1.0,
        #     step=1.0
        # )
        bullet_pos = self.pos.xy  # ボスの現在位置をコピー

        homing = HomingFireball(
            lambda: pygame.math.Vector2(bullet_pos),  # 発射時点の位置を固定コピー
            lambda: pygame.math.Vector2(1, 0),
            self.screen,
            self.get_player_pos
        )
        homing.drawing_shoot()
        self.weapon.projectiles_group.add(homing)
        self.weapon.all_sprites.add(homing)

    # def choose_move_direction(self, x, y, px, py, dx, dy, sigma=100.0, t=1.0, step=1.0):
    #     directions = [
    #         (1, 0), (-1, 0), (0, 1), (0, -1),
    #         (1, 1), (1, -1), (-1, 1), (-1, -1)
    #     ]

    #     def f_modified(x, y, px, py, dx, dy, sigma, t):
    #         rx, ry = x - px, y - py
    #         r_len = math.hypot(rx, ry)
    #         w = math.exp(-r_len ** 2 / (sigma ** 2))
    #         d_len = math.hypot(dx, dy)
    #         cos_theta = (rx * dx + ry * dy) / (r_len * d_len + 1e-8)
    #         b = math.exp(-((cos_theta + 1) ** 2) / (2 * 0.4 ** 2))
    #         return w * b

    #     best_f = float('-inf')
    #     best_dir = (0, 0)
    #     for dx_step, dy_step in directions:
    #         nx = x + dx_step * step
    #         ny = y + dy_step * step
    #         val = f_modified(nx, ny, px, py, dx, dy, sigma, t)
    #         if val > best_f:
    #             best_f = val
    #             best_dir = (dx_step, dy_step)

    #     length = math.hypot(*best_dir)
    #     return (best_dir[0] / length, best_dir[1] / length) if length else (0.0, 0.0)


import pygame
import math
from Weapon.ProjectileType import Projectile

class HomingFireball(Projectile):
    SIZE = (12, 12)
    COLOR = (255, 0, 100)  # 赤紫系
    SPRITE_COORDINATE = (6, 6)
    SPRITE_RADIUS = 6

    def __init__(self, get_position_func, shoot_direction, screen, get_player_pos):
        super().__init__("HomingFire", get_position_func, shoot_direction, screen)
        self.SPEED = 4
        self.get_player_pos = get_player_pos
        self.pos = pygame.math.Vector2(0, 0)  # 初期化
        self.velocity = pygame.math.Vector2(0, 0)

    def create_image(self) -> pygame.Surface:
        image = pygame.Surface(self.SIZE, pygame.SRCALPHA)
        image.fill(self.COLOR)
        #pygame.draw.circle(image, (255, 255, 0), self.SPRITE_COORDINATE, self.SPRITE_RADIUS)  # 弾本体を黄色に
        pygame.draw.circle(image, self.COLOR, self.SPRITE_COORDINATE, self.SPRITE_RADIUS)
        print("create_bbimage")
        return image

    def clone(self) -> Projectile:
        return HomingFireball(self.get_position, self.shoot_direction, self.screen, self.get_player_pos)

    def drawing_shoot(self):
        self.enable = True
        self.pos = self.get_position()
        self.image = self.create_image()
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.velocity = pygame.math.Vector2(0, 0)  # 初期は静止、次の update で追尾
        self.beam_sound.play()

    def update(self):
        if not self.enable:
            return



        # プレイヤーを追いかける向きを毎フレーム計算
        player_pos = self.get_player_pos()
        move_dx, move_dy = self.choose_move_direction(
            x=self.pos.x, y=self.pos.y,
            px=player_pos.x, py=player_pos.y,
            dx=1.0, dy=0.0, sigma=100.0, t=1.0, step=1.0
        )
        self.velocity = pygame.math.Vector2(move_dx, move_dy) * self.SPEED

        self.pos += self.velocity
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        if not self.screen.get_rect().colliderect(self.rect):
            self.kill()

    def choose_move_direction(self, x, y, px, py, dx, dy, sigma=100.0, t=1.0, step=1.0):
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

        def f_modified(x, y, px, py, dx, dy, sigma, t):
            rx, ry = x - px, y - py
            r_len = math.hypot(rx, ry)
            w = math.exp(-r_len ** 2 / (sigma ** 2))
            d_len = math.hypot(dx, dy)
            cos_theta = (rx * dx + ry * dy) / (r_len * d_len + 1e-8)
            b = math.exp(-((cos_theta + 1) ** 2) / (2 * 0.4 ** 2))
            return w * b

        best_f = float('-inf')
        best_dir = (0, 0)
        for dx_step, dy_step in directions:
            nx = x + dx_step * step
            ny = y + dy_step * step
            val = f_modified(nx, ny, px, py, dx, dy, sigma, t)
            if val > best_f:
                best_f = val
                best_dir = (dx_step, dy_step)

        length = math.hypot(*best_dir)
        return (best_dir[0] / length, best_dir[1] / length) if length else (0.0, 0.0)
