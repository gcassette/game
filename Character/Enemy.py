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
