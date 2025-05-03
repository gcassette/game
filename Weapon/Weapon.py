from Weapon.ProjectileType import Projectile

class Weapon:
    def __init__(self, projectiles_group):
        super().__init__()
        self.prj_group = projectiles_group
        self.bullets: list[Projectile] = []

    def resister_bullet(self, bullet: Projectile):
        self.bullets.append(bullet)

    def shoot(self, bullet_number=0):
        bullet_type: Projectile = self.bullets[bullet_number]
        bullet: Projectile = bullet_type.clone()  # ここでbulletを複製 & 参照切り
        self.prj_group.add(bullet)
        bullet.drawing_shoot()
