#Создай собственный Шутер!

from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y,  player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        windows.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Enamy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


win_width = 700
win_height = 500
display.set_caption('Shooter')
windows = display.set_mode((win_width, win_height))
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire_sound  = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('AGENCYB.ttf' , 80)
font2 = font.SysFont('AGENCYBR.ttf' , 36)

win = font1.render('YOU WIN!', True, (0,255,0))
lose = font1.render('YOU LOSE(', False, (255,0,0))


calc = 0


finish = False

ship = Player('rocket.png', 5, win_height - 100, 80, 100, 15)

game = True

enemyS = sprite.Group()
for i in range(7):
    enemy = Enamy('asteroid.png', randint(30, 670), randint(-100, -20), 40, 50, randint(1, 5))
    enemyS.add(enemy)

lost = 0

bullets = sprite.Group()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
                fire_sound.play()
    if not finish:
        windows.blit(background, (0,0))
        text = font2.render('Счёт:'+ str(calc), True, (255,255,255))
        windows.blit(text, (20,20))
        text1 = font2.render('Пропущено:'+ str(lost), True, (255,255,255))
        windows.blit(text1, (20,50))
        ship.update()
        ship.reset()
        enemyS.update()
        enemyS.draw(windows)
        bullets.draw(windows)
        bullets.update()
        sprites_lists = sprite.spritecollide(
            ship, enemyS, True
        )
        sprites_list = sprite.groupcollide(
             enemyS, bullets, True, True
        )
        if sprites_lists or lost == 3:
            finish = True
            windows.blit(lose,(200, 200) )

        if calc == 100:
            finish = True
            windows.blit(win,(200, 200) )

        if sprites_list:
            calc += 1
            enemy = Enamy('asteroid.png', randint(30, 670), randint(-100, -20), 40, 50, randint(1, 5))
            enemyS.add(enemy)
            



    
    
    display.update()
    time.delay(50)