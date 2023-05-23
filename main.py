import pygame
import random
pygame.init()

s_width = 500
s_height = 300

screen = pygame.display.set_mode((s_width, s_height))
clock = pygame.time.Clock()

white = (255,255,255)
black = (0,0,0)


    
class Player(pygame.sprite.Sprite):
  def __init__(self, image):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.transform.scale(image, (50,50))
    self.rect = self.image.get_rect()
    self.rect.bottomleft = (0, s_height)

  def update(self):
    #Movement Keybinds for Player Here
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_w]:
      self.rect.y -= 5
    if keystate[pygame.K_a]:
      self.rect.x -= 5
    if keystate[pygame.K_s]:
      self.rect.y += 5
    if keystate[pygame.K_d]:
      self.rect.x += 5

    #Prevents player from leaving boundary
    if self.rect.left <= 0:
      self.rect.left = 0
    if self.rect.bottom >= s_height:
      self.rect.bottom = s_height
    if self.rect.top <= 0:
      self.rect.top = 0
    if self.rect.right >= s_width:
      self.rect.right = s_width

class Enemy(pygame.sprite.Sprite):
  def __init__(self, image, x , y):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.transform.scale(image, (50,50))
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)
    self.speed = 1

  def update(self, target):
    if self.rect.x > target.rect.x:
      #Fill in code here
      self.rect.x-= self.speed
    else:
      self.rect.x += self.speed

    if self.rect.y > target.rect.y:
      #Fill in code here
      self.rect.y -= self.speed
    else:
      self.rect.y += self.speed

def draw_text(color, text, font, size, x, y, surface):
  font_name = pygame.font.match_font(font)
  Font = pygame.font.Font(font_name, size)
  text_surface = Font.render(text, True, color)
  text_rect = text_surface.get_rect()
  text_rect.center = (x,y)
  surface.blit(text_surface,text_rect)
  
    
    
#IMPORT IMAGES:
player_img = pygame.image.load("monkey.png").convert()
enemy_img = pygame.image.load("shark.png").convert()


#CREATING SPRITE GROUPS:
playerSprites = pygame.sprite.Group()
enemySprites = pygame.sprite.Group()

#CREATING OBJECTS:
player = Player(player_img)
enemy1 = Enemy(enemy_img, s_width, s_height/2)

#ADD OBJECTS TO GROUPS:
playerSprites.add(player)
enemySprites.add(enemy1)

time = 0
reset = 0
game_state = "Play"
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      quit()

  if game_state == "Lose":
    #BLIT GAMEOVER BACKGROUND TO SCREEN
    draw_text((30,0,255), 'Game Over', 'comic sans ms', 75, 200, 125, screen)   
  else:
    screen.fill((255,153,51))
    
    #Collisions Here
    collisions = pygame.sprite.spritecollide(player, enemySprites, False)
    for c in collisions:
      print("GAME OVER")
      game_state = "Lose"
    screen.fill((255,153,51))
  
    #TIMER FOR PLAYER:
    time = pygame.time.get_ticks()/1000
    draw_text(black, "Score: "+ str(time) + " seconds", "arial", 18, 110, 20, screen )
    
    #TEN SECOND TIMER FOR ENEMY:
    milliseconds = pygame.time.get_ticks() - reset
    if milliseconds >= 10000:
      reset+= 10000
      enemy = Enemy(enemy_img, random.randint(0,s_width), random.randint(0,s_height))
      enemySprites.add(enemy)
    
    #DRAWING TO SCREEN:
    playerSprites.draw(screen)
    enemySprites.draw(screen)
  
    #UPDATE GROUPS:
    playerSprites.update()
    enemySprites.update(player)
  
    
  clock.tick(40)
  pygame.display.update()