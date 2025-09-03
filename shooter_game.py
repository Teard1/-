from pygame import *
from random import *
import sys
import pygame
from time import time as timer
win_width = 700
win_height = 500
window = display.set_mode((win_width,win_height))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"),(win_width,win_height))
clock = time.Clock()
mixer.init()
mixer.music.load("space.ogg")
mixer_music.play()
lost = 0
score = 0
class GameSprite(sprite.Sprite):
    def __init__(self,image_path,x,y,size_x,size_y,speed=0):
        super().__init__()
        self.image = transform.scale(image.load(image_path),(size_x,size_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.x = randint(0,620)
            self.rect.y  = -40
            lost +=1

class Bullet(GameSprite):
    def update(self):
        
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
        
class Player(GameSprite):
    
    def update(self,keys):
        if keys[K_LEFT]and self.rect.x >0:
            self.rect.x -= self.speed
        if keys[K_RIGHT]and self.rect.x < 635:
            self.rect.x += self.speed
    def fire(self):
        xx = self.rect.x + 30
        bullet = Bullet("bullet.png",xx,self.rect.y,5,10,3)
        bullets.add(bullet)
        

class Asterid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.x = randint(0,620)
            self.rect.y  = -40
            


asteroids = sprite.Group()
monsters = sprite.Group()
for i in range(5):
    monster = Enemy("ufo.png",randint(200,650),-20,65,65,randint(1,3))
    monsters.add(monster)
for i in range(3):
    asterid = Asterid("asteroid.png",randint(100,650),-20,65,65,randint(1,3))
    asteroids.add(asterid)
player = Player("rocket.png",350,430,65,65,5)
z = 0
c = 255
font.init()
font1 = font.SysFont(None,40)
font2 = font.SysFont(None,100)
fire_sound = mixer.Sound("fire.ogg")

bullets = sprite.Group()

fire_num = 0
relad = False
heart = 3
game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE and finish != True:
                if fire_num < 8 and relad != True:
                    fire_num +=1
                    player.fire()
                    fire_sound.play()
                if fire_num  >= 8 and relad != True:
                    lat_time = timer()
                    relad =True
    keys = key.get_pressed()
    player.update(keys)
    monsters.update()
    bullets.update()
    asteroids.update()
    if finish != True:
        
        window.blit(background,(0,0))

        if relad  == True:
            now_time = timer()
            if now_time - lat_time < 3:
                reload  = font1.render("Wait, reload...",1 ,(150,0,0))
                window.blit(reload,(260,460))
            else:
                fire_num = 0
                relad = False


        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        player.reset()

        text_lost = font1.render("Пропущено: "+ str(lost),1,"white")
        text_score = font1.render("Cчет: "+ str(score),1,"white")

        window.blit(text_lost,(10,10))
        window.blit(text_score,(10,40))

        text_heart = font2.render(str(heart),1,(z,c,0))
        window.blit(text_heart,(650,10))

        if sprite.spritecollide(player,monsters,True):
            monster = Enemy("ufo.png",randint(200,650),-20,65,65,randint(1,3))
            monsters.add(monster)
            heart = int(heart)
            heart -= 1
            z += 100
            c -= 100
        if sprite.spritecollide(player,asteroids,True):
            asterid = Asterid("asteroid.png",randint(100,650),-20,65,65,randint(1,3))
            asteroids.add(asterid)
            heart = int(heart)
            heart -= 1
            z += 100
            c -= 100
        if sprite.groupcollide(monsters,bullets,True,True):
            score +=1
            monster = Enemy("ufo.png",randint(200,650),-20,65,65,randint(1,5))
            monsters.add(monster)

        if int(heart)<= 0  or lost >= 5:
            finish = True
            text_lose= font1.render("LOSE",1,"red")
            window.blit(text_lose,(350,250))

        if score >= 10:
            finish = True
            text_win= font1.render("WIN",1,"yellow")
            window.blit(text_win,(350,250))
        

        display.update()
        clock.tick(40)