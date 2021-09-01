# Versao 5: acrescenta uma nova entidade (Enemy).

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

class Player(GameEntity):
    image = None
    
    def __init__(self, game, x = 0, y = 0, w = 64, h = 32):
        GameEntity.__init__(self, game, x, y, w, h)
    def draw(self):
        self.game.screen.blit(self.image, (self.rect.left, self.rect.top))

# Cria uma nova classe de entidade, para representar os inimigos
class Enemy(GameEntity):
    image = None
    
    def __init__(self, game, x = 0, y = 0, w = 64, h = 32):
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
        # adiciona uma entidade do jogador
        self.entities.append(Player(self, 10, 170))
        # carrega a imagem do inimigo
        Enemy.image = pygame.image.load(os.path.join("images","enemyship.png"))
        # adiciona uma entidade de inimigo
        self.entities.append(Enemy(self, 320, 60))
        
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
