import pygame
import sys
from os.path import join
import random

# general setup
pygame.init()
WIDTH = 1280
HEIGHT = 720
clock = pygame.time.Clock() # used for setting frame rate

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

surf = pygame.Surface((100, 200))
surf.fill('orange')
x = 100

# importing an image
player = pygame.image.load("images/player.png").convert_alpha()
player_rect = player.get_frect(center = (WIDTH / 2, HEIGHT /2))
player_dir = pygame.math.Vector2(1, -1)
# print(player_dir)
player_speed = 300

stars = pygame.image.load(join("images", "star.png")).convert_alpha()

meteor = pygame.image.load("images/meteor.png").convert_alpha()
meteor_rect = meteor.get_frect(center = (WIDTH / 2, HEIGHT /2))

lazer = pygame.image.load("images/laser.png").convert_alpha()
lazer_rect = lazer.get_frect(bottomleft = (20, HEIGHT - 20))

star_pos = [(random.randint(2, WIDTH - 23), random.randint(2, HEIGHT - 23)) for _ in range(20)] 

while True:
    dt = clock.tick(120) / 1000    # delta time
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # draw the game
    screen.fill('darkgray')
    
    # draw stars
    for pos in star_pos:        
        screen.blit(stars, pos) 
                
    screen.blit(player, player_rect)
    # player_rect.x += 50
    # player_rect.y -= 50

    if player_rect.top < 0 or player_rect.bottom > HEIGHT:
        player_dir.y *= -1
    if player_rect.right > WIDTH or player_rect.left < 0:
        player_dir.x *= -1
    
    player_rect.center += player_dir * player_speed * dt
    screen.blit(lazer, lazer_rect)
    screen.blit(meteor, meteor_rect)
    
    pygame.display.update()


