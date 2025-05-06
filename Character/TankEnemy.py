import pygame

IMG_TANK = 'assets//train.png'  # 適切な画像に差し替えてください

class Tank(pygame.sprite.Sprite):
    def __init__(self, screen, all_sprites, tank_group, start_pos=(50, 50), speed=2):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load(IMG_TANK).convert_alpha()
        self.rect = self.image.get_rect(topleft=start_pos)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = speed
        self.hp = 10
        self.tank_group = tank_group  # 他の戦車グループ
        all_sprites.add(self)
        tank_group.add(self)

    def update(self):
        # 下に落ち続ける
        self.pos.y += self.speed
        self.rect.topleft = self.pos

        screen_bottom = self.screen.get_height()

        # 地面 or 他戦車との衝突チェック
        collided = False
        for tank in self.tank_group:
            if tank == self:
                continue
            if self.rect.colliderect(tank.rect):
                self.pos.y = tank.rect.top - self.rect.height
                collided = True
                break

        if self.rect.bottom >= screen_bottom:
            self.pos.y = screen_bottom - self.rect.height
            collided = True

        # 止まる
        if collided:
            self.speed = 0

        self.rect.topleft = self.pos
