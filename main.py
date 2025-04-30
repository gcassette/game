import pygame
import math
from Enemy import Enemy

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BULLET_SPEED = 10
ROTATE_SPEED = 3  # 回転速度（度単位）
screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load('assets//robot.png').convert_alpha()
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 1
        self.angle = 0  # 向いている角度（度）
        self.direction = pygame.math.Vector2(0, 0)  # 移動方向はキー入力に基づく

    def update(self):
        keys = pygame.key.get_pressed()

        # 回転処理（W/Sキー）
        if keys[pygame.K_w]:
            self.angle += ROTATE_SPEED
        if keys[pygame.K_s]:
            self.angle -= ROTATE_SPEED

        # 移動処理（矢印キー）
        self.direction.x = 0
        self.direction.y = 0

        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.direction.x = 1

        if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
            self.direction.y = 1

        if self.direction.length() != 0:
            self.direction = self.direction.normalize()

        self.pos += self.direction * self.speed
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        # 画面内制限
        #screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.rect.clamp_ip(screen_rect)
        self.pos.x = max(0, min(SCREEN_WIDTH, self.pos.x))
        self.pos.y = max(0, min(SCREEN_HEIGHT, self.pos.y))

        # 回転画像の再描画（angleだけに基づく）
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def shoot(self):
        bullet = Bullet(self.rect.center, self.angle)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        self.velocity = pygame.math.Vector2(
            math.cos(math.radians(angle)),
            -math.sin(math.radians(angle))
        ) * BULLET_SPEED

    def update(self):
        self.pos += self.velocity
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        if not screen_rect.colliderect(self.rect):
            self.kill()
# Initialization
pygame.init()
font = pygame.font.SysFont(None, 36)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hello Pygame")

all_sprites = pygame.sprite.Group()
spriteEneies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
enemy = Enemy(screen)
all_sprites.add(player)
spriteEneies.add(enemy)
all_sprites.add(spriteEneies)

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.shoot()
        if event.type == Enemy.ENEMY_RETREAT_EVENT:
            enemy.exit()

    all_sprites.update()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    #direction_text = font.render(f"Angle: {player.angle:.2f}", True, (255, 255, 0))
    #screen.blit(direction_text, (10, 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()