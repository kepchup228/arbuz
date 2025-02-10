import pygame
from game import Game
from settings import *


class StartScreen:
    def __init__(self):
        self.title_font = pygame.font.Font(None, 30)  # шрифт для заголовков
        self.body_font = pygame.font.Font(None, 20)  # шрифт для основного текста
        self.italic_font = pygame.font.Font(None, 20)  # шрифт для курсива
        self.title_color = (0, 0, 0)  # цвет заголовков
        self.body_color = (50, 50, 50)  # цвет основного текста

        self.instructions = [
            "Описание игры",
            "",
            "Цель игры",
            "Ваша задача — управлять персонажем, собирать монеты и избегать столкновений с врагами.",
            "Набирайте очки, повышайте уровень и становитесь сильнее!",
            "",
            "Управление",
            "- *Стрелки* или *WASD*: Двигайте персонажа влево, вправо, вверх, вниз.",
            "- *Esc*: Завершить игру в любой момент.",
            "",
            "Как играть",
            "1. *Начало игры*: После запуска игры вы увидите экран с кнопкой 'Начать'. Нажмите на неё, чтобы начать.",
            "2. *Сбор монет*: Собирайте монеты, которые появляются случайным образом. Каждая собранная монета увеличивает ваш счет.",
            "3. *Избегайте врагов*: Враги будут появляться на уровне. Если вы столкнетесь с врагом, ваш персонаж потеряет здоровье.",
            "4. *Уровни*: После сбора 10 монет ваш персонаж повысит уровень.",
            "5. *Конец игры*: Если здоровье вашего персонажа достигнет нуля, игра закончится.",
            "",
            "Дополнительные советы",
            "- Старайтесь избегать врагов и планируйте свои движения заранее.",
            "- Следите за количеством собранных монет и старайтесь достичь как можно большего результата.",
            "- Используйте кнопку 'Начать заново', чтобы попробовать снова и улучшить свои навыки!"
        ]
        self.play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 125, 200, 50)
        self.scroll_offset = 0

        # звук
        pygame.mixer.init()
        try:
            self.button_sound = pygame.mixer.Sound("data/sounds/button_click.wav")
        except FileNotFoundError:
            print("Звуковой файл не найден. Проверьте путь к файлу.")
            self.button_sound = None  # если звук не загрузился
        except pygame.error as e:
            print(f"Ошибка загрузки звука: {e}")
            self.button_sound = None  # если звук не загрузился

    def draw(self, surface):
        surface.fill(WHITE)
        title_text = self.title_font.render("Как играть", True, self.title_color)
        surface.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))  # заголовок вверху

        for i, line in enumerate(self.instructions):
            # курсив если надо
            if "*" in line:
                parts = line.split("*")
                x = 50
                for j, part in enumerate(parts):
                    if j % 2 == 1:  # курсив
                        instruction_text = self.italic_font.render(part, True, self.body_color)
                    else:  # обычный текст
                        instruction_text = self.body_font.render(part, True, self.body_color)
                    surface.blit(instruction_text, (x, 100 + i * 25 + self.scroll_offset))
                    x += instruction_text.get_width()  # обновляем позицию x
            else:
                instruction_text = self.body_font.render(line, True, self.body_color)
                surface.blit(instruction_text, (50, 100 + i * 25 + self.scroll_offset))

        pygame.draw.rect(surface, (0, 255, 0), self.play_button)  # кнопка "Играть"
        button_text = pygame.font.Font(None, 36).render("Играть", True, (0, 0, 0))
        surface.blit(button_text, (self.play_button.x + 50, self.play_button.y + 10))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.collidepoint(event.pos):
                if self.button_sound:  # проверяем, загружен ли звук
                    self.button_sound.play()
                return True  # начать игру
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                self.scroll_offset += 10
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.scroll_offset -= 10
        return False


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    game = Game()
    start_screen = StartScreen()  # создание стартового экрана

    running = True  # для основного цикла
    in_game = False  # для отслеживания состояния игры
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # выход из игры при закрытии окна
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # выход при нажатии Esc в любом случае
                    running = False
            if not in_game:
                if start_screen.handle_event(event):
                    in_game = True  # переход в игру

        if in_game:
            game.level.update()  # обновление уровня игры
            game.level.draw(screen)  # отрисовка уровня на экране
        else:
            start_screen.draw(screen)  # отрисовка стартового экрана

        pygame.display.flip()  # обновление экрана
        clock.tick(FPS)  # установка FPS

    pygame.quit()  # завершение Pygame


if __name__ == "__main__":
    main()
