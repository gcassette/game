import pygame
<<<<<<< Updated upstream
=======
import math
from Enemy import Enemy
from Life import Life

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BULLET_SPEED = 10
ROTATE_SPEED = 3  # 回転速度（度単位）
screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
time_limit = 300
>>>>>>> Stashed changes

# Define our square object and call super to
# give it all the properties and methods of pygame.sprite.Sprite
# Define the class for our square objects
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
<<<<<<< Updated upstream
        self.image = pygame.image.load('assets//robot.png').convert_alpha()
=======
        self.original_image = pygame.image.load('assets//calcium.png').convert_alpha()
        self.image = self.original_image.copy()
>>>>>>> Stashed changes
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
        self.speed_x = 0
        self.speed_y = 0
    def update(self):
        keys = pygame.key.get_pressed()
        
        self.speed_x = 0
        self.speed_y = 0
        
        if keys[pygame.K_LEFT]:
            self.speed_x = -1
        if keys[pygame.K_RIGHT]:
            self.speed_x = 1
        if keys[pygame.K_UP]:
            self.speed_y = -1
        if keys[pygame.K_DOWN]:
            self.speed_y = 1
            
        # Update position
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Keep inside window
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 600

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Hello Pygame")

<<<<<<< Updated upstream
=======
# Create Life instance
player_life = Life(heart_image_path="assets//heart.png", max_lives=5, position=(10, 10))
player_life.gain_life()
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()

>>>>>>> Stashed changes
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Game loop
running = True

# clock = pygame.time.Clock()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
<<<<<<< Updated upstream
    # Update the display using flip
=======

    #direction_text = font.render(f"Angle: {player.angle:.2f}", True, (255, 255, 0))
    #screen.blit(direction_text, (10, 30))


    # Calculate the time elapsed
    elapsed_ms = pygame.time.get_ticks()
    elapsed_sec = elapsed_ms // 1000
    time_ramaining = time_limit - elapsed_sec
    timer_text = font.render(f"Time: {time_ramaining}s", True, (255, 255, 255))

    screen.blit(timer_text, (650, 10))

    player_life.draw(screen)

>>>>>>> Stashed changes
    pygame.display.flip()

# Quit Pygame
pygame.quit()