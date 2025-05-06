import pygame
from Character.Player import Player
from Character.Enemy import Enemy
from Character.WanderEnemy import WanderEnemy
from Character.ChaseEnemy import ChaseEnemy
from Character.LinearEnemy import LinearEnemy
from Character.BossEnemy import BossEnemy
from Character.TankEnemy import Tank
from Life import Life
from Background import Background
import SpriteGroups.EnemyProjectile

def generate_enemies(chase_enemy_num, linear_enemy_num, wander_enemy_num, bb_enemy_num):
    if chase_enemy_num:
        for i in range(chase_enemy_num):
            chase_enemy[i] = ChaseEnemy(screen, all_sprites, enemy_projectiles, lambda: player.pos, update_interval=120)
            enemies.add(chase_enemy[i])
    if chase_enemy_num:
        for i in range(linear_enemy_num):
            linear_enemy[i] = LinearEnemy(screen, all_sprites, enemy_projectiles, lambda: player.pos)
            enemies.add(linear_enemy[i])
    if wander_enemy_num:
        for i in range(wander_enemy_num):
            wander_enemy[i] = WanderEnemy(screen, all_sprites, enemy_projectiles,lambda: player.pos)
            enemies.add(wander_enemy[i])
    if bb_enemy_num:
        for i in range(bb_enemy_num):
            bb_enemy[i] = BossEnemy(screen, all_sprites, enemy_projectiles, lambda: player.pos)
            enemies.add(bb_enemy[i])


SCREEN_WIDTH, SCREEN_HEIGHT = 800, 585
screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT) 
TIME_LIMIT = 300

# Initialization
pygame.init()
font = pygame.font.SysFont(None, 36)
japanese_font = pygame.font.Font('assets/BestTen-DOT.otf', 25)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load("assets/calcium_icon.png").convert_alpha()
pygame.display.set_icon(icon)
pygame.display.set_caption("カルシウム王子の冒険")
pygame.mixer.init()
pygame.mixer.music.load("assets/\u571f\u661f\u30c0\u30f3\u30b9.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.02)
damage_sound = pygame.mixer.Sound("assets/レトロアクション_3.mp3")
damage_sound.set_volume(0.05)
enemy_damage_sound = pygame.mixer.Sound("assets/ショット命中.mp3")
enemy_damage_sound.set_volume(0.05)

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
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = 'pause_init'
        elif state == 'pause':
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = 'playing'
        elif state == 'title':
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                state = "level_init"  # Start the game     
        elif state == 'story':
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # Left mouse button released
                if next_button_rect.collidepoint(event.pos):
                    if scene == 'scene1':
                        scene = 'scene2'
                    elif scene == 'scene2':
                        scene = 'scene3'
                    elif scene == 'scene3':
                        scene = 'scene4'                        
                if scene == 'scene4' and play_button_rect.collidepoint(event.pos):
                    state = 'level_init'

    if state == 'playing':

        # レベル構成
        if wave_init:
            if wave == 1:
                generate_enemies(1,0,0,0)
            elif wave == 2:
                generate_enemies(1,0,0,0)
            elif wave == 3:       
                generate_enemies(5,0,0,0)
            elif wave == 4:
                generate_enemies(1,1,0,0)
            elif wave == 5:
                generate_enemies(2,3,0,0)
            elif wave == 6:
                generate_enemies(1,1,1,0)
            elif wave == 7:
                generate_enemies(1,2,3,0)
            elif wave == 8:
                generate_enemies(3,2,3,0)
            elif wave == 9:
                generate_enemies(0,0,0,1)
                boss_start_time = pygame.time.get_ticks() // 1000
                boss_flag = True
                background = Background(SCREEN_WIDTH, SCREEN_WIDTH, scroll_speed=1, image='assets/gachigire_castle.png')
            else:
                state = 'game_clear_init'

            all_sprites.add(enemies)
            print('wave' + str(wave))
            wave_init = False

        else:
            if not enemies:
                wave += 1
                wave_init = True


        #direction_text = font.render(f"Angle: {player.angle:.2f}", True, (255, 255, 0))
        #screen.blit(direction_text, (10, 30))

        # Calculate the time elapsed
        elapsed_ms = pygame.time.get_ticks()
        elapsed_sec = elapsed_ms // 1000
        time_ramaining = TIME_LIMIT - elapsed_sec + level_start_time
        timer_text = font.render(f"Time: {time_ramaining}s", True, (255, 255, 255))
        # --- 衝突判定 ---
        if collided_enemies := pygame.sprite.spritecollide(player, enemies, False, collided=pygame.sprite.collide_mask):
            if not player.invincible:
                player_life.lose_life()
                damage_sound.play()
                player.trigger_invincibility(duration_frames=300)
                print("Player hit by enemy!")

            for collided_enemy in collided_enemies:
                print(f"[DEBUG] Player pos: {player.pos}, Collided with {type(collided_enemy).__name__} at {collided_enemy.pos}")
                if isinstance(collided_enemy, ChaseEnemy):
                    collided_enemy.trigger_cooldown(frames=120)

        # --- プレイヤーと戦車の衝突判定 ---
        if collided_tanks := pygame.sprite.spritecollide(player, tanks, False, collided=pygame.sprite.collide_mask):
            if not player.invincible:
                player_life.lose_life()
                damage_sound.play()
                player.trigger_invincibility(duration_frames=300)
                print("Player hit by tank!")


        # Player と Fireball の当たり判定
        
        if collided_fireballs := pygame.sprite.spritecollide(player, enemy_projectiles, True, collided=pygame.sprite.collide_mask):
            player_life.lose_life()
            damage_sound.play()
        # 全ての敵と bullets の当たり判定
        for enemy in enemies:
            
            collided_bullets = pygame.sprite.spritecollide(enemy, bullets, True, collided=pygame.sprite.collide_mask)
            if collided_bullets:
                enemy.take_damage()
                enemy_damage_sound.play()
                print(f"Enemy {enemy} hit by bullet!")
                if enemy in bb_enemy: #ボスの残機管理
                    boss_life.lose_life()
                    if boss_life.current_lives > 19:
                        i = 30 - boss_life.current_lives - 1
                        tank_enemy.append(Tank(screen, all_sprites, tanks, start_pos=(50, 50 + i*60)))
                        tanks.add(tank_enemy[i])
                        all_sprites.add(tanks)

                if enemy.hp <= 0:
                    enemy.kill()



        # ライフが0になったらゲーム終了
        if player_life.current_lives <= 0:
            print("ゲームオーバー")
            state = 'game_over_init'

        all_sprites.update()
        background.update()
        background.draw(screen)
        all_sprites.draw(screen)

        screen.blit(timer_text, (650, 10))

        player_life.draw(screen)
        if boss_flag:
            boss_life.draw(screen)
            boss_life_caption = japanese_font.render('BOSS LIFE', True, (255, 255, 255))
            screen.blit(boss_life_caption, (390,430))
            print('tanks drawn')
            tanks.draw(screen)

    elif state == 'game_clear_init':
        GAME_CLEAR = pygame.image.load('assets/GAME_CLEAR.png').convert()
        title_button = pygame.image.load('assets/title_button.png').convert()
        title_button_hover = pygame.image.load('assets/title_button_hover.png').convert()
        title_button_rect = play_button.get_rect(center=(402, 530))
        state = 'game_clear'

    elif state == 'game_clear':
        screen.blit(GAME_CLEAR, (0,0))
        # play button
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if title_button_rect.collidepoint(mouse_pos):
            screen.blit(title_button_hover, title_button_rect)
            if mouse_click[0]:  # Left-click
                state = 'title_init'
        else:
            screen.blit(title_button, title_button_rect)

    elif state == 'game_over_init':
        GAME_OVER = pygame.image.load('assets/GAME_OVER.png').convert()
        title_button = pygame.image.load('assets/title_button.png').convert()
        title_button_hover = pygame.image.load('assets/title_button_hover.png').convert()
        title_button_rect = play_button.get_rect(center=(402, 530))
        state = 'game_over'

    elif state == 'game_over':
        screen.blit(GAME_OVER, (0,0))
        # play button
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if title_button_rect.collidepoint(mouse_pos):
            screen.blit(title_button_hover, title_button_rect)
            if mouse_click[0]:  # Left-click
                state = 'title_init'
        else:
            screen.blit(title_button, title_button_rect)

    elif state == 'title':      # display title
        screen.blit(bg_title, (0,0))    # background image

        if (pygame.time.get_ticks() % 1000 - 500) < 0: #display image in turn every .5 sec
            screen.blit(calcium_1,calcium_1.get_rect(center=(410,350)))
        else:
            screen.blit(calcium_2,calcium_2.get_rect(center=(410,350)))

        screen.blit(title_logo,title_logo.get_rect(center=(400,50)))   # title logo

        # play button
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if play_button_rect.collidepoint(mouse_pos):
            screen.blit(play_button_hover, play_button_rect)
            if mouse_click[0]:  # Left-click
                state = 'level_init'
        else:
            screen.blit(play_button, play_button_rect)

        if story_button_rect.collidepoint(mouse_pos):
            screen.blit(story_button_hover, story_button_rect)
            if mouse_click[0]:  # Left-click
                state = 'story_init'
        else:
            screen.blit(story_button, story_button_rect)

    elif state == 'title_init': # initialize title screen
        bg_title = pygame.image.load('assets/bg_title.png').convert()
        calcium_1 = pygame.image.load("assets/calcium_title_1.png").convert_alpha()
        calcium_2 = pygame.image.load("assets/calcium_title_2.png").convert_alpha()
        title_logo = pygame.image.load("assets/title_logo.png").convert_alpha()
        play_button = pygame.image.load("assets/play_button.png").convert_alpha()
        play_button_hover = pygame.image.load("assets/play_button_hover.png").convert_alpha()
        play_button_rect = play_button.get_rect(center=(402, 380))
        story_button = pygame.image.load("assets/story_button.png").convert_alpha()
        story_button_hover = pygame.image.load("assets/story_button_hover.png").convert_alpha()
        story_button_rect = story_button.get_rect(center=(402, 460))

        state = 'title'

    elif state == 'story_init':
        story_bg1 = pygame.image.load('assets/story_bg1.png').convert()
        story_bg2 = pygame.image.load('assets/story_bg2.png').convert()
        story_bg3 = pygame.image.load('assets/story_bg3.png').convert()
        story_bg4 = pygame.image.load('assets/story_bg4.png').convert()
        calcium_story_1 = pygame.image.load("assets/calcium_story_1.png").convert_alpha()
        calcium_story_2 = pygame.image.load("assets/calcium_story_2.png").convert_alpha()
        next_button = pygame.image.load("assets/next_button.png").convert_alpha()
        next_button_hover = pygame.image.load("assets/next_button_hover.png").convert_alpha()
        next_button_rect = next_button.get_rect(center=(700, 530))
        play_button = pygame.image.load("assets/play_button.png").convert_alpha()
        play_button_hover = pygame.image.load("assets/play_button_hover.png").convert_alpha()
        play_button_rect = play_button.get_rect(center=(402, 530))
        state = 'story'
        scene = 'scene1'


    elif state == 'story':
        if scene == 'scene1':
            screen.blit(story_bg1, (0,0))
            if (pygame.time.get_ticks() % 1000 - 500) < 0: #display image in turn every .5 sec
                    screen.blit(calcium_story_1,calcium_story_1.get_rect(center=(400,530)))
            else:
                screen.blit(calcium_story_2,calcium_story_2.get_rect(center=(400,530)))

        elif scene == 'scene2':
            screen.blit(story_bg2, (0,0))

        elif scene == 'scene3':
            screen.blit(story_bg3, (0,0))

        elif scene == 'scene4':
            screen.blit(story_bg4, (0,0))
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            if play_button_rect.collidepoint(mouse_pos):
                screen.blit(play_button_hover, play_button_rect)    
            else:
                screen.blit(play_button, play_button_rect)

        if not scene == 'scene4':
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            if next_button_rect.collidepoint(mouse_pos):
                screen.blit(next_button_hover, next_button_rect)    
            else:
                screen.blit(next_button, next_button_rect)


    elif state == 'level_init': # initialize game screen
        all_sprites = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        enemy_projectiles = pygame.sprite.Group()
        tanks = pygame.sprite.Group()

        player = Player(screen, all_sprites, bullets)
        #enemy = Enemy(screen, all_sprites, enemy_projectiles)
        wander_enemy = []
        chase_enemy = []
        linear_enemy = []
        bb_enemy = []
        tank_enemy = []
        for i in range(10):
            wander_enemy.append(WanderEnemy(screen, all_sprites, enemy_projectiles,lambda: player.pos))
            chase_enemy.append(ChaseEnemy(screen, all_sprites, enemy_projectiles, lambda: player.pos, update_interval=120))
            linear_enemy.append(LinearEnemy(screen, all_sprites, enemy_projectiles, lambda: player.pos))
            bb_enemy.append(BossEnemy(screen, all_sprites, enemy_projectiles, lambda: player.pos))
            # tank_enemy.append(Tank(screen, all_sprites, tanks))
        # 敵のグループを作成
        enemies = pygame.sprite.Group()

        # enemies.add(wander_enemy, chase_enemy)  # ← ここ追加
        # enemies.add(linear_enemy)  # ← ここ追加
        # enemies.add(bb_enemy)
        # enemies.add(chase_enemy)

        all_sprites.add(player)
        all_sprites.add(enemies)
        all_sprites.add(bullets)
        all_sprites.add(enemy_projectiles)

        player_life = Life(max_lives=30)
        boss_life = Life(max_lives=30, position=(390,460), image='assets/heart_blue.png')
        background = Background(SCREEN_WIDTH, SCREEN_WIDTH, scroll_speed=1)

        level_start_time = pygame.time.get_ticks() // 1000  #define the level time started

        state = 'playing'
        wave = 1
        wave_init = True
        boss_flag = False
        boss_start_time = 0

    elif state == 'pause_init':
        paused = pygame.image.load('assets/paused.png').convert()
        title_button = pygame.image.load('assets/title_button.png').convert()
        title_button_hover = pygame.image.load('assets/title_button_hover.png').convert()
        title_button_rect = play_button.get_rect(center=(402, 530))
        state = 'pause'

    elif state == 'pause':
        screen.blit(paused, (0,0))
        # play button
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if title_button_rect.collidepoint(mouse_pos):
            screen.blit(title_button_hover, title_button_rect)
            if mouse_click[0]:  # Left-click
                state = 'title_init'
        else:
            screen.blit(title_button, title_button_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
