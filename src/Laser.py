import pygame

#class for player Laser
class Player_Laser():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    #Draws the laser
    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    #Moves the laser
    def move(self, vel):
        self.y -= vel

    #Collision detection
    def collision(obj1, obj2):
        offset_x = int(obj2.x) - int(obj1.x)
        offset_y = int(obj2.y) - int(obj1.y)
        return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None
    

#class for the lasers
class Enemy_Laser():
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    #draws the laser
    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    #moves the laser
    def move(self, vel):
        self.y += vel

    #collision detection
    def collision(obj1, obj2):
        offset_x = int(obj2.x) - int(obj1.x)
        offset_y = int(obj2.y) - int(obj1.y)
        return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None