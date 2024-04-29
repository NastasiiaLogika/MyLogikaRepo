from pygame import *


image_back = "background.jpg"
image_hero = "car.jpg"

class GamePlayer(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Spite.__init__(self)
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y)
        )
        self.speed = player_speed
        
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
        
    win_width = 700
    win_height = 500
    display.set_caption("Races")
    window = display.set_mode((win_width, win_height))
    background = transform.scale(image.load(image_back), (win_width, win_height))
    
    
    window.blit(background, (0,0))