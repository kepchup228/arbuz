import pygame
import random
from player import Player
from enemy import Enemy
from item import Item
from settings import *


class Level:
    def __init__(self):
        self.player = Player()  # игрок
        self.enemies = [Enemy(self.player) for _ in range(5)]  # враги
        self.items = [Item() for _ in range(10)]  # предметы
        self.coin_spawn_timer = 0  # таймер спавна монет
        self.coin_spawn_interval = 2000  # интервал спавна

        # предыдущие результаты
        self.previous_score = LAST_SCORE
        self.previous_level = LAST_LEVEL
        self.previous_coins = LAST_COINS

        # кнопка "начать заново"
        self.restart_button = RestartButton()

    def spawn_coins(self):
        current_time = pygame.time.get_ticks()
        if len(self.items) < 7 and current_time - self.coin_spawn_timer > self.coin_spawn_interval:
            if len(self.items) < 10:
                new_coin = Item()
                new_coin.rect.topleft = (random.randint(0, WIDTH - 50), random.randint(0, HEIGHT - 50))
                self.items.append(new_coin)
                self.coin_spawn_timer = current_time

    def update(self):
        self.player.update()

        # добавление нового врага на уровне 3
        if self.player.level == 3 and len(self.enemies) == 5:
            new_enemy = Enemy(self.player)
            # проверка на пересечение с врагами другими
            if not any(new_enemy.rect.colliderect(enemy.rect) for enemy in self.enemies):
                self.enemies.append(new_enemy)  # добавляем нового врага, если нет пересечений

        for coin in self.items[:]:
            if self.player.rect.colliderect(coin.rect):
                self.items.remove(coin)  # сбор монеты
                self.player.coins_collected += 1

                if self.player.coins_collected >= 10:
                    self.player.level_up()  # повышение уровня

        for enemy in self.enemies:
            enemy.update()  # обновление врагов
            if self.player.rect.colliderect(enemy.rect):
                self.player.take_damage(10)  # урон игроку

        self.spawn_coins()  # спавн монет

    def draw(self, surface):
        surface.fill(WHITE)

        if self.player.health <= 0:
            self.display_game_over(surface)  # конец игры
            return  # прекращение отрисовки

        self.player.draw(surface)  # отрисовка игрока
        self.player.draw_health_bar(surface)  # отрисовка здоровья

        for enemy in self.enemies:
            enemy.draw(surface)  # отрисовка врагов
        for item in self.items:
            item.draw(surface)  # отрисовка предметов

        font = pygame.font.Font(None, 36)
        coins_text = font.render(f"Монет - {self.player.coins_collected}", True, (0, 0, 0))
        level_text = font.render(f"LEVEL {self.player.level}", True, (0, 0, 0))
        surface.blit(coins_text, (10, 10))  # отображение монет
        surface.blit(level_text, (10, 50))  # отображение уровня

    def display_game_over(self, surface):
        game_over_text = GameOverText()  # текст окончания игры
        all_sprites = pygame.sprite.Group(game_over_text, self.restart_button)

        # текст "Game Over"
        while game_over_text.n > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # левый клик
                        if self.restart_button.rect.collidepoint(event.pos):
                            self.restart_game()  # перезапуск игры

            all_sprites.update()
            surface.fill((0, 0, 0))  # очистка экрана
            all_sprites.draw(surface)

            pygame.display.flip()
            pygame.time.delay(30)

        self.save_results()  # сохранение результатов
        self.show_final_score(surface)  # отображение финального счета

        # отображение кнопки "начать заново"
        self.restart_button.draw(surface)
        pygame.display.flip()

        # обработка нажатия кнопки
        self.handle_restart_event()

    def handle_restart_event(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # левый клик
                        if self.restart_button.rect.collidepoint(event.pos):
                            self.restart_game()  # перезапуск игры

    def save_results(self):
        global LAST_SCORE, LAST_LEVEL, LAST_COINS
        LAST_SCORE = self.player.coins_collected  # сохранение счета
        LAST_LEVEL = self.player.level  # сохранение уровня
        LAST_COINS = self.player.coins_collected  # сохранение монет

    def restart_game(self):
        import main
        main.main()  # перезапуск игры

    def show_final_score(self, surface):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Счет: {self.player.coins_collected}", True, TEXT_COLOR)
        level_text = font.render(f"Уровень: {self.player.level}", True, TEXT_COLOR)
        coins_text = font.render(f"Общее количество монет: {self.player.coins_collected}", True, TEXT_COLOR)

        # отображение прошлых результатов
        last_score_text = font.render(f"Прошлый счет: {self.previous_score}", True, LAST_RESULT_COLOR)
        last_level_text = font.render(f"Прошлый уровень: {self.previous_level}", True, LAST_RESULT_COLOR)
        last_coins_text = font.render(f"Прошлое количество монет: {self.previous_coins}", True, LAST_RESULT_COLOR)

        surface.fill((0, 0, 0))  # очистка экрана
        surface.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 100))
        surface.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HEIGHT // 2 - 50))
        surface.blit(coins_text, (WIDTH // 2 - coins_text.get_width() // 2, HEIGHT // 2))

        surface.blit(last_score_text, (WIDTH // 2 - last_score_text.get_width() // 2, HEIGHT // 2 + 50))
        surface.blit(last_level_text, (WIDTH // 2 - last_level_text.get_width() // 2, HEIGHT // 2 + 100))
        surface.blit(last_coins_text, (WIDTH // 2 - last_coins_text.get_width() // 2, HEIGHT // 2 + 150))

        pygame.display.flip()
        pygame.time.delay(5000)  # задержка перед закрытием


class RestartButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 36)
        self.image = self.font.render("Начать заново", True, (0, 255, 0))
        self.rect = self.image.get_rect(center=(WIDTH // 2, 50))

    def draw(self, surface):
        surface.blit(self.image, self.rect)  # отрисовка кнопки


class GameOverText(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 74)
        self.image = self.font.render("Game Over", True, (255, 0, 0))
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.n = 255
        self.y_spee = -1  # скорость движения

    def update(self):
        self.rect.y += self.y_spee  # движение текста
        self.n -= 2  # уменьшение 
        if self.n < 0:
            self.n = 0
        self.image.set_alpha(self.n)

    def draw(self, surface):
        surface.blit(self.image, self.rect)  # отрисовка текста
