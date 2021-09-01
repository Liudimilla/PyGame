# Versao 11: acrescenta grupos e mascaras de colisao

import os
import random
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
    def hit(self, other):
        pass

class Player(GameEntity):
    image = None
    collision_group = 1
    collision_mask = 2
    
    def __init__(self, game, x = 0, y = 0, w = 64, h = 32):
        GameEntity.__init__(self, game, x, y, w, h)
        self.speed = 4
        self.timer = 0
    def update(self):
        if self.timer > 0:
            self.timer -= 1
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
        if self.game.commands["fire"] and self.timer == 0:
            self.game.include(Laser(self.game, self.rect.x + self.rect.width, self.rect.y + self.rect.height/2))
            self.timer = 10
    def draw(self):
        self.game.screen.blit(self.image, (self.rect.left, self.rect.top))

class Enemy(GameEntity):
    image = None
    collision_group = 2
    collision_mask = 6
        
    def __init__(self, game, x = 0, y = 0, w = 64, h = 32):
        GameEntity.__init__(self, game, x, y, w, h)
        self.speed = -3
    def update(self):
        self.rect.x += self.speed
        if self.rect.x < -self.rect.width:
            self.game.destroy(self)
    def draw(self):
        self.game.screen.blit(self.image, (self.rect.left, self.rect.top))

class Laser(GameEntity):
    image = None
    collision_group = 4
    collision_mask = 2
        
    def __init__(self, game, x = 0, y = 0, w = 32, h = 16):
        GameEntity.__init__(self, game, x, y, w, h)
        self.speed = 6
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > self.game.screen_width:
            self.game.destroy(self)
    def draw(self):
        self.game.screen.blit(self.image, (self.rect.left, self.rect.top))

class Explosion(GameEntity):
    image = None
    collision_group = 0
    collision_mask = 0   
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
        self.destroy_list = []
        self.include_list = []
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
        # carrega a imagem da explosao
        Explosion.image = pygame.image.load(os.path.join("images","explosion.png"))
        Explosion.set_frames(8, 8)
        # carrega a imagem do laser do jogador
        Laser.image = pygame.image.load(os.path.join("images","playershot.png"))
        
    def main_loop(self):
        t_old = pygame.time.get_ticks()
        play = True
        while play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    self.handle_key(event.key, event.type == pygame.KEYDOWN)
            t_new = pygame.time.get_ticks()
            if t_new - t_old >= 1000:
                # adiciona uma entidade de inimigo a cada 1 segundo
                self.entities.append(Enemy(self, 640, random.randrange(0, 328)))
                t_old = t_new
            # executa a atualização das entidades
            for e in self.entities:
                e.update()
            # executa o teste de colisao
            self.collision_test()
            # remove as entidades que pediram para ser destruidas
            for e in self.destroy_list:
                self.entities.remove(e)
            # limpa a lista de entidades que devem ser destruidas
            self.destroy_list = []
            # inclui as entidades que devem ser adicionadas
            for e in self.include_list:
                self.entities.append(e)
            # limpa a lista de entidades que devem ser adicionadas
            self.include_list = []
            # executa o desenho das entidades
            self.screen.fill((0, 0, 128))
            for e in self.entities:
                e.draw()
            pygame.display.flip()
            # faz o programa aguardar 50 milissegundos
            pygame.time.wait(50)

    def collision_test(self):
        i = 0
        while i < len(self.entities):
            e1 = self.entities[i]
            j = i + 1
            while j < len(self.entities):
                e2 = self.entities[j]
                if e1.collision_mask & e2.collision_group != 0:
                    if e1.rect.colliderect(e2.rect):
                        e1.hit(e2)
                        e2.hit(e1)
                j += 1
            i += 1

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
        
    def destroy(self, e):
        self.destroy_list.append(e)
        
    def include(self, e):
        self.include_list.append(e)

if __name__ == "__main__":
    my_game = Game()
    my_game.setup()
    my_game.main_loop()
    my_game.shutdown()
