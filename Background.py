import pygame

class Background:
    def __init__(self, screen_width, screen_height, scroll_speed=1):
        self.image = pygame.image.load('assets//bg1.png').convert()
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