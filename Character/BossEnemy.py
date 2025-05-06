import pygame
import math
import random
from Character.Character import Character
from Weapon.ProjectileType import Projectile  # 自作のProjectile型を使ってる前提



IMG_BOSS = 'assets//gachigire.png'

class BossEnemy(Character):
    def __init__(self, screen, all_sprites, enemy_projectiles, get_player_pos):
        start_pos = (600, 300)  # 画面右端に出現
        super().__init__(IMG_BOSS, start_pos, all_sprites, enemy_projectiles, speed=1.5, max_hp=30)


        self.screen = screen
        self.get_player_pos = get_player_pos

        self.direction = pygame.math.Vector2(0, 1)
        self.move_range = 150  # 移動範囲の縦幅
        self.move_timer = 0
        self.move_interval = 60  # 1秒に1回方向反転（60fps前提）

        self.shoot_timer = 0
        self.shoot_interval = 90  # ホーミング弾を1.5秒ごとに撃つ

        self.shoot_timer2 = 0
        self.shoot_interval2 = 150  # 直進弾の発射間隔（調整可）

        # self.tank_group = tank_group  # 戦車グループ
        self.summon_timer = 0
        self.summon_interval = 300  # 5秒ごとに戦車召喚（60FPS前提）


        mask_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
        pygame.draw.circle(mask_surface, (255, 255, 255), self.image.get_rect().center, 30)
        self.mask = pygame.mask.from_surface(mask_surface)


    def set_bullets(self):
        pass  # 今は攻撃に直接 FireBall を使っているので空でOK

    def update(self):
        player_pos = self.get_player_pos()

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

        # 直進弾は HP が半分以下のときのみ使用
        if self.hp <= self.max_hp / 2:
            self.shoot_timer2 += 1
            if self.shoot_timer2 >= self.shoot_interval2:
                self.shoot_timer2 = 0
                self.fire_straight()


    def fire_homing(self):
        bullet_pos = self.pos.xy
        direction_to_player = (self.get_player_pos() - self.pos).normalize()

        homing = HomingFireball(
            lambda: pygame.math.Vector2(bullet_pos),                     # 発射位置を固定コピー
            lambda: direction_to_player,                                 # 初期向き = プレイヤーへの向き
            self.screen,
            self.get_player_pos
        )
        homing.drawing_shoot()
        self.weapon.projectiles_group.add(homing)
        self.weapon.all_sprites.add(homing)

    def fire_straight(self):
        bullet_pos = self.pos.xy
        direction = (self.get_player_pos() - self.pos).normalize()

        straight = StraightFireball(
            lambda: pygame.math.Vector2(bullet_pos),
            lambda: direction,
            self.screen
        )
        straight.drawing_shoot()
        self.weapon.projectiles_group.add(straight)
        self.weapon.all_sprites.add(straight)


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
        self.has_avoided = False
        self.avoid_direction = None  # 回り込み成功後の固定方向

        


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

        player_pos = self.get_player_pos()
        current_dir = self.velocity.normalize() if self.velocity.length_squared() > 0 else pygame.math.Vector2(1, 0)
        direction_to_player = (player_pos - self.pos).normalize()

        if not self.has_avoided:
            vec_from_player = self.pos - player_pos
            vec_from_player = vec_from_player.normalize()
            player_forward = pygame.math.Vector2(1, 0)

            cos_theta = player_forward.dot(vec_from_player)
            distance = (self.pos - player_pos).length()

            print(f"[DEBUG] cosθ: {cos_theta:.3f}, Player→Bullet dist: {distance:.2f}, BulletPos: {self.pos}, PlayerPos: {player_pos}")

            if cos_theta < -0.8:
                self.has_avoided = True
                self.avoid_direction = (player_pos - self.pos).normalize()
                print("[DEBUG] 回り込み成功 -> 突進モード移行")

        # 動作切り替え
        if self.has_avoided:
            self.velocity = self.avoid_direction * self.SPEED  # ← 固定方向に直進
        else:
            desired_dir = self.choose_around_direction(self.pos, player_pos, current_dir)
            self.velocity = (self.velocity * 0.85 + desired_dir * 0.15).normalize() * self.SPEED


        self.pos += self.velocity
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        if not self.screen.get_rect().colliderect(self.rect):
            self.kill()





    def choose_around_direction(self, pos, target, forward_dir, epsilon=1.0):
        """
        pos: 現在の位置（Vector2）
        target: プレイヤー位置（Vector2）
        forward_dir: 現在の進行方向（Vector2）
        epsilon: 微小変化量（勾配の差分ステップ）
        """



        def potential(p):
            fake_target = target  # ← 参照点を左にズラす
            to_player = fake_target - p
            dist = to_player.length()
            if dist == 0:
                return -float('inf')

            to_player_norm = to_player.normalize()
            forward_norm = forward_dir.normalize()

            # 距離に応じた重み: 理想距離で最大、それより近くても遠くても減少
            dist_opt = 200   # 理想的な接近距離（要調整）
            sigma = 50       # 鋭さ（広がり）
            w1 = math.exp(-((dist - dist_opt) ** 2) / (2 * sigma ** 2))

            # 正面回避（正面 cosθ ≒ 1 → スコア小、背面 cosθ ≒ -1 → スコア大）
            cos_theta = forward_norm.dot(to_player_norm)
            w2 = math.exp(-((cos_theta + 1) ** 2) / (2 * 0.4 ** 2))

            return w1 * w2
        dx = (potential(pos + pygame.math.Vector2(epsilon, 0)) - potential(pos - pygame.math.Vector2(epsilon, 0))) / (2 * epsilon)
        dy = (potential(pos + pygame.math.Vector2(0, epsilon)) - potential(pos - pygame.math.Vector2(0, epsilon))) / (2 * epsilon)

        grad = pygame.math.Vector2(dx, dy)

        if grad.length_squared() == 0:
            return forward_dir.normalize()
        else:
            return grad.normalize()
        


class StraightFireball(Projectile):
    SIZE = (12, 12)
    COLOR = (255, 255, 0)  # 黄色
    SPRITE_COORDINATE = (6, 6)
    SPRITE_RADIUS = 6

    def __init__(self, get_position_func, shoot_direction, screen,speed = 2.5):
        super().__init__("StraightFire", get_position_func, shoot_direction, screen)
        self.SPEED = speed
        self.pos = pygame.math.Vector2(0, 0)
        self.velocity = pygame.math.Vector2(0, 0)

    def create_image(self) -> pygame.Surface:
        image = pygame.Surface(self.SIZE, pygame.SRCALPHA)
        pygame.draw.circle(image, self.COLOR, self.SPRITE_COORDINATE, self.SPRITE_RADIUS)
        return image

    def clone(self) -> Projectile:
        return StraightFireball(self.get_position, self.shoot_direction, self.screen)

    def drawing_shoot(self):
        self.enable = True
        self.pos = self.get_position()
        self.image = self.create_image()
        self.rect = self.image.get_rect(center=self.pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.velocity = self.shoot_direction().normalize() * self.SPEED
        self.beam_sound.play()

    def update(self):
        if not self.enable:
            return

        self.pos += self.velocity
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        if not self.screen.get_rect().colliderect(self.rect):
            self.kill()



