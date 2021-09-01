# Versao 4: acrescenta a capacidade de desenhar imagens as entidades de jogo

import os
import pygame
import pygame.display
import pygame.time
from pygame.locals import *

class GameEntity():
    def __init__(self, game, x = 0, y = 0, w = 32, h = 32):
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
    def update(self):
        pass
    def draw(self):
        pass

# Vamos criar uma subclasse de GameEntity para representar a entidade controlada
# pelo jogador. Ela recebe um objeto com a imagem a ser desenhada.
class Player(GameEntity):
    image = None
    
    def __init__(self, game, x = 0, y = 0, w = 32, h = 32):
        GameEntity.__init__(self, game, x, y, w, h)
    def draw(self):
        self.game.screen.blit(self.image, (self.rect.left, self.rect.top))

class Game():
    def __init__(self):
        self.screen_width = 640
        self.screen_height = 360
        self.screen = None
        self.entities = []
        
    def setup(self):
        pygame.init()
        self.screen = pygame.display.set_mode([self.screen_width, self.screen_height])
        # carrega a imagem do jogador
        Player.image  = pygame.image.load(os.path.join("images","playership.png"))
        # adiciona uma entidade do jogador no centro da tela
        self.entities.append(Player(self, self.screen_width/2, self.screen_height/2, 64, 32))
    
    def main_loop(self):
        # executa a atualização das entidades
        for e in self.entities:
            e.update()
        # executa o desenho das entidades
        for e in self.entities:
            e.draw()
        pygame.display.flip()
        # faz o programa aguardar 2 segundos
        pygame.time.wait(2000)

    def shutdown(self):
        pass

if __name__ == "__main__":
    my_game = Game()
    my_game.setup()
    my_game.main_loop()
    my_game.shutdown()
