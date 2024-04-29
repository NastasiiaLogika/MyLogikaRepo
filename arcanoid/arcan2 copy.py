import pygame
pygame.init()

#змінні, що відповідають за координати платформи
platform_x =200
platform_y =330
#змінні, відповідальні за напрями переміщення м'яча
dx =3
dy =3
#фраги, які відповідають за рух платформи вправо/ліворуч
move_right =False
move_left =False
back = (200,255,255)#колір фону (background)
mw = pygame.display.set_mode((800,600))#Вікно програми (main window)
mw.fill(back)
clock = pygame.time.Clock()


#прапор закінчення гри
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
        if event.type== pygame.QUIT:
            game_over =True
        if event.type== pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:#якщо натиснута клавіша
                move_right =True #піднімаємо прапор
            if event.key == pygame.K_LEFT:
                move_left =True #піднімаємо прапор
        elif event.type== pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right =False #опускаємо прапор
            if event.key == pygame.K_LEFT:
                move_left =False #опускаємо прапор
    
    if move_right:#прапор руху вправо
        platform.rect.x +=3
    if move_left:#прапор руху вліво
        platform.rect.x -=3
    #додаємо постійне прискорення м'ячу по x і y
        ball.rect.x += dx
    ball.rect.y += dy
    #якщо м'яч досягає меж екрана, міняємо напрямок його руху
    if ball.rect.y <0:
        dy *=-1
    if ball.rect.x >450 or ball.rect.x <0:
        dx *=-1
    #якщо м'яч торкнувся ракетки, міняємо напрямок руху
    if ball.rect.colliderect(platform.rect):
        dy *=-1
    for m in monsters:
        m.draw()
    platform.draw()
    ball.draw()
    pygame.display.update()
    clock.tick(40)