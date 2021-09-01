# Versao 1: apenas carrega e inicializa o PyGame

# vamos importar os modulos basicos do PyGame
import pygame
from pygame.locals import *

# vamos criar uma classe para representar a estrutura do jogo
class Game():
    def __init__(self):
        pass
        
    def setup(self):
        # inicializa os modulos do PyGame
        pygame.init()
    
    def main_loop(self):
        pass

    def shutdown(self):
        pass

if __name__ == "__main__":
    my_game = Game()
    my_game.setup()
    my_game.main_loop()
    my_game.shutdown()
