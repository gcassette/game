import pygame
import math
from Life import Life
from Background import Background

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 585
BULLET_SPEED = 10
ROTATE_SPEED = 3
ENEMY_SPEED = 3.0
FPS = 60
DISTANCE_ARRIVAL_PERMISSION = 5.0
TIME_LIMIT = 300

screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

class Character(pygame.sprite.Sprite):
    def __init__(self, image_path, start_pos, speed=1):
        super().__init__()
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = self.original_image.copy()
        #characterのscreen上の位置をrectで管理する、
        self.rect = self.image.get_rect(center=start_pos)
        #characterの本当の位置をposで管理する、
        self.pos = pygame.math.Vector2(self.rect.center)
        #directionは移動方向を表すベクトル、speedは移動速度を表す。characterの移動距離はspeed * directionで決まる。
        self.speed = speed
        self.direction = pygame.math.Vector2(0, 0)


    def move(self):
        #directionは移動方向を表すベクトルのため正規化を行い、長さを1にする。
        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()
        else:
            self.direction.update(0, 0)
        self.pos += self.direction * self.speed
        self.rect.center = (round(self.pos.x), round(self.pos.y))
        

class Player(Character):
    def __init__(self):
        super().__init__('assets//calcium.png', (400, 300), speed=1)
        self.angle = 0
    def move(self):
        super().move()  # Characterのmove()を呼び出し

        # 画面内に制限する処理だけを追加
        self.rect.clamp_ip(screen_rect)
        self.pos.x = max(0, min(SCREEN_WIDTH, self.pos.x))
        self.pos.y = max(0, min(SCREEN_HEIGHT, self.pos.y))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.angle += ROTATE_SPEED
        if keys[pygame.K_s]:
            self.angle -= ROTATE_SPEED

        self.direction.update(0, 0)
        if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.direction.x = 1

        if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
            self.direction.y = 1

        self.move()
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def shoot(self):
        bullet = Bullet(self.rect.center, self.angle)
        all_sprites.add(bullet)
        bullets.add(bullet)
        beam_sound.play()

class Enemy(Character):
    def __init__(self):
        super().__init__('assets//enemy_sake.png', (SCREEN_WIDTH + 10, SCREEN_HEIGHT / 2), speed=ENEMY_SPEED)
        self.attack_pos = pygame.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.exit_pos = pygame.math.Vector2(SCREEN_WIDTH / 2, -100)
        self.phase = "entry"
        self.script = self.behavior_script()
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
pygame.mixer.init()
pygame.mixer.music.load("assets/\u571f\u661f\u30c0\u30f3\u30b9.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.05)
beam_sound = pygame.mixer.Sound("assets/\u30d3\u30fc\u30e0\u97f3.mp3")
beam_sound.set_volume(0.05)
player_life = Life(max_lives=5)
background = Background(SCREEN_WIDTH, SCREEN_WIDTH, scroll_speed=1)

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
enemy = Enemy()
all_sprites.add(player)
all_sprites.add(enemy)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.shoot()

    background.update()
    background.draw(screen)

    all_sprites.update()
    all_sprites.draw(screen)

    # Calculate the time elapsed
    elapsed_ms = pygame.time.get_ticks()
    elapsed_sec = elapsed_ms // 1000
    time_ramaining = TIME_LIMIT - elapsed_sec
    timer_text = font.render(f"Time: {time_ramaining}s", True, (255, 255, 255))

    screen.blit(timer_text, (650, 10))

    player_life.draw(screen)

    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
