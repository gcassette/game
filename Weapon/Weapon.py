from Weapon.ProjectileType import Projectile

class Weapon:
    def __init__(self, all_sprites, projectiles_group):
        self.all_sprites = all_sprites
        self.projectiles_group = projectiles_group
        self.bullets: list[Projectile] = []

    def resister_bullet(self, bullet: Projectile):
        self.bullets.append(bullet)

    def shoot(self, bullet_number=0):
        bullet_type: Projectile = self.bullets[bullet_number]
        bullet: Projectile = bullet_type.clone()  # ここでbulletを複製 & 参照切り
        self.all_sprites.add(bullet)
        self.projectiles_group.add(bullet)
        bullet.drawing_shoot()
