import pygame
pygame.init()
pygame.mixer.init()

# velocity[0] - if negative, to left, if positive to right
# velocity[1] - if negative up, if positive down |==

size = width, height = 800,600
velocity = [2,2]
black = 150, 150, 150
gravity = 1                         # 0 is noGravity, 1 is gravityDown, 2 is gravityUp
gravityTickSpeeds = [0.01,0.05,0.1,0.2,0.5]
gravityTickIndex = 2
MAXSPEED = 5

pygame.mixer.music.load("wallhit.wav")
scr = pygame.display.set_mode(size)
pygame.display.set_caption("flopping birb")

ball = pygame.image.load("ball\\ball.png")
ballhitbox = ball.get_rect()
startticks = pygame.time.get_ticks()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and velocity[1] > -5:
                if velocity[1] > 0: velocity[1] = 0
                velocity[1] += -2
                print("\n\nUp we go!\n")
                
            elif event.key == pygame.K_DOWN and velocity[1] < 5:
                if velocity[1] < 0: velocity[1] = 0
                velocity[1] += 2
                print("\n\nDown we go!\n")

            elif event.key == pygame.K_LEFT and velocity[0] > -5:
                if velocity[0] > 0: velocity[0] = 0
                velocity[0] -= 2
                print("\n\nLeft we go!\n")

            elif event.key == pygame.K_RIGHT and velocity[0] < 5:
                if velocity[0] < 0: velocity[0] = 0
                velocity[0] += 2
                print("\n\nRight we go!\n")
                
            elif event.key == pygame.K_r:
                velocity = [2,2]
                ballhitbox.x = 0
                ballhitbox.y = 0
                print("\n\nAww, a reset D:\n")

            elif event.key == pygame.K_s:
                velocity = [0,0]
                print("\n\nHalt!\n")

            elif event.key == pygame.K_g:
                gravity += 1
                gravity %= 3
                print("\n\nGRAVITY SWIIIITCH!\n")

            elif event.key == pygame.K_f:
                gravityTickIndex += 1
                gravityTickIndex %= len(gravityTickSpeeds)
                print("\n\nGravitational field strength changed!\n")
                
            elif event.key == pygame.K_SPACE:
                print("\n\nBye!\n")
                pygame.quit()
                exit()

    

    if ballhitbox.left < 0 or ballhitbox.right > width:
        velocity[0] = -velocity[0]
        print(velocity)
        pygame.mixer.music.play()
            
    if ballhitbox.top < 0 or ballhitbox.bottom > height:
        velocity[1] = -velocity[1]
        print(velocity)
        pygame.mixer.music.play()


    if ballhitbox.left < -10:
        ballhitbox.right = width-1
        print("\n\nWoops! You zapped through the wall!\n")
        
    elif ballhitbox.right > width + 10:
        ballhitbox.left = 1
        print("\n\nWoops! You zapped through the wall!\n")

    elif ballhitbox.top < -10:
        ballhitbox.bottom = height-1
        print("\n\nWoops! You zapped through the ceiling!\n")

    elif ballhitbox.bottom > height + 10:
        ballhitbox.top = 1
        print("\n\nWoops! You zapped through the floor!\n")


    ballhitbox = ballhitbox.move(velocity)

    if gravity:
        seconds = (pygame.time.get_ticks()-startticks)/1000
        if seconds > gravityTickSpeeds[gravityTickIndex]:
            startticks = pygame.time.get_ticks()        # restart counter
            if gravity == 1: velocity[1] += 1
            else: velocity[1] -= 1
            print(velocity)

    if velocity[0] > MAXSPEED: velocity[0] = MAXSPEED
    elif velocity[0] < -MAXSPEED: velocity[0] = -MAXSPEED
    if velocity[1] > MAXSPEED: velocity[1] = MAXSPEED
    elif velocity[1] < -MAXSPEED: velocity[1] = -MAXSPEED

    scr.fill(black)
    scr.blit(ball,ballhitbox)
    pygame.display.flip()
