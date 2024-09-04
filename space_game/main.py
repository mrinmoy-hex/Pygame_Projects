import pygame
import sys
from os.path import join
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, groups) -> None:
        super().__init__(groups)
        self.image = pygame.image.load("space_game/images/player.png").convert_alpha()
        self.rect = self.image .get_frect(center = (WIDTH / 2, HEIGHT /2))
        self.player_dir = pygame.math.Vector2()
        self.player_speed = 300
        
    def update(self, dt) -> None:
        keys = pygame.key.get_pressed()
        self.player_dir.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.player_dir.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.player_dir = self.player_dir.normalize() if self.player_dir else self.player_dir
        self.rect.center += self.player_dir * self.player_speed * dt
        
        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE]:
            print("fire laser")

    # for debugging player direction
    # print(player_dir) 

class Stars(pygame.sprite.Sprite):
    def __init__(self, groups, surf) -> None:
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (random.randint(2, WIDTH - 23), random.randint(2, HEIGHT - 23)))

# general setup
pygame.init()
WIDTH = 1280
HEIGHT = 720
clock = pygame.time.Clock() # used for setting frame rate

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

all_sprites = pygame.sprite.Group()
# all_sprites.add(player) # not required as it's added in the group by init method
star_surf = pygame.image.load(join("space_game","images", "star.png")).convert_alpha()
for i in range(20):
    Stars(all_sprites, star_surf)
player = Player(all_sprites)

meteor = pygame.image.load("space_game/images/meteor.png").convert_alpha()
meteor_rect = meteor.get_frect(center = (WIDTH / 2, HEIGHT /2))

lazer = pygame.image.load("space_game/images/laser.png").convert_alpha()
lazer_rect = lazer.get_frect(bottomleft = (20, HEIGHT - 20))


while True:
    dt = clock.tick(120) / 1000    # delta time
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    all_sprites.update(dt)
       
    screen.fill('darkgray')
    # screen.blit(player.image, player.rect) Not an ideal approach
    all_sprites.draw(screen)
    
    pygame.display.update()


