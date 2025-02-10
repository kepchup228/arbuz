import pygame
import os
import random
from settings import WIDTH, HEIGHT


class Item:
    def __init__(self):
        self.image_path = 'data/images/item.png'
        if os.path.isfile(self.image_path):  # проверяем существование файла
            original_image = pygame.image.load(self.image_path)
            self.image = pygame.transform.scale(original_image, (30, 30))  # меняем размер
        else:
            self.image = pygame.Surface((30, 30))
            self.image.fill((255, 223, 0))

        # случайная начальная позицию
        self.rect = self.image.get_rect()
        self.rect.topleft = (random.randint(0, WIDTH - 30), random.randint(0, HEIGHT - 30))

    def draw(self, surface):
        surface.blit(self.image, self.rect)
