import os
import pygame
import random
from Laser import Enemy_Laser

#enemies
blue_enemy = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
red_enemy = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
green_enemy = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
#end of enemies

#start of shots
blue_laser = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
red_laser = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
green_laser = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
#end of shots

size = width, height = 720, 540

#This is the class for the main enemy
class Enemy_Ship():
    colour_map = {

    "red": (red_enemy, red_laser),
    "blue": (blue_enemy, blue_laser),
    "green": (green_enemy, green_laser)

    #This is the map for the colours of the enemy, it gets randomized
    }

    #initiation of the enemy
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.lasers = []
        self.ship_img, self.laser_img = self.colour_map[random.choice(["red", "blue", "green"])]
        self.cool_down_counter = 0
        self.mask = pygame.mask.from_surface(self.ship_img)
        #basic initiation E.G where the ship spawns, its health, the lasers etc

    #draws the surface onto the screen
    def draw(self, screen):
        screen.blit(self.ship_img, (self.x, self.y))

    #gets width    
    def get_width(self):
        return self.ship_img.get_width()
    
    #gets height    
    def get_height(self):
        return self.ship_img.get_height()
        
    #moves the surface down the screen
    def move(self, vel):
        self.y += vel
        
    #Adds 1 fatality from total Fatalities if enemy gets past
    def life_loss(self, y, Fatalities):
        if self.y < height:
            Fatalities += 1
        
    #shoots the laser from the enemy
    def shoot(self, laser_vel, shoot_speed):
        if self.cool_down_counter == 60:
            laser = Enemy_Laser(self.x - (self.get_width()/2), self.y + 10, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter -= 60

        for laser in self.lasers:
            laser.move(laser_vel)
            if laser.y < -50:
                self.lasers.remove(laser)

    #collision detection for player
    def laser_hit_player(self, player):
        for laser in self.lasers:
            if laser.collision(player):
                player.health -= 10
                self.lasers.remove(laser)


