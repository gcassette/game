import pygame

class Life(pygame.sprite.Sprite):
    def __init__(self, heart_image_path, max_lives, position=(10, 10), spacing=40):
        super().__init__()
        self.max_lives = max_lives
        self.current_lives = max_lives
        self.position = position
        self.spacing = spacing
        self.image = pygame.image.load(heart_image_path).convert_alpha()
        self.rect = self.image.get_rect()

    def lose_life(self):
        if self.current_lives > 0:
            self.current_lives -= 1

    def gain_life(self):
        if self.current_lives < self.max_lives:
            self.current_lives += 1

    def draw(self, surface):
        for i in range(self.current_lives):
            x = self.position[0] + i * self.spacing
            y = self.position[1]
            surface.blit(self.image, (x, y))