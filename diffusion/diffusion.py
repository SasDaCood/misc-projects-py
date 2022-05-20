import turtle,winsound
from random import randint
from time import sleep,time

class Bubble(turtle.Turtle):
	def __init__(self):
		turtle.Turtle.__init__(self)
		
		self.shape("bubble.gif")
		self.up()
		self.speed(0)
		self.goto(randint(-WIDTH//10,WIDTH//10),randint(-HEIGHT//10,HEIGHT//10))

	def move(self):
		self.right(randint(0,359))
		self.forward(randint(1,MOVELIMIT))

	def deactivate(self):
		self.reset()
		self.ht()
		bubbleList.remove(self)

WIDTH,HEIGHT = 800,600
BUBBLENUM = 300
#bubbleList = [None] * BUBBLENUM
MOVELIMIT = 50
playPopSound = False

if BUBBLENUM < 300:
	DELAY = 0.05
elif BUBBLENUM >= 300:
	DELAY = 0
else:
	print("Bug occured. Exiting.")
	exit()

screen = turtle.Screen()
screen.setup(WIDTH,HEIGHT)
screen.bgcolor("gray")
screen.title("Diffusion visualizer")
screen.addshape("bubble.gif")
turtle.tracer(0,0)

bubbleList = [Bubble() for x in range(BUBBLENUM)]

sleep(1)
startTime = time()

while 1:
	for bubble in bubbleList:
		bubble.move()

		if bubble.pos()[0] > WIDTH//2 or bubble.pos()[0] < -WIDTH//2 or bubble.pos()[1] > HEIGHT//2 or bubble.pos()[1] < -HEIGHT//2:
			bubble.deactivate()
			if playPopSound: winsound.PlaySound("pop.wav", winsound.SND_ASYNC)
			#print(bubble,"has been deactivated. position is",bubble.pos())

	turtle.update()
	sleep(DELAY)

	if not bubbleList:
		break
	#print("for loop finished")


text = turtle.Turtle()
text.up()
text.ht()
text.color("blue")
text.write("All bubbles have touched the outer wall and have been popped.\nTime taken: {} seconds.\nExiting in 5 seconds...".format(int(time()-startTime)),align="center",font=("Calibri",20))

sleep(5)
exit()
