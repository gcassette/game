import pygame

# Define our square object and call super to
# give it all the properties and methods of pygame.sprite.Sprite
# Define the class for our square objects
class Square(pygame.sprite.Sprite):
    def __init__(self):
        super(Square, self).__init__()
         
        # Define the dimension of the surface
        # Here we are making squares of side 25px
        self.surf = pygame.Surface((25, 25))
         
        # Define the color of the surface using RGB color coding.
        self.surf.fill((0, 200, 255))
        self.rect = self.surf.get_rect()

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Hello Pygame")

# instantiate all square objects
square1 = Square()
square2 = Square()
square3 = Square()
square4 = Square()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Define where the squares will appear on the screen
    # Use blit to draw them on the screen surface
    screen.blit(square1.surf, (40, 40))
    screen.blit(square2.surf, (40, 530))
    screen.blit(square3.surf, (730, 40))
    screen.blit(square4.surf, (730, 530))
    # Update the display using flip
    pygame.display.flip()

# Quit Pygame
pygame.quit()