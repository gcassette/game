import pygame
from Character.Player import Player
from Character.Enemy import Enemy
from Character.WanderEnemy import WanderEnemy
from Life import Life
from Background import Background
import SpriteGroups.EnemyProjectile


SCREEN_WIDTH, SCREEN_HEIGHT = 800, 585
screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT) 
TIME_LIMIT = 300

# Initialization
pygame.init()
font = pygame.font.SysFont(None, 36)
japanese_font = pygame.font.Font('assets/BestTen-DOT.otf', 50)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("カルシウム王子の冒険")
pygame.mixer.init()
pygame.mixer.music.load("assets/\u571f\u661f\u30c0\u30f3\u30b9.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.02)
damage_sound = pygame.mixer.Sound("assets/レトロアクション_3.mp3")
damage_sound.set_volume(0.05)
clock = pygame.time.Clock()

running = True
state = 'title_init'
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == 'playing':
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.shoot()
        elif state == 'title':
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                state = "level_init"  # Start the game     

    if state == 'playing':
        all_sprites.update()
        background.update()
        background.draw(screen)
        all_sprites.draw(screen)

        #direction_text = font.render(f"Angle: {player.angle:.2f}", True, (255, 255, 0))
        #screen.blit(direction_text, (10, 30))

        # Calculate the time elapsed
        elapsed_ms = pygame.time.get_ticks()
        elapsed_sec = elapsed_ms // 1000
        time_ramaining = TIME_LIMIT - elapsed_sec + level_start_time
        timer_text = font.render(f"Time: {time_ramaining}s", True, (255, 255, 255))
        # --- 衝突判定 ---

        # Player と 敵本体の当たり判定
        if pygame.sprite.spritecollide(player, enemies, False, collided=pygame.sprite.collide_rect):
            player_life.lose_life()
            damage_sound.play()

        # Player と Fireball の当たり判定
        if pygame.sprite.spritecollide(player, enemy_projectiles, True, collided=pygame.sprite.collide_rect):
            player_life.lose_life()
            damage_sound.play()

        # WanderEnemy と bullets の当たり判定
        # wander_enemy と bullets の当たり判定
        if pygame.sprite.spritecollide(wander_enemy, bullets, True, collided=pygame.sprite.collide_rect):
            wander_enemy.take_damage()

            if wander_enemy.hp <= 0:
                wander_enemy.kill()

        # ライフが0になったらゲーム終了
        if player_life.current_lives <= 0:
            print("ゲームオーバー")
            state = 'title_init'


        screen.blit(timer_text, (650, 10))

        player_life.draw(screen)

        all_sprites.update()
        all_sprites.draw(screen)

    elif state == 'title':      # display title
        screen.blit(bg_title, (0,0))    # background image
        title_text = japanese_font.render("カルシウム王子の冒険", True, (0, 0, 0))
        # prompt_text = font.render("Press SPACE to Start", True, (0, 0, 0))
        screen.blit(title_text, title_text.get_rect(center=(400, 50)))
        # screen.blit(prompt_text, prompt_text.get_rect(center=(400, 350)))

        if (pygame.time.get_ticks() % 1000 - 500) < 0: #display image in turn every .5 sec
            screen.blit(calcium_1,(300,70))
        else:
            screen.blit(calcium_2,(300,70))

    elif state == 'title_init': # initialize title screen
        bg_title = pygame.image.load('assets/bg_title.png').convert()
        calcium_1 = pygame.image.load("assets/calcium_title_1.png").convert_alpha()
        calcium_2 = pygame.image.load("assets/calcium_title_2.png").convert_alpha()
        state = 'title'

    elif state == 'level_init': # initialize game screen
        player_life = Life(max_lives=5)
        background = Background(SCREEN_WIDTH, SCREEN_WIDTH, scroll_speed=1)

        all_sprites = pygame.sprite.Group()
        sprite_enemies = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        enemy_projectiles = pygame.sprite.Group()

        ene_pro_manager = SpriteGroups.EnemyProjectile.EnemyProjectileManager(all_sprites, enemy_projectiles)

        player = Player(screen, all_sprites)
        enemy = Enemy(screen, ene_pro_manager)
        wander_enemy = WanderEnemy(screen, ene_pro_manager)

        enemies = pygame.sprite.Group()  # ← ここ追加
        all_sprites.add(player)
        all_sprites.add(enemy)
        all_sprites.add(wander_enemy)

        all_sprites.add(sprite_enemies)

        level_start_time = pygame.time.get_ticks() // 1000  #define the level time started

        state = 'playing'

    pygame.display.flip()
    clock.tick(60)

pygame.quit()