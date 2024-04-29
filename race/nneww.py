from pygame import *
from random import randint

# ініціалізація Pygame
init()

# шрифти і написи
font.init()
font2 = font.Font(None, 36)

# налаштування вікна
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")

# навантаження зображень
img_back = "road.jpg"  # фон гри
img_hero = "car-d.png"  # герой
img_enemy = "car2.png"  # ворог

# клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# клас головного гравця
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

# клас ворога
class Enemy(GameSprite):
    collisions = 0  # лічильник зіткнень

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0

# функція завершення гри
def finish_game():
    global finish
    finish = True
    window.fill((0, 0, 0))
    text = font2.render("Game Over", 1, (255, 255, 255))
    window.blit(text, (250, 200))
    display.update()
    time.delay(2000)
 



# Основний цикл гри
while True:
    
    
    # навантаження зображень
    background = transform.scale(image.load(img_back), (win_width, win_height))

    # створення спрайтів
    ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
    monsters = sprite.Group()
    for i in range(1, 7):
        monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 90, 90, randint(1, 10))
        monsters.add(monster)

    run = True
    finish = False
    
    while run:
        for e in event.get():
            if e.type == QUIT:
                run = False

        if not finish:
            # обновлення екрану
            window.blit(background, (0, 0))
            
            # керування гравцем
            ship.update()
            ship.reset()
            
            # керування ворогами
            monsters.update()
            monsters.draw(window)
            
            # відображення результатів
            text = font2.render("Зіткнень: " + str(Enemy.collisions), 1, (255, 255, 255))
            window.blit(text, (10, 20))
            display.update()
            
            # Перевірка зіткнень корабля з ворогами
            if sprite.spritecollide(ship, monsters, True):
                # Якщо є зіткнення, збільшити лічильник зіткнень
                Enemy.collisions += 1
                if Enemy.collisions >= 5:
                    finish_game()
                    Enemy.collisions = 0
            
            # затримка
            time.delay(50)
        else:
            break  # Вихід з циклу, коли гра завершена
