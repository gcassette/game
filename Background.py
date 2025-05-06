import pygame

class Background:
    def __init__(self, screen_width, screen_height, scroll_speed=1, image='assets//bg1.png'):
        self.image = pygame.image.load(image).convert()
        # self.image = pygame.transform.scale(self.image, (screen_width, screen_height))
        self.width = self.image.get_width()
        self.scroll_x = 0
        self.scroll_speed = scroll_speed
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self):
        self.scroll_x -= self.scroll_speed
        if self.scroll_x <= -self.width:
            self.scroll_x = 0

    def draw(self, surface):
        # Draw twice to create a seamless loop
        surface.blit(self.image, (self.scroll_x, 0))
        surface.blit(self.image, (self.scroll_x + self.width, 0))

"""
ありがとうございます。あなたの `Background` クラスは、**横方向にループスクロールする背景**を実現するためのクラスです。以下に詳しく解説します。

---

## 🎯 概要

この `Background` クラスは、背景画像を横にスクロールさせ、**シームレスにループさせる**処理を行います。ゲームにおける「動きのある背景」を演出するために使われます。

---

## 🧩 クラスの構成

### ### `__init__()` コンストラクタ

```python
def __init__(self, screen_width, screen_height, scroll_speed=1):
    self.image = pygame.image.load('assets//bg1.png').convert()
    self.width = self.image.get_width()
    self.scroll_x = 0
    self.scroll_speed = scroll_speed
    self.screen_width = screen_width
    self.screen_height = screen_height
```

* `self.image`：背景画像（`bg1.png`）を読み込む。
* `self.width`：画像の幅。ループ処理に使う。
* `self.scroll_x`：背景のスクロール位置。初期値は0。
* `self.scroll_speed`：スクロールする速さ。
* `screen_width`, `screen_height`：背景を描画する画面サイズ。

🔸 ※ `scale()` の行はコメントアウトされていて、背景画像のリサイズは今はしていない。

---

### ### `update()` メソッド

```python
def update(self):
    self.scroll_x -= self.scroll_speed
    if self.scroll_x <= -self.width:
        self.scroll_x = 0
```

* スクロールを進める（左に移動する）。
* 画像の左端が完全に画面外に出たら、スクロール位置をリセットして**ループ再生**。

---

### ### `draw()` メソッド

```python
def draw(self, surface):
    surface.blit(self.image, (self.scroll_x, 0))
    surface.blit(self.image, (self.scroll_x + self.width, 0))
```

* 画像を **2回描画**することで、ループスクロールを実現。
* `scroll_x + self.width` により、2枚目の画像が1枚目の右隣にくるように配置。
* これにより切れ目のないスムーズなスクロールが可能。

---

## 🖼️ ビジュアル的なイメージ

```
画面幅:   |<---------------------------- SCREEN_WIDTH ---------------------------->|
描画順:   [ image(1) @ scroll_x ] [ image(2) @ scroll_x + width ]
スクロール: ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ←
リセット条件: scroll_x <= -width のとき scroll_x = 0
```

---

## ✅ 改善ポイント（任意）

1. **スケーリングを有効化**したい場合は、以下の行を元に戻して使います：

   ```python
   self.image = pygame.transform.scale(self.image, (screen_width, screen_height))
   ```

2. **垂直方向（Y方向）のスクロール**もしたい場合は別途調整が必要です。

---

何か応用したい方向（例：背景切り替え、縦スクロールなど）があればそれもお手伝いできます。

"""