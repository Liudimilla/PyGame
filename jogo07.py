# Versao 7: adiciona movimento ao jogador. Para isso foi preciso adicionar tratamento de eventos
# no main loop, algumas variaveis para representar os comandos no Game e o metodo update em Player

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
        self.speed = 4;
    def update(self):
        if self.game.commands["move right"]:
            self.rect.x += self.speed;
            if self.rect.x > self.game.screen_width / 2:
                self.rect.x = self.game.screen_width / 2
        if self.game.commands["move left"]:
            self.rect.x -= self.speed;
            if self.rect.x < 0:
                self.rect.x = 0
        if self.game.commands["move up"]:
            self.rect.y -= self.speed;
            if self.rect.y < 0:
                self.rect.y = 0
        if self.game.commands["move down"]:
            self.rect.y += self.speed;
            if self.rect.y > self.game.screen_height - self.rect.height:
                self.rect.y = self.game.screen_height - self.rect.height
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
        self.commands = {'move left': False, 'move right': False, 'move up': False, 'move down': False, 'fire': False};
        
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
        play = True
        while play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    self.handle_key(event.key, event.type == pygame.KEYDOWN)

            # executa a atualização das entidades
            for e in self.entities:
                e.update()
            # executa o desenho das entidades
            self.screen.fill((0, 0, 128))
            for e in self.entities:
                e.draw()
            pygame.display.flip()
            # faz o programa aguardar 50 milissegundos
            pygame.time.wait(50)

    #novo metodo adicionado a Game para tratar eventos de teclas
    def handle_key(self, key, pressed):
        if key == K_DOWN:
            self.commands['move down'] = pressed
        if key == K_LEFT:
            self.commands['move left'] = pressed
        if key == K_UP:
            self.commands['move up'] = pressed
        if key == K_RIGHT:
            self.commands['move right'] = pressed
        if key == K_SPACE:
            self.commands['fire'] = pressed

    def shutdown(self):
        pass

if __name__ == "__main__":
    my_game = Game()
    my_game.setup()
    my_game.main_loop()
    my_game.shutdown()
