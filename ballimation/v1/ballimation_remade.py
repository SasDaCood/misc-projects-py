import pygame
from random import randint
pygame.init()
pygame.mixer.init()

def tschuss():
    pygame.quit()
    print("\n\nAlright then, bye! Have a nice day!\nPress enter to exit.")
    input()
    exit()

def pauseLoop(quitLoop = False):
    pause = True
    if quitLoop: 
        print("\nDo you really want to quit? Press Y or N for yes or no, respectively.")

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if not quitLoop:
                    if event.key == pygame.K_p:
                        pause = False

                elif event.key == pygame.K_y:
                    tschuss()
                elif event.key == pygame.K_n:
                    pause = False
                
    print("\nGame resumed!")
    

area = WIDTH,HEIGHT = 800,600
speed = [1,1]
GRAY = 150,150,150
MAXSPEED = 6
FRAMERATE = 200

pygame.mixer.music.load("wallhit.wav")
screen = pygame.display.set_mode(area)
pygame.display.set_caption("Round the Ball")
ball = pygame.image.load("ball.png")
clock = pygame.time.Clock()
#pygame.display.set_icon(ball)
ballrect = ball.get_rect()
gravity = 1
'''
0 is gravNone, 1 is gravDown, 2 is gravLeft,
3 is gravUp, 4 is gravRight.
'''
gravPing = [0.02,0.05,0.1,0.2,0.5]
gravPingIndex = 2
WALL_OFFSET = max(ballrect.width,ballrect.height)/2

print("Press the directional keys to jerk to one side.\nLeft-click anywhere to teleport, right-click to randomly teleport.\nPress R to reset, O to reverse your direction,\nG to toggle gravity settings, F to toggle gravitational field strength,\nS to stop all motion, I to change speed to random numbers,\nP to pause and resume, and Q to quit.")
startticks = pygame.time.get_ticks()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION: continue           # prevent lag
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if speed[1] > 0: speed[1] = 0
                speed[1] -= 2

            elif event.key == pygame.K_DOWN:
                if speed[1] < 0: speed[1] = 0
                speed[1] += 2

            elif event.key == pygame.K_LEFT:
                if speed[0] > 0: speed[0] = 0
                speed[0] -= 2

            elif event.key == pygame.K_RIGHT:
                if speed[0] < 0: speed[0] = 0
                speed[0] += 2

            elif event.key == pygame.K_r:
                ballrect.x = ballrect.y = WALL_OFFSET
                speed = [2,2]
                print("\nBall reset!")

            elif event.key == pygame.K_o:
                speed[0] = -speed[0]
                speed[1] = -speed[1]
                print("\nSpeed reversed!")

            elif event.key == pygame.K_g:
                gravity += 1
                gravity %= 5
                if gravity == 0: print("\nGravity off!")
                elif gravity == 1: print("\nGravity down!")
                elif gravity == 2: print("\nGravity left!")
                elif gravity == 3: print("\nGravity up!")
                elif gravity == 4: print("\nGravity right!")
                else: raise Exception("Unknown value for gravity - {}".format(gravity))

            elif event.key == pygame.K_f:
                gravPingIndex += 1
                gravPingIndex %= len(gravPing)
                if gravPingIndex == 0: print("\nGravitational strength extremely high!")
                elif gravPingIndex == 1: print("\nGravitational strength high!")
                elif gravPingIndex == 2: print("\nGravitational strength medium!")
                elif gravPingIndex == 3: print("\nGravitational strength low!")
                elif gravPingIndex == 4: print("\nGravitational strength extremely low!")
                else: raise Exception("Unknown value for gravity ping index - {}".format(gravPingIndex))
                
            elif event.key == pygame.K_s:
                speed[0] = speed[1] = 0
                print("\nBall stopped!")

            elif event.key == pygame.K_i:
                speed = [randint(-MAXSPEED,MAXSPEED),randint(-MAXSPEED,MAXSPEED)]
                print("\nSpeed randomized!")

            elif event.key == pygame.K_p:
                print("\nGame paused! Press P to resume.")
                pauseLoop()

            elif event.key == pygame.K_q:
                pauseLoop(True)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:                       # LMB is 1, RMB is 3
                if event.pos[0] > WALL_OFFSET and event.pos[0] < WIDTH-WALL_OFFSET and event.pos[1] > WALL_OFFSET and event.pos[1] < HEIGHT-WALL_OFFSET:
                    ballrect.centerx,ballrect.centery = event.pos[0],event.pos[1]
                    print("\nTeleported to {0}, {1}!".format(event.pos[0],event.pos[1]))
                else:
                    print("\nToo close to the walls!")
            elif event.button == 3:
                ballrect.centerx,ballrect.centery = randint(WALL_OFFSET,WIDTH-WALL_OFFSET),randint(WALL_OFFSET,HEIGHT-WALL_OFFSET)
                print("\nRandomly teleported to {0}, {1}!".format(ballrect.centerx,ballrect.centery))
                            
        elif event.type == pygame.QUIT:
            tschuss()


    if ballrect.left < -10:
        ballrect.centerx = WIDTH - WALL_OFFSET
        print("\nYou zapped through the walls! D:")
    elif ballrect.right > WIDTH+10:
        ballrect.centerx = WALL_OFFSET
        print("\nYou zapped throught the walls! D:")
    if ballrect.top < -10:
        ballrect.centery = HEIGHT - WALL_OFFSET
        print("\nYou zapped throught the walls! D:")
    elif ballrect.bottom > HEIGHT+10:
        ballrect.centery = WALL_OFFSET
        print("\nYou zapped throught the walls! D:")


    seconds = (pygame.time.get_ticks() - startticks)/1000
    if gravity and seconds >= gravPing[gravPingIndex]:
        if gravity == 1: speed[1] += 1
        elif gravity == 2: speed[0] -= 1
        elif gravity == 3: speed[1] -= 1
        elif gravity == 4: speed[0] += 1
        startticks = pygame.time.get_ticks()
        

    if speed[0] > MAXSPEED: speed[0] = MAXSPEED
    elif speed[0] < -MAXSPEED: speed[0] = -MAXSPEED
    if speed[1] > MAXSPEED: speed[1] = MAXSPEED
    elif speed[1] < -MAXSPEED: speed[1] = -MAXSPEED

        
    if ballrect.left < 0 or ballrect.right > WIDTH:
        speed[0] = -speed[0]
        pygame.mixer.music.play()
    if ballrect.top < 0 or ballrect.bottom > HEIGHT:
        speed[1] = -speed[1]
        pygame.mixer.music.play()

    ballrect.move_ip(speed)
    screen.fill(GRAY)
    screen.blit(ball,ballrect)
    pygame.display.flip()

    clock.tick(FRAMERATE)
