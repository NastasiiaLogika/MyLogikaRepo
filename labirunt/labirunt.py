from pygame import *
'''Необхідні класи'''
 
#клас-батько для спрайтів
class GameSprite(sprite.Sprite):
    #конструктор класу
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        #кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        #кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def run(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y  > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 420:
            self.rect.y += self.speed
            
class Enemy(GameSprite):
    direction = "right"
    
    def run(self):
        if self.rect.x <= 470:
            self.direction = "right"
        if self.rect.x >= 620:
            self.direction = "left"
            
        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
            
            
class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, 
                 wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.wall_x = wall_x
        self.wall_y = wall_y
        self.wall_width = wall_width
        self.wall_height = wall_height
        
        self.image = Surface((wall_width, wall_height))
        self.image.fill((color_1, color_2, color_3))
        
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
        
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


 
#стіни
w1 = Wall(154, 205, 50, 100, 20, 450, 10)
w2 = Wall(154, 205, 50, 100, 480, 350, 10)
w3 = Wall(154, 205, 50, 100, 20, 10, 380)

font.init()
font = font.Font(None, 70)
win = font.render('You win!', True, (255, 215, 0))
lose = font.render('You Lose!', True, (255,215,0))

#Ігрова сцена:
win_width = 700
win_height = 500


window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("background.jpeg"), (win_width, win_height))

 
 
#Персонажі гри:
player = Player('sprite11.png', 5, win_height - 80, 4)
monster = Enemy('sprite22.png', win_width - 80, 280, 2)
final = GameSprite('sprite11.png', 700 - 120, 500 - 80, 0)
 
game = True
finish = False
clock = time.Clock()
FPS = 60

#музика
# mixer.init()
# mixer.music.load('jungles.ogg')
# mixer.music.play()
 
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False


#коли гра триває
    if finish != True:
        window.blit(background,(0, 0))
        player.reset()
        player.run()
        monster.reset()
        monster.run()
        final.reset()
    
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()

    display.update()
    clock.tick(FPS)