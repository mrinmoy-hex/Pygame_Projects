import pygame
import sys
from os.path import join
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, groups) -> None:
        super().__init__(groups)
        self.image = pygame.image.load("space_game/images/player.png").convert_alpha()
        self.rect = self.image.get_frect(center = (WIDTH / 2, HEIGHT /2))
        self.player_dir = pygame.math.Vector2()
        self.player_speed = 300
        
        # laser cooldown
        self.can_shoot = True
        self.laser_shot_time = 0
        self.cooldown_duration = 400 
        
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shot_time >= self.cooldown_duration:
                self.can_shoot = True
        
    def update(self, dt) -> None:
        keys = pygame.key.get_pressed()
        self.player_dir.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.player_dir.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.player_dir = self.player_dir.normalize() if self.player_dir else self.player_dir
        self.rect.center += self.player_dir * self.player_speed * dt
        
        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(lazer, self.rect.midtop, (all_sprites, lazer_sprite))     # same thing as in meteor sprite
            self.can_shoot = False 
            self.laser_shot_time = pygame.time.get_ticks()
            
        self.laser_timer()

    # for debugging player direction
    # print(player_dir) 

class Stars(pygame.sprite.Sprite):
    def __init__(self, groups, surf) -> None:
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = (random.randint(2, WIDTH - 23), random.randint(2, HEIGHT - 23)))

class Laser(pygame.sprite.Sprite):
    def __init__(self,surf, pos, groups) -> None:
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        
    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill() # kills the sprite after passed the window height

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups) -> None:
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center = pos) 
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(random.uniform(-0.5, 0.5), 1)
        self.speed = random.randint(400, 500)
        
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
            
def collisions():
    global running  # not an ideal approach, goona fix this later
    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True)
    if collision_sprites:
        running = False # ends the game if meteor strikes the player
    #print("Laser collision")
    for laser in lazer_sprite:
        collided_sprite = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprite:
            laser.kill()

def display_score ():
    current_time = pygame.time.get_ticks() // 100   # floor division for better score
    text_surf = font.render(str(current_time), True, (240, 240, 240))
    text_rect =text_surf.get_frect(midbottom = (WIDTH / 2, HEIGHT - 50))
    screen.blit(text_surf, text_rect)
    pygame.draw.rect(screen, (240, 240, 240), text_rect.inflate(20, 16).move(0, -8), 5, 10)
    
# general setup
pygame.init()
WIDTH = 1280
HEIGHT = 720
clock = pygame.time.Clock() # used for setting frame rate
running = True

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
lazer_sprite = pygame.sprite.Group()
# all_sprites.add(player) # not required as it's added in the group by init method

#import stuff
star_surf = pygame.image.load(join("space_game","images", "star.png")).convert_alpha()
meteor = pygame.image.load("space_game/images/meteor.png").convert_alpha()
lazer = pygame.image.load("space_game/images/laser.png").convert_alpha()
font = pygame.font.Font(join("space_game", "images", "Oxanium-Bold.ttf"), 40)

# sprites
for i in range(20):
    Stars(all_sprites, star_surf)
player = Player(all_sprites)


# meteor_rect = meteor.get_frect(center = (WIDTH / 2, HEIGHT /2))
# custom events -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while running:
    dt = clock.tick(120) / 1000    # delta time
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == meteor_event:
            x,y = random.randint(0, WIDTH), random.randint(-200, -100)
            Meteor(meteor, (x,y), (all_sprites, meteor_sprites))    # this thing give access to all meteor sprites
            
    all_sprites.update(dt)
    # collisions for sprites
    collisions()   
    screen.fill('#3a2e3f')  # hex color code for background
    # screen.blit(player.image, player.rect) Not an ideal approach
    all_sprites.draw(screen)
    display_score()
    
    pygame.display.update()


