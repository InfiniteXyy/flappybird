from sys import exit
import random
import pygame
from pygame.locals import *


# configure
screen_w = 288
screen_h = 512

# class bird
class Bird(pygame.sprite.Sprite):
    def __init__(self, bird_img, bird_sounds, pos):
        pygame.sprite.Sprite.__init__(self) 
        self.images = bird_img
        self.sounds = bird_sounds
        self.rect = self.images[0].get_rect()
        self.rect.midbottom = pos
        self.speed = 1
        self.a = 0.2
        self.angle = 0
        self.is_hit = False
    def move(self):
        self.rect.top += self.speed
        self.speed += self.a
        if self.speed >= 0:
            self.angle -= 2
    def click(self):
        self.sounds[0].play()
        self.speed = -4
        self.angle = 18
    def die(self):
        self.sounds[1].play()
        self.sounds[2].play()
        self.is_hit = True
        
            
# class pipe
class Pipe(pygame.sprite.Sprite):
    def __init__(self, pipe_img, pos, num):
        pygame.sprite.Sprite.__init__(self)
        self.image = pipe_img
        self.rect = self.image.get_rect()
        self.rect.top = pos
        self.rect.left = 288 + 144*num
    def move(self):
        self.rect.left -=1
    def change(self):
        self.rect.left = 288
        self.rect.top = random.randint(-240, -100)
# init the game
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((screen_w,screen_h))
pygame.display.set_caption('flappy bird')


# load img
bg_img = pygame.image.load("../flappybird/bg_day.png").convert_alpha()
land_img = pygame.image.load("../flappybird/land.png").convert_alpha()

# load sound 0:wing 1:hit 2:die 3:point 4:swooshing
bird_sounds = []
bird_sounds.append(pygame.mixer.Sound("../flappybird/flappybirdmusic/sfx_wing.ogg"))
bird_sounds.append(pygame.mixer.Sound("../flappybird/flappybirdmusic/sfx_hit.ogg"))
bird_sounds.append(pygame.mixer.Sound("../flappybird/flappybirdmusic/sfx_die.ogg"))
bird_sounds.append(pygame.mixer.Sound("../flappybird/flappybirdmusic/sfx_point.ogg"))
bird_sounds.append(pygame.mixer.Sound("../flappybird/flappybirdmusic/sfx_swooshing.ogg"))
for i in bird_sounds:
    i.set_volume(0.1)
    
# config fonts

fonts = []
for i in range(48, 58):
    name = "../flappybird/font_0" + str(i) + ".png"
    fonts.append(pygame.image.load(name).convert_alpha())
def set_score():
    temp = str(score)
    flag = len(temp)
    for i in range(flag):     
        screen.blit(fonts[int(temp[i])], (144 + i * 24 - 12 * flag, 20))

# config bird

bird_imgs = []
bird_imgs.append(pygame.image.load("../flappybird/bird0_0.png").convert_alpha())
bird_imgs.append(pygame.image.load("../flappybird/bird0_1.png").convert_alpha())
bird_imgs.append(pygame.image.load("../flappybird/bird0_2.png").convert_alpha())
bird_pos = [100, 230]

bird = Bird(bird_imgs, bird_sounds, bird_pos)

# config pipe

pipe_img = pygame.image.load("../flappybird/pipes.png").convert_alpha()

pipe = []
for i in range(3):
    pipe_pos = random.randint(-260, -80)
    pipe.append(Pipe(pipe_img, pipe_pos, i))

# config the game
score = 0
clock = pygame.time.Clock()
running = True
index = 0
delay = 0
bg_x = 0
pipe_delay = 0
pipe_flag = 0
delay_num = 144
game_start_delay = 0
pipe_delay_start = False
while running:
    if not bird.is_hit:
    # get event      
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                bird.click()
        for one_pipe in pipe:
            if one_pipe.rect.left <= 114 and one_pipe.rect.left >= 34:
                if bird.rect.top < one_pipe.rect.top + 305 or bird.rect.bottom > one_pipe.rect.top + 420:
                    bird.die()
                elif one_pipe.rect.left == 100:
                    bird.sounds[3].play()
                    score += 1
        if bird.rect.top >= 357:
            bird.die()
        game_start_delay += 1
        if game_start_delay == 288:
            pipe_delay_start = True
        bg_x = (bg_x + 1) % screen_w
        delay = (delay + 1) % 6
        if delay == 1:
            index = (index + 1) % 3
        if pipe_delay_start:
            pipe_delay = (pipe_delay + 1) % delay_num
            if pipe_delay == 0:
                pipe[pipe_flag].change()
                pipe_flag = (pipe_flag + 1) % 3
        clock.tick(60)
        bird.move()
        for x in pipe:
            x.move()
# game over
    else:
        if bird.rect.top <= 357:
            bird.rect.top += 4
            bird.angle += 3
            clock.tick(60)
        else:
            pygame.quit()
            exit()
# image blit
    screen.blit(bg_img,(-bg_x, 0))  
    screen.blit(bg_img,(screen_w-bg_x, 0))
    for i in range(3):
        screen.blit(pipe[i].image, pipe[i].rect)
    screen.blit(land_img, (-bg_x, 400))
    screen.blit(land_img, (screen_w-bg_x, 400))
    
    rotated_bird = pygame.transform.rotate(bird.images[index], bird.angle)
    screen.blit(rotated_bird, bird.rect)
    set_score()
    pygame.display.flip()
