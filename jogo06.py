# Versao 6: acrescenta a entidade Explosion com animacao

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

class Enemy(GameEntity):
    image = None
    
    def __init__(self, game, x = 0, y = 0, w = 64, h = 32):
        GameEntity.__init__(self, game, x, y, w, h)
    def draw(self):
        self.game.screen.blit(self.image, (self.rect.left, self.rect.top))

class Explosion(GameEntity):
    image = None
    frames = []
    expw = 64
    exph = 64
    
    def __init__(self, game, x = 0, y = 0):
        GameEntity.__init__(self, game, x, y, self.expw, self.exph)
        self.current_frame = 0
    @classmethod
    def set_frames(cls, num_rows, num_per_row):
        cls.frames = []
        for y in range(num_rows):
            for x in range(num_per_row):
                cls.frames.append(Rect(cls.expw*x, cls.exph*y, cls.expw, cls.exph))
    def draw(self):
        self.game.screen.blit(self.image, (self.rect.left, self.rect.top), Explosion.frames[self.current_frame])
        self.current_frame = self.current_frame + 1
        if self.current_frame >= len(self.frames):
            self.current_frame = len(self.frames) - 1

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
        # carrega a imagem da explosao
        Explosion.image = pygame.image.load(os.path.join("images","explosion.png"))
        Explosion.set_frames(8, 8)
        self.entities.append(Explosion(self, 200, 200))
        
    def main_loop(self):
        # repete a logica ate termos exibido 64 quadros de animacao
        ct = 0
        while ct < 64:
            # executa a atualização das entidades
            for e in self.entities:
                e.update()
            # executa o desenho das entidades
            for e in self.entities:
                e.draw()
            pygame.display.flip()
            # faz o programa aguardar 50 milissegundos
            pygame.time.wait(50)
            ct = ct + 1

    def shutdown(self):
        pass

if __name__ == "__main__":
    my_game = Game()
    my_game.setup()
    my_game.main_loop()
    my_game.shutdown()
