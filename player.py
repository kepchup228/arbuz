import pygame
import os
from settings import *

class Player:
    def __init__(self):
        self.image_path = 'data/images/player.png'
        if not os.path.isfile(self.image_path):
            print(f"Ошибка: файл {self.image_path} не найден!")
            self.image = pygame.Surface((50, 50))
        else:
            original_image = pygame.image.load(self.image_path)
            self.image = pygame.transform.scale(original_image, (50, 50))  # изменение размера

        self.rect = self.image.get_rect()
        self.rect.topleft = (100, 100)  # начальная позиция игрока
        self.speed = 5
        self.health = 100
        self.y_timer = 0  # время последнего урона
        self.y_ti = 200  # длительность неуязвимости в миллисекундах
        self.coins_collected = 0  # собранные монеты
        self.level = 1  # уровень игрока
        self.base_speed = 5  # базовая скорость

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < WIDTH - self.rect.width:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < HEIGHT - self.rect.height:
            self.rect.y += self.speed

    def draw(self, surface):
        current_time = pygame.time.get_ticks()
        if current_time - self.y_timer < self.y_ti:
            # рисовать игрока полупрозрачным во время неуязвимости
            self.image.set_alpha(128)
        else:
            self.image.set_alpha(255)

        surface.blit(self.image, self.rect)

    def draw_health_bar(self, surface):
        bar_width = 50
        bar_height = 10
        health_ratio = self.health / 100

        bar_x = self.rect.x + (self.rect.width - bar_width) // 2
        bar_y = self.rect.y - 15

        # рисуем красный фон шкалы
        pygame.draw.rect(surface, RED, (bar_x, bar_y, bar_width, bar_height))
        # рисуем зеленую часть шкалы хп
        pygame.draw.rect(surface, GREEN, (bar_x, bar_y, bar_width * health_ratio, bar_height))

    def take_damage(self, damage):
        current_time = pygame.time.get_ticks()
        if current_time - self.y_timer > self.y_ti:
            self.health -= damage
            self.y_timer = current_time  # время последнего урона
            if self.health < 0:
                self.health = 0  # чтобы здоровье не уходило в минус

    def level_up(self):
        if self.level < 20:  # максимальный уровень - 20
            self.level += 1
            self.coins_collected = 0  # обнуляем счёт монет
            self.speed = self.base_speed * (1 + 0.05 * self.level)  # увеличиваем скорость
        if self.level >= 20:
            self.level = 20