class EnemyProjectileManager:
    def __init__(self, all_sprites, projectiles_group):
        self.all_sprites = all_sprites
        self.projectiles_group = projectiles_group

    def add(self, bullet):
        self.all_sprites.add(bullet)
        self.projectiles_group.add(bullet)
