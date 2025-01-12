import pygame
import os

pygame.font.init()

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

WIDTH , HEIGHT = 700,600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('python game!')

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

HEALTH_FONT= pygame.font.SysFont('comicsans',40)
WINNER_FONT = pygame.font.SysFont('comicsans',100)

FPS = 60
SPACESHIP_WIDTH = 55
SPACESHIP_HEIGHT = 40

BORDER = pygame.Rect((WIDTH +10)//2 - 5,0,10,HEIGHT)
VEL = 6

BULLET_VEL = 7

MAX_BULLETS = 3
YELLOW_BULLET = []
RED_BULLET = []
RED_HEALTH = 10
YELLOW_HEALTH = 10

ASSETS_PATH = 'C:\\Users\\anves\\Downloads\\PygameForBeginners-main\\PygameForBeginners-main\\Assets'


YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join(ASSETS_PATH,'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join(ASSETS_PATH,'spaceship_red.png'))	
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),270)

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join(ASSETS_PATH ,'space.png')),(WIDTH,HEIGHT))

def draw_window(red, yellow,RED_BULLET,YELLOW_BULLET,red_health,yellow_health):

	WIN.fill(WHITE)
	WIN.blit(BACKGROUND,(0,0))
	pygame.draw.rect(WIN,BLACK,BORDER)

	red_health_text = HEALTH_FONT.render('Health: ' + str(red_health),1,WHITE)
	yellow_health_text = HEALTH_FONT.render('Health: ' + str(yellow_health),1,WHITE)
	WIN.blit(red_health_text,(WIDTH - red_health_text.get_width() -10,10))
	WIN.blit(yellow_health_text,(10,10))

	WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
	WIN.blit(RED_SPACESHIP,(red.x,red.y))

	for bullets in RED_BULLET:
	   pygame.draw.rect(WIN,RED,bullets)

	for bullets in YELLOW_BULLET:
	   pygame.draw.rect(WIN,YELLOW,bullets)


	pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # left
        yellow.x -= VEL
    elif keys_pressed[pygame.K_d]and yellow.x + VEL + yellow.width < BORDER.x :  # right
        yellow.x += VEL
    elif keys_pressed[pygame.K_w] and yellow.y -VEL > 0:  # up
        yellow.y -= VEL
    elif keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height + 15 < HEIGHT:  # down
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x -VEL > BORDER.x + 25:  # left
        red.x -= VEL
    elif keys_pressed[pygame.K_RIGHT]and red.x + VEL +red.width < WIDTH:  # right
        red.x += VEL
    elif keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # up
        red.y -= VEL
    elif keys_pressed[pygame.K_DOWN] and red.y + VEL +red.height + 15 < HEIGHT:  # down
        red.y += VEL


def handle_bullets(YELLOW_BULLET,RED_BULLET,yellow,red):
	for bullet in YELLOW_BULLET:
		bullet.x += BULLET_VEL
		if red.colliderect(bullet):
			pygame.event.post(pygame.event.Event(RED_HIT))
			YELLOW_BULLET.remove(bullet)
		elif bullet.x> WIDTH:
			YELLOW_BULLET.remove(bullet)


	for bullet in RED_BULLET:
		bullet.x -= BULLET_VEL
		if yellow.colliderect(bullet):
			pygame.event.post(pygame.event.Event(YELLOW_HIT))
			RED_BULLET.remove(bullet)
		elif bullet.x < 0:
			RED_BULLET.remove(bullet)

def draw_winner(text):
	draw_text = WINNER_FONT.render(text,1,WHITE)
	WIN.blit(draw_text,(WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))

	pygame.display.update()
	pygame.time.delay(5000)

def main():

   global RED_HEALTH, YELLOW_HEALTH,RED_BULLET,YELLOW_BULLET

   red = pygame.Rect(600,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
   yellow = pygame.Rect(100,300,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)

   clock = pygame.time.Clock()
   run = True
   while run:
        clock.tick(FPS) 

        for event in pygame.event.get():
           if event.type == pygame.QUIT:
             run = False
             

           if event.type == pygame.KEYDOWN:
           	  if event.key == pygame.K_LCTRL and len(YELLOW_BULLET) < MAX_BULLETS:
           	  	bullet = pygame.Rect(yellow.x + yellow.width , yellow.y + yellow.height//2 - 3, 10,5)
           	  	YELLOW_BULLET.append(bullet)

           	  if event.key == pygame.K_RCTRL and len(RED_BULLET) < MAX_BULLETS:
           	  	bullet = pygame.Rect(red.x , red.y + red.height//2 - 3, 10,5)
           	  	RED_BULLET.append(bullet)

           if event.type == RED_HIT:
           	    RED_HEALTH -= 1
           if event.type == YELLOW_HIT:
           	    YELLOW_HEALTH -= 1  

        winner_text = ''
        if RED_HEALTH == 0:
        	winner_text = 'Yellow wins!'
        if YELLOW_HEALTH == 0:
        	winner_text = 'Red wins!'

        if winner_text != '':
        	draw_winner(winner_text)
        	break


        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed,yellow)
        red_handle_movement(keys_pressed,red)


        handle_bullets(YELLOW_BULLET,RED_BULLET,yellow,red)
        draw_window(red,yellow,RED_BULLET,YELLOW_BULLET,RED_HEALTH,YELLOW_HEALTH)  
	
   pygame.quit()

if __name__ == '__main__':
  main()


