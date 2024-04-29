import pygame
pygame.init()


back = (200, 255, 255)
mw = pygame.display.set_mode((800, 600))
mw.fill(back)
clock = pygame.time.Clock()
dx = 3
dy = 3


platform_x = 200
platform_y = 330
move_right = False
move_left = False
game_over = False


#клас із попереднього проекту
class Area():
    def __init__(self, x=0, y=0, width =10, height =10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = back
        if color:
            self.fill_color = color


    def color(self, new_color):
        self.fill_color = new_color


    def fill(self):
        pygame.draw.rect(mw,self.fill_color,self.rect)


    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)


    def colliderect(self, rect):
        return self.rect.colliderect(rect)


class Label(Area):
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)
    def draw(self, shift_x=0, shift_y=0):
        self.fill()
        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))



#клас для об'єктів-картинок
class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10):
         Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
         self.image = pygame.image.load(filename).convert_alpha()  # Додайте convert_alpha() для правильного відображення з прозорістю

    def draw(self):
        # Змініть розмір малюнка, використовуючи розміри, передані у конструкторі
        scaled_image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        mw.blit(scaled_image, (self.rect.x, self.rect.y))


#створення м'яча та платформи
ball = Picture('ball-r.png',160,200,50,50)
platform = Picture('platform-r.png', platform_x, platform_y,100,30)


#Створення ворогів
start_x =5 #координати створення першого монстра
start_y =5
count =9 #кількість монстрів у верхньому ряду
monsters = []#список для зберігання об'єктів-монстрів
for j in range(3):#цикл по стовпцях
    y = start_y + (55* j)#координата монстра у кожному слід. стовпці буде зміщена на 55 пікселів по y
    x = start_x + (27.5* j)#і 27.5 по x
    for i in range(count):#цикл по рядах(рядків) створює в рядку кількість монстрів,що дорівнює count
        d = Picture ('enemy.png', x, y, 80,40)#створюємо монстра
        monsters.append(d)#додаємо до списку
        x = x + 90 #збільшуємо координату наступного монстра
    count = count -1 #для наступного ряду зменшуємо кількість монстрів


while not game_over:
    ball.fill()
    platform.fill()
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_LEFT:
                move_left = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right = False
            if event.key == pygame.K_LEFT:
                move_left = False
        
    if move_right:
        platform.rect.x +=3
    if move_left:
        platform.rect.x -=3
    ball.rect.x += dx
    ball.rect.y += dy
    if  ball.rect.y < 0:
        dy *= -1
    if ball.rect.x > 450 or ball.rect.x < 0:
        dx *= -1
    if ball.rect.y > 350:
        time_text = Label(150,150,50,50,back)
        time_text.set_text('YOU LOSE',60, (255,0,0))
        time_text.draw(10, 10)
        game_over = True
    if len(monsters) == 0:
        time_text = Label(150,150,50,50,back)
        time_text.set_text('YOU WIN',60, (0,200,0))
        time_text.draw(10, 10)
        game_over = True
    if ball.rect.colliderect(platform.rect):
        dy *= -1
    for m in monsters:
        m.draw()
        #якщо монстра торкнувся м'яч, видаляємо монстра зі списку та міняємо напрямки руху м'яча
        if m.rect.colliderect(ball.rect):
            monsters.remove(m)
            m.fill()
            dy *= -1
    platform.draw()
    ball.draw()
    pygame.display.update()
    clock.tick(40)