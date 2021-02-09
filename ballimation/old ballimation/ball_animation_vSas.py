import pygame
from time import sleep
pygame.init
pygame.mixer.init()

size = width, height = 800,600
velocity = [1,1]
black = 0, 0, 0
pygame.mixer.music.load("wallhit.wav")

scr = pygame.display.set_mode(size)

ball = pygame.image.load("ball.bmp")
ballhitbox = ball.get_rect()

print(velocity)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_A:
                pygame.quit()
                exit()
            #elif event.key = pygame.K_UP:
            #    velocity

    ballhitbox = ballhitbox.move(velocity)

    if ballhitbox.left < 0 or ballhitbox.right > width:
        velocity[0] = -velocity[0]
        print(velocity)
        pygame.mixer.music.play()
            
    if ballhitbox.top < 0 or ballhitbox.bottom > height:
        velocity[1] = -velocity[1]
        print(velocity)
        pygame.mixer.music.play()

    scr.fill(black)
    scr.blit(ball,ballhitbox)
    pygame.display.flip()
