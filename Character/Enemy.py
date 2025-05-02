import pygame
import Weapon.ProjectileType as ProjectileType
from Character.Character import Character

IMG_Enemy = "Assets\\skull.png"

ENEMY_SPEED = 3.0
DISTANCE_ARRIVAL_PERMISSION = 5.0

FPS = 60

class Enemy(Character):
    def __init__(self, screen, projectiles_manager):
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        self.screen = screen

        self.attack_pos = pygame.math.Vector2(screen_width / 2, screen_height / 2)
        self.exit_pos = pygame.math.Vector2(screen_width / 2, -100)
        self.phase = "entry"
        self.script = self.behavior_script()
        super().__init__(IMG_Enemy, (screen_width + 10, screen_height / 2), projectiles_manager, speed=ENEMY_SPEED)
        
        next(self.script)

    def set_target(self, target):
        self.direction = (target - self.pos)
        distance = self.direction.length()
        if distance != 0:
            self.direction = self.direction.normalize() * self.speed
        else:
            self.direction.update(0, 0)
        self.target_pos = target

    def update(self):
        try:
            next(self.script)
        except StopIteration:
            pass

    def behavior_script(self):
        self.phase = "entry"
        self.set_target(self.attack_pos)
        while not self.is_arrived():
            self.move()
            yield

        self.phase = "attack"
        self.direction.update(0, 0)
        yield from self.wait_frames(FPS * 2)

        self.phase = "exit"
        self.set_target(self.exit_pos)
        while not self.is_arrived():
            self.move()
            yield

        self.kill()

    def wait_frames(self, frames):
        for _ in range(frames):
            yield

    def is_arrived(self):
        return (self.target_pos - self.pos).length() <= DISTANCE_ARRIVAL_PERMISSION
    
    def shoot(self):
        self.weapon.shoot()
    
    def set_bullets(self):
        bullet_type = ProjectileType.BulletLinerly(lambda: self.rect.center, lambda: self.direction, self.screen)
        self.weapon.resister_bullet(bullet_type)
"""
class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.image = pygame.image.load(IMG_Enemy).convert_alpha()
        self.rect = self.image.get_rect()
        self.screen = screen

        self.angle = 0
        self.speed = 3.0
        self.vx = 0
        self.vy = 0
        self.distance = 0.0

        self.appearancePosition = (self.screen.get_width() + 10, self.screen.get_height() / 2)
        self.attackPosition = (self.screen.get_width() / 2, self.screen.get_height() / 2)
        self.dissapearancePosition = (self.screen.get_width() / 2, -100)

        self.target_pos = None
        self.rect.center = self.appearancePosition

        #所持武器一覧
        self.weapon = Weapon(lambda: self.rect.center, self.angle, self.screen)

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

    def shoot(self, all_sprites, bullets_sprites_group):
        self.weapon.shoot(all_sprites, bullets_sprites_group)
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        """