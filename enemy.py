import pygame
import os
from settings import *


class Enemy:
    def __init__(self, player):
        self.image_path = 'data/images/enemy.png'

        if not os.path.isfile(self.image_path):
            print(f"Ошибка: файл {self.image_path} не найден!")
            self.image = pygame.Surface((50, 50))
        else:
            original_image = pygame.image.load(self.image_path)
            self.image = pygame.transform.scale(original_image, (50, 50))

        # управления места врага
        self.rect = self.image.get_rect()
        self.rect.topleft = (400, 100)
        self.speed = 2
        self.health = 50
        self.player = player

    def update(self):
        # движение врага к игроку
        if self.player.rect.x < self.rect.x:
            self.rect.x -= self.speed
        elif self.player.rect.x > self.rect.x:
            self.rect.x += self.speed

        if self.player.rect.y < self.rect.y:
            self.rect.y -= self.speed
        elif self.player.rect.y > self.rect.y:
            self.rect.y += self.speed

    def draw(self, surface):
        # Отрисовываем врага на экране
        surface.blit(self.image, self.rect)

        # полоска здоровья
        health_bar_width = 50
        health_bar_height = 5

        pygame.draw.rect(surface, RED, (self.rect.x, self.rect.y - 10, health_bar_width, health_bar_height))

        pygame.draw.rect(surface, GREEN,
                         (self.rect.x, self.rect.y - 10, health_bar_width * (self.health / 50), health_bar_height))
