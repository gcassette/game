from abc import ABC, abstractclassmethod
import pygame
import math

class Weapon(pygame.sprite.Sprite):
    @abstractmethod
    def shoot(self, all_sprites, bullets_sprites_group):
        pass