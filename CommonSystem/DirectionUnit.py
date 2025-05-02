import pygame

class DirectionUnit:

    #(0,0)は入力違反
    def __init__(self, direction: pygame.math.Vector2):
        if direction.x == 0 & direction.y == 0:
            raise ValueError(f"direction is invalid. (direction: {direction} )")
        self.unit = direction.normalize()
        #ノルムが必要になったら
        #self.norm = np.linalg.norm(direction)

    def get_unit(self):
        return self.unit