# Versao 2: inicializa uma janela grafica

# vamos importar o modulo basico, controle de janelas e controle de tempo do PyGame
import pygame
import pygame.display
import pygame.time
from pygame.locals import *

class Game():
    # vamos modificar o construtor de Game para definir alguns atributos
    def __init__(self):
        self.screen_width = 640
        self.screen_height = 360
        self.screen = None
        
    def setup(self):
        pygame.init()
        # inicializa uma janela grafica
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])
    
    def main_loop(self):
        # faz o programa aguardar 2 segundos
        pygame.time.wait(2000)

    def shutdown(self):
        pass

if __name__ == "__main__":
    my_game = Game()
    my_game.setup()
    my_game.main_loop()
    my_game.shutdown()

