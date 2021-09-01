# Versao 3: adiciona uma classe para representar entidades do jogo
# tais como personagens, inimigos etc.

import pygame
import pygame.display
import pygame.time
from pygame.locals import *

# A classe GameEntity sera usada para representar uma entidade do jogo
# Assim, ela inicialmente possui uma posicao e um tamanho, dados em pixels
class GameEntity():
    def __init__(self, game, x = 0, y = 0, w = 32, h = 32):
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
    def update(self):
        pass
    # Por enquanto a entidade se "desenha" escrevendo sua posicao atual
    def draw(self):
        print("Entidade de jogo em X:" + str(self.rect.left) + ", Y:" + str(self.rect.top));

class Game():
    def __init__(self):
        self.screen_width = 640
        self.screen_height = 360
        self.screen = None
        self.entities = []
        
    def setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])
        # adiciona uma entidade de jogo no centro da tela
        self.entities.append(GameEntity(self, self.screen_width/2, self.screen_height/2))
    
    def main_loop(self):
        # executa a atualização das entidades
        for e in self.entities:
            e.update()
        # executa o desenho das entidades
        for e in self.entities:
            e.draw()
        # faz o programa aguardar 2 segundos
        pygame.time.wait(2000)

    def shutdown(self):
        pass

if __name__ == "__main__":
    my_game = Game()
    my_game.setup()
    my_game.main_loop()
    my_game.shutdown()
