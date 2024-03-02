import pygame
import os
import random
import ctypes
from Player import Player_Ship
from Enemy import Enemy_Ship, Enemy_Laser

pygame.init()
BG = pygame.image.load(os.path.join("assets", "background-black.png")) #background for game

#main player
pixel_ship = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))
small_pixel_ship = pygame.transform.scale(pixel_ship, (50, 50))
pixel_ship_shoot = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))
#end of main player

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

pygame.key.set_repeat(20,20) #This is for keys that are pressed, and have to be repeated
user32 = ctypes.windll.user32
size1 = width1, height1 = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1) - 70 #size of window
size = width, height = 720, 540
BG_bigger = pygame.transform.scale(BG, (size)) #makes background fit the window
pygame.display.set_caption("Space Cringe") #space cringe, haha




#main program
def main():
    speed = 8
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    Fatalities = 0
    x = width/2 - small_pixel_ship.get_width()/2
    y = height-100
    level = 0
    wave_length = 3
    enemy_vel = 0.5
    laser_vel = 5
    level_cooldown = 0
    game_break = True
    main_font = pygame.font.SysFont("bahnschrift", 25)
    run = True
    fps = 60
    shoot_speed = 10
    clock = pygame.time.Clock() #
    main_player = Player_Ship(x,y) #Creates the main player from the class
    enemies = [] #stores the enemies on screen
    game_over_counter = 0


    #This section is for the game over text
    game_over_font = pygame.font.SysFont("bahnschrift", 50) #Game over font
    game_over = 'Game over, you lose n00b' #Game over text
    game_over_label = (game_over_font.render(f"{game_over}", 1, (255,255,255))) #Game over label that can be rendered onto the window

    cringe_text_lib = {

    "1": ('Goodluck, you will need it'),
    "2": ('Wow, you really are a terrible'),
    "3": ('If you die now, uninstall the game and never play again'),
    "4": ('Did you know I made this game? I am so cool, I am the best')
    }



    cringe_text_label = (main_font.render(cringe_text_lib[random.choice(["1", "2", "3", "4"])], 1, (255,255,255)))


    while run:

        level_label = (main_font.render(f"Level = {level}", 1, (255,255,255))) #generates a label for the level
        Fatalities_label = (main_font.render(f"Fatalities = {Fatalities}", 1, (255,255,255))) #generates a label for Fatalities left
        new_round = 'Next round = {0}, there will be {1} enemies'.format(level + 1, wave_length + 1)
        new_round_label = (main_font.render(new_round, 1, (255,255,255)))
        clock.tick(fps) #refreshes the screen 60 times per second (when fps = 60)



        # This is the round logic, if game_break is = True, game will be on break, otherwise, it will not

        if len(enemies) == 0 and Fatalities < 5 and main_player.health > 0: # If there are no enemies and player still has Fatalities and health left
            level_cooldown += 1 # Level_cooldown will be icnremented by 60 times a second
            if level_cooldown >= 240: # If level_cooldown is 240, or if 3 seconds pass then:
                game_break = False # The game will resume and the break will be over
                level_cooldown -= 240 # The level_cooldown will reset
            elif level_cooldown < 240: # However if 3 seconds have not passed, then the game_break = True
                game_break = True # Or in otherwords, the game is still on a break
            if game_break == False: # game_break = False means the break is over
                level += 1
                wave_length += 1
                enemy_vel += 0.5

                # This creates an enemy according to the wavelength
                for i in range(0, wave_length):
                    enemy = Enemy_Ship(random.randrange(0, width-100), random.randrange(-500, -30))
                    enemies.append(enemy)

        # End of round logic

        # This is the enemy logic
        for enemy in enemies:
            enemy.cool_down_counter += 1
            enemy.move(enemy_vel)
            if enemy.y - 10 > height and Fatalities < 5:
                Fatalities += 1
                enemies.remove(enemy)
            enemy.shoot(laser_vel, shoot_speed)
            enemy.laser_hit_player(main_player)
        # End of enemy logic

        # This shoots the laser and moves it
        if game_break == False:
            main_player.cool_down_counter += 1 #This is the cooldown for the player, if it is equal to 15, player will shoot
            main_player.shoot(laser_vel, Fatalities, shoot_speed) #This is the shooting method being called
            main_player.laser_hit_enemy(enemies)
        main_player.move_laser(laser_vel)
        # End of main player laser

        # This is the Fatalities and health logic
        if Fatalities == 5 or main_player.health == 0:
            for enemy in enemies:
                enemies.remove(enemy)
                for laser in enemy.lasers:
                    enemy.lasers.remove(laser)
            for laser in main_player.lasers:
                main_player.lasers.remove(laser)
            game_over_counter += 1
            if game_over_counter == 90:
                run = False
        # End of Fatalities and health logic



        #Fix key and mouse functionality
        #this is to turn button presses into an action
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()

            if event.type == pygame.QUIT:
                run = False

            if keys[pygame.K_a] and main_player.x > 10:
                main_player.x -= speed
            if keys[pygame.K_d] or keys[pygame.K_RIGHT] and main_player.x < width - main_player.get_width() - 10:
                main_player.x += speed
            if keys[pygame.K_w] or keys[pygame.K_UP] and main_player.y > 10:
                main_player.y -= speed
            if keys[pygame.K_s] or keys[pygame.K_DOWN] and main_player.y < height - main_player.get_height() - 10:
                main_player.y += speed
            if keys[pygame.K_ESCAPE]:
                run = False


        #start of the function that draws everything onto the window
        def redraw_win():
            screen.blit(BG_bigger, (0,0))
            screen.blit(Fatalities_label, (10, 10))
            screen.blit(level_label, (10, level_label.get_height()+10))
    
            # Get the current position of the cursor
            cursor_position = pygame.mouse.get_pos()

            # Set the new position of the spaceship based on the cursor position
            main_player.x = cursor_position[0] - main_player.get_width() + 25
            main_player.y = cursor_position[1] - main_player.get_height() + 25

            if Fatalities == 5 or main_player.health == 0:
                screen.blit(game_over_label, (width/2 - game_over_label.get_width()/2, height/2))

            if game_break == True:
                screen.blit(new_round_label, (width/2 - new_round_label.get_width()/2, height/2))

                if level == 0:
                    screen.blit(cringe_text_label, (width/2 - cringe_text_label.get_width()/2, height/2 + 20))

            for enemy in enemies:
                enemy.draw(screen)
                for laser in enemy.lasers:
                    laser.draw(screen)

            for laser in main_player.lasers:
                laser.draw(screen)

            main_player.draw(screen)
        #End of the function


            pygame.display.update() #refreshes the screen
        redraw_win() #calls function that draws everything
main() #calls main program
