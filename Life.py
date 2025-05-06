import pygame

class Life(pygame.sprite.Sprite):
    def __init__(self, max_lives, position=(10, 10), spacing=40, image='assets/heart.png'):
        super().__init__()
        self.max_lives = max_lives
        self.current_lives = max_lives
        self.position = position
        self.spacing = spacing
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()

    def lose_life(self):
        if self.current_lives > 0:
            self.current_lives -= 1

    def gain_life(self):
        if self.current_lives < self.max_lives:
            self.current_lives += 1

    def draw(self, surface):
        for i in range(self.current_lives):
            x = self.position[0] + i * self.spacing - (i // 10) * self.spacing * 10
            y = self.position[1] + (i // 10) * self.spacing
            surface.blit(self.image, (x, y))


class Heal(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load('assets/heart_green.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)