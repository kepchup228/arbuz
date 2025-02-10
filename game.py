import pygame
from level import Level
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.level.update()
            self.level.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()