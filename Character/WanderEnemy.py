import pygame
import random
import Weapon.ProjectileType as ProjectileType
from Character.Character import Character

IMG_WEnemy = 'assets//enemy_sake.png'

class WanderEnemy(Character):
    def __init__(self, screen, projectiles_manager):
        self.screen = screen
        super().__init__(IMG_WEnemy, (random.randint(100, 700), random.randint(100, 500)), projectiles_manager, speed=2.0, max_hp=2)
        
        self.phase = "wander"
        self.wait_counter = 0
        self.move_counter = 0
        self.max_move_frames = 60
        self.max_wait_frames = 30
        self.set_random_direction()
        self.fireball_timer = 0
        self.fireball_interval = 90  # 1.5秒ごと（FPS=60前提）
        self.facing_left = True  # 左右反転状態を記録する変数

    def set_random_direction(self):
        directions = [
            pygame.math.Vector2(1, 0),   # 右
            pygame.math.Vector2(-1, 0),  # 左
            pygame.math.Vector2(0, 1),   # 下
            pygame.math.Vector2(0, -1)   # 上
        ]
        self.direction = random.choice(directions) * self.speed

    def set_bullets(self):
        bullet_type = ProjectileType.BulletLinerly(lambda: self.rect.center, lambda: self.direction, self.screen)
        self.weapon.resister_bullet(bullet_type)


    def update(self):
        if self.phase == "wander":
            self.move()
            self.move_counter += 1
            screen_rect = self.screen.get_rect()

            # 画面端に到達したら止まって方向転換準備
            if not screen_rect.contains(self.rect):
                self.rect.clamp_ip(screen_rect)
                self.phase = "wait"
                self.wait_counter = 0
                return

            if self.move_counter >= self.max_move_frames:
                self.phase = "wait"
                self.wait_counter = 0

        elif self.phase == "wait":
            self.wait_counter += 1
            if self.wait_counter >= self.max_wait_frames:
                self.set_random_direction()
                self.move_counter = 0
                self.phase = "wander"
         # 火の玉発射

         # 左右反転状態を記録
        if self.direction.x < 0:
            self.image = pygame.transform.flip(self.original_image, True, False)
            self.facing_left = False
        else:
            self.image = self.original_image.copy()
            self.facing_left = True

        self.fireball_timer += 1
        if self.fireball_timer >= self.fireball_interval:
            direction = pygame.math.Vector2(-1, 0) if self.facing_left else pygame.math.Vector2(1, 0)
            fireball = ProjectileType.Fireball(lambda: self.rect.center, lambda: direction, self.screen)
            self.weapon.shoot()
            self.fireball_timer = 0