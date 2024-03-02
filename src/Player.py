import os
import pygame
from Laser import Player_Laser

#player
pixel_ship = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))
small_pixel_ship = pygame.transform.scale(pixel_ship, (50, 50))
pixel_ship_shoot = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))
#end of player


#Class for player
class Player_Ship():
   
    #Initialization for Player
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = small_pixel_ship
        self.ship_laser = pixel_ship_shoot
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.cool_down_counter = 0
        self.lasers = []

    #Function to draw the player
    def draw(self, screen):
        health_percentage = self.health / 100
        screen.blit(self.ship_img, (self.x, self.y))
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y + self.get_height() + 10, self.get_width(), 10))
        if self.health > 0:
            pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y + self.get_height() + 10,
                                                 self.get_width() * health_percentage, 10))

    #Helper Function to get the width of the player ship img
    def get_width(self):
        return self.ship_img.get_width()

    #Helper Function to get the height of the player ship img
    def get_height(self):
        return self.ship_img.get_height()

    #shoots projectiles fronm the ship
    def shoot(self, laser_vel, Fatalities, shoot_speed):
        if self.cool_down_counter == 20 and Fatalities < 5 and self.health > 0:
            laser = Player_Laser(self.x - self.get_width() / 2, self.y - 10, self.ship_laser)
            self.lasers.append(laser)
            self.cool_down_counter -= 20

    #Function to move the laser
    def move_laser(self, laser_vel):
        for laser in self.lasers:
            laser.move(laser_vel)
            if laser.y < -50:
                self.lasers.remove(laser)

    #Collision detection for enemy
    def laser_hit_enemy(self, enemies):
        for enemy in enemies:
            for laser in self.lasers:
                if laser.collision(enemy):
                    enemies.remove(enemy)
                    self.lasers.remove(laser)



