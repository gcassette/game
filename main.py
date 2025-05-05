import pygame
from Character.Player import Player
from Character.Enemy import Enemy
from Character.WanderEnemy import WanderEnemy
from Character.ChaseEnemy import ChaseEnemy
from Life import Life
from Background import Background
import SpriteGroups.EnemyProjectile


SCREEN_WIDTH, SCREEN_HEIGHT = 800, 585
screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT) 
TIME_LIMIT = 300

# Initialization
pygame.init()
font = pygame.font.SysFont(None, 36)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hello Pygame")
pygame.mixer.init()
pygame.mixer.music.load("assets/\u571f\u661f\u30c0\u30f3\u30b9.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.02)
damage_sound = pygame.mixer.Sound("assets/レトロアクション_3.mp3")
damage_sound.set_volume(0.05)
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
chase_enemy = ChaseEnemy(screen, ene_pro_manager, lambda: player.pos, update_interval=5)
# 敵のグループを作成
enemies = pygame.sprite.Group()

all_sprites.add(player)
all_sprites.add(enemy)
all_sprites.add(wander_enemy)
all_sprites.add(chase_enemy)
enemies.add(enemy, wander_enemy, chase_enemy)  # ← ここ追加

all_sprites.add(sprite_enemies)

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.shoot()

    all_sprites.update()
    background.update()
    background.draw(screen)
    all_sprites.draw(screen)

    #direction_text = font.render(f"Angle: {player.angle:.2f}", True, (255, 255, 0))
    #screen.blit(direction_text, (10, 30))

    # Calculate the time elapsed
    elapsed_ms = pygame.time.get_ticks()
    elapsed_sec = elapsed_ms // 1000
    time_ramaining = TIME_LIMIT - elapsed_sec
    timer_text = font.render(f"Time: {time_ramaining}s", True, (255, 255, 255))
    # --- 衝突判定 ---

    if collided_enemies := pygame.sprite.spritecollide(player, enemies, False, collided=pygame.sprite.collide_mask):
        if not player.invincible:  # ← この条件を追加
            player_life.lose_life()
            damage_sound.play()
            player.trigger_invincibility(duration_frames=300)
            print("Player hit by enemy!")

            for collided_enemy in collided_enemies:
                if isinstance(collided_enemy, ChaseEnemy):
                    collided_enemy.trigger_cooldown(frames=120)




    # Player と Fireball の当たり判定
    if collided_fireballs := pygame.sprite.spritecollide(player, enemy_projectiles, True, collided=pygame.sprite.collide_mask):
        #player_life.lose_life()
        #damage_sound.play()
        #print("Player hit by enemy projectile!")
        #playerとbulletの座標を出力
        # print(f"Player Position: {player.pos.x}, {player.pos.y}")
        # for proj in enemy_projectiles:
        #     print(f"Enemy Projectile Position: {proj.pos.x}, {proj.pos.y}")
        pass

    # WanderEnemy と bullets の当たり判定
    # wander_enemy と bullets の当たり判定
    if collided_bullets := pygame.sprite.spritecollide(wander_enemy, bullets, True, collided=pygame.sprite.collide_mask):
        wander_enemy.take_damage()
        print("WanderEnemy hit by bullet!")

        if wander_enemy.hp <= 0:
            wander_enemy.kill()

    # Player と 敵本体の当たり判定
    # if pygame.sprite.spritecollide(player, chase_enemy, False, collided=pygame.sprite.collide_rect):
    #     player_life.lose_life()
    #     damage_sound.play()
    #     chase_enemy.trigger_cooldown(frames=120)

    # collided_list = pygame.sprite.spritecollide(player, enemies, False, collided=pygame.sprite.collide_rect)
    # if collided_list:
    #     player_life.lose_life()
    #     damage_sound.play()
    #     for collided_enemy in collided_list:
    #         if isinstance(collided_enemy, ChaseEnemy):
    #             collided_enemy.trigger_cooldown(frames=120)

    # for collided_enemy in enemies:
    #     if collided_enemy.rect.colliderect(player.get_enlarged_rect(100)):
    #         player_life.lose_life()
    #         damage_sound.play()

    #         if isinstance(collided_enemy, ChaseEnemy):
    #             collided_enemy.trigger_cooldown(frames=120)


    # ライフが0になったらゲーム終了
    if player_life.current_lives <= 0:
        print("ゲームオーバー")
        running = False


    screen.blit(timer_text, (650, 10))

    player_life.draw(screen)

    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

"""
このコードは `Pygame` を使ったシンプルな**2Dシューティングゲーム**のメインループを構築したものです。以下でコードの各部分について丁寧に解説します。

---

## ✅ 1. モジュールとクラスの読み込み

```python
import pygame
from Character.Player import Player
from Character.Enemy import Enemy
from Character.WanderEnemy import WanderEnemy
from Life import Life
from Background import Background
import SpriteGroups.EnemyProjectile
```

* `pygame`: 2Dゲーム用のPythonライブラリ
* `Player`, `Enemy`, `WanderEnemy`: プレイヤー、通常の敵、ランダム移動する敵のクラス
* `Life`: プレイヤーのライフ管理クラス
* `Background`: 横スクロール背景クラス
* `SpriteGroups.EnemyProjectile`: 敵の弾の管理用モジュール

---

## ✅ 2. 画面・定数設定

```python
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 585
screen_rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
TIME_LIMIT = 300
```

* ゲーム画面サイズ：800×585
* `screen_rect`: 画面の境界矩形（キャラがはみ出さないためなどに使える）
* `TIME_LIMIT`: ゲーム制限時間（秒）

---

## ✅ 3. Pygameの初期化とリソース読み込み

```python
pygame.init()
font = pygame.font.SysFont(None, 36)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hello Pygame")
```

* Pygame の初期化と画面生成
* ゲームタイトルをウィンドウに表示

```python
pygame.mixer.init()
pygame.mixer.music.load("assets/土星ダンス.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.02)
```

* BGMを読み込んで再生。ループ再生 `(-1)`、音量は控えめ。

```python
damage_sound = pygame.mixer.Sound("assets/レトロアクション_3.mp3")
damage_sound.set_volume(0.05)
```

* ダメージを受けた時の効果音を設定

---

## ✅ 4. ゲームオブジェクトの生成

```python
player_life = Life(max_lives=5)
background = Background(SCREEN_WIDTH, SCREEN_WIDTH, scroll_speed=1)
```

* プレイヤーのライフを5に設定
* 背景を生成（`scroll_speed=1`）

```python
all_sprites = pygame.sprite.Group()
sprite_enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_projectiles = pygame.sprite.Group()
```

* スプライト管理グループを作成
* `all_sprites`: 全スプライト
* `sprite_enemies`: 敵のスプライト（未使用っぽい？）
* `bullets`, `enemy_projectiles`: 弾の管理グループ

```python
ene_pro_manager = SpriteGroups.EnemyProjectile.EnemyProjectileManager(all_sprites, enemy_projectiles)
```

* 敵の弾を管理するマネージャーのインスタンス作成

```python
player = Player(screen, all_sprites)
enemy = Enemy(screen, ene_pro_manager)
wander_enemy = WanderEnemy(screen, ene_pro_manager)
```

* プレイヤー、通常敵、さまよう敵のインスタンスを生成

```python
enemies = pygame.sprite.Group()
all_sprites.add(player, enemy, wander_enemy)
```

* `enemies`: 敵との当たり判定用の空のグループ（でも`enemy`や`wander_enemy`をここに追加していないので不備あり）

---

## ✅ 5. メインループ（ゲーム進行）

```python
clock = pygame.time.Clock()
running = True
```

* FPS（毎秒フレーム数）制御用
* `running` が False になるまでループ

---

## ✅ 6. イベント処理

```python
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        player.shoot()
```

* ウィンドウの閉じるボタン or `スペースキー` を押したときの処理

---

## ✅ 7. 更新処理と描画

```python
all_sprites.update()
background.update()
background.draw(screen)
all_sprites.draw(screen)
```

* スプライトの位置などを更新
* 背景をスクロール描画
* スプライトの描画

---

## ✅ 8. タイマー表示

```python
elapsed_ms = pygame.time.get_ticks()
elapsed_sec = elapsed_ms // 1000
time_ramaining = TIME_LIMIT - elapsed_sec
timer_text = font.render(f"Time: {time_ramaining}s", True, (255, 255, 255))
```

* 経過時間を取得して、残り時間を算出
* タイマー表示をレンダリング

---

## ✅ 9. 衝突判定

```python
# プレイヤー vs 敵（※enemies に誰も入ってないので無効）
if pygame.sprite.spritecollide(player, enemies, False, collided=pygame.sprite.collide_rect):
    ...

# プレイヤー vs 敵の弾
if pygame.sprite.spritecollide(player, enemy_projectiles, True, ...):
    ...

# さまよう敵 vs プレイヤーの弾
if pygame.sprite.spritecollide(wander_enemy, bullets, True, ...):
    wander_enemy.take_damage()
    if wander_enemy.hp <= 0:
        wander_enemy.kill()
```

* 敵との接触や被弾でライフが減る
* WanderEnemy の HP が 0 以下で削除される

---

## ✅ 10. ライフゲージやゲームオーバー判定

```python
if player_life.current_lives <= 0:
    print("ゲームオーバー")
    running = False
```

* ライフが0になったら終了

---

## ✅ 11. 画面更新とFPS調整

```python
screen.blit(timer_text, (650, 10))
player_life.draw(screen)
all_sprites.update()
all_sprites.draw(screen)
pygame.display.flip()
clock.tick(60)
```

* タイマーやライフを描画
* 表示を更新（`flip()`）
* FPSを60に制限

---

## ✅ 12. ゲーム終了

```python
pygame.quit()
```

---

## ❗ 気になる点（修正候補）

1. `enemies` に `enemy` や `wander_enemy` を追加していない
   　→ 当たり判定が無効になってる。

2. `all_sprites.update()` がループ内で2回呼ばれている
   　→ 冗長なので1回でよい。

---

必要であれば、これをベースに機能追加（スコア表示、ステージ進行、複数敵など）もできます。ご希望があればお知らせください。


ご質問の箇所におけるコード：

```python
player = Player(screen, all_sprites)
enemy = Enemy(screen, ene_pro_manager)
wander_enemy = WanderEnemy(screen, ene_pro_manager)
```

と

```python
all_sprites = pygame.sprite.Group()
sprite_enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_projectiles = pygame.sprite.Group()
```

は、\*\*オブジェクト指向プログラミング（OOP）\*\*の観点から見ると、以下のような設計になっています。

---

## 🧩 概要：クラスとインスタンスの関係

このコードは **「登場キャラクターや弾などをクラスで定義」し、**それぞれを**個別のオブジェクトとして生成（インスタンス化）**しています。
また、**`Group`（グループ）オブジェクトで、それらを一括管理**できるようにしています。

---

## 🔍 各行のオブジェクト指向的な役割

### 🔸 `all_sprites = pygame.sprite.Group()`

* **`Group` クラス**のインスタンスを作成。
* `Sprite`（スプライト）を複数まとめて扱うための**コンテナ**。
* **共通の `update()` や `draw()` を一括で呼び出せる**。

---

### 🔸 `player = Player(screen, all_sprites)`

* `Player` クラス（`pygame.sprite.Sprite` を継承しているはず）のインスタンス。
* `__init__()` メソッドで `screen` と `all_sprites` を引数に取り、初期化。
* おそらく `all_sprites.add(self)` を内部で呼び、**自分自身をスプライトグループに登録**している。

👉 **責務**：自分の描画、移動、攻撃（`shoot()`）などを管理する。

---

### 🔸 `enemy = Enemy(screen, ene_pro_manager)`

* `Enemy` クラスのインスタンス。
* 引数 `ene_pro_manager` は弾の発射などを管理するクラス（弾生成やグループへの追加を委譲）。

👉 **責務**：敵キャラの行動ロジック（移動・弾発射など）

---

### 🔸 `wander_enemy = WanderEnemy(screen, ene_pro_manager)`

* `WanderEnemy` クラス（`Enemy` のサブクラスの可能性あり）。
* ランダム移動や特殊パターンの動きを持つ敵。

👉 **責務**：画面内を自律的にランダム移動し、必要に応じて攻撃する。

---

### 🔸 `bullets`, `enemy_projectiles` グループ

* プレイヤー弾・敵弾をそれぞれ管理するためのグループ。
* `pygame.sprite.Group()` を使うことで、当たり判定・描画・更新を効率化。

---

## 🎯 オブジェクト指向的にどうなっているか

### ✅ クラスごとの「責任分担」が明確

| クラス名                       | 責任・機能                  |
| -------------------------- | ---------------------- |
| `Player`                   | プレイヤーの表示、移動、攻撃、ライフ管理   |
| `Enemy`                    | 通常敵の表示・移動・攻撃           |
| `WanderEnemy`              | 自律的に動く敵                |
| `EnemyProjectileManager`   | 敵弾の生成・登録管理（**委譲パターン**） |
| `Group` (`all_sprites` など) | スプライトの一括処理、衝突判定、描画の対象  |

---

### ✅ 各オブジェクトは **自律的な振る舞い（encapsulation）** を持つ

たとえば `player.update()` はプレイヤーの状態更新のみを担当し、`enemy.update()` は敵のみの行動を更新。
これにより、各オブジェクトが**単一責任原則**に近い形で動作しています。

---

### ✅ スプライトグループの活用は **ポリモーフィズム** を実現

* `all_sprites.update()` とするだけで、グループ内のすべてのスプライト（`Player`, `Enemy`, `WanderEnemy`）の `update()` が自動的に呼ばれます。
* これは**継承したメソッドを共通インターフェースで呼び出す**という、OOPの代表的なパターン（**ポリモーフィズム**）。

---

## ✅ まとめ

この部分のコードはオブジェクト指向において：

* **クラスベース設計**（Player, Enemy...）
* **インスタンス化による状態保持**
* **責務の分離と委譲**
* **スプライトグループによるポリモーフィズム**

をうまく活かしています。
特に `Group` クラスによって、**共通メソッド（`update`/`draw`）の一括呼び出しが可能**になっているのが、OOPとして非常に良い設計です。

---

よりOOPを強化したい場合は、例えば：

* `EnemyManager` クラスで敵の生成や一括管理を行う
* `Game` クラスにメインループをまとめる

などが考えられます。必要であれば提案もできます。

"""