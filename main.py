import pygame
import math

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets//robot.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
        self.pos = pygame.math.Vector2(self.rect.center)  # 小数位置管理
        self.speed = 1
        self.direction = pygame.math.Vector2(0, 0)
        self.move_x = 0
        self.move_y = 0
        self.total_move_x = 0
        self.total_move_y = 0

    def update(self):
        keys = pygame.key.get_pressed()

        # 移動前座標は小数で保存
        old_x, old_y = self.pos.x, self.pos.y

        self.direction.x = 0
        self.direction.y = 0
        
        # 左右キーの排他処理
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        # 上下キーの排他処理
        if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if self.direction.length() != 0:
            self.direction = self.direction.normalize()

        self.pos += self.direction * self.speed
        self.rect.center = (round(self.pos.x), round(self.pos.y))

        screen_rect = pygame.Rect(0, 0, 800, 600)
        self.rect.clamp_ip(screen_rect)
        
        # --- 小数位置のまま画面内に収める ---
        self.pos.x = max(0, min(800, self.pos.x))
        self.pos.y = max(0, min(600, self.pos.y))

        new_x, new_y = self.pos.x, self.pos.y  # ここも小数！

        self.move_x = new_x - old_x
        self.move_y = new_y - old_y

        self.total_move_x += abs(self.move_x)
        self.total_move_y += abs(self.move_y)

# Initialize Pygame
pygame.init()
font = pygame.font.SysFont(None, 36)

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Hello Pygame")

player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    # --- 移動距離を画面に出す ---
    move_text = font.render(f"Move x: {player.move_x:.2f}, y: {player.move_y:.2f}", True, (0, 255, 0))
    direction_text = font.render(f"Direction x: {player.direction.x:.2f}, y: {player.direction.y:.2f}", True, (255, 255, 0))
    total_move_text = font.render(f"Total Move x: {player.total_move_x:.2f}, y: {player.total_move_y:.2f}", True, (0, 0, 255))

    screen.blit(move_text, (10, 30))         # 1行目
    screen.blit(direction_text, (10, 70))     # 2行目
    screen.blit(total_move_text, (10, 110))   # 3行目

    pygame.display.flip()

pygame.quit()
