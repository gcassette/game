import pygame
import math
from Player import Player
from Enemy import Enemy


SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

# Initialization
pygame.init()
font = pygame.font.SysFont(None, 36)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hello Pygame")

all_sprites = pygame.sprite.Group()
spriteEneies = pygame.sprite.Group()
sprites_bullets = pygame.sprite.Group()

player = Player(screen)
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
            player.shoot(all_sprites, sprites_bullets)

    all_sprites.update()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    #direction_text = font.render(f"Angle: {player.angle:.2f}", True, (255, 255, 0))
    #screen.blit(direction_text, (10, 30))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()