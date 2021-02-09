#for a v2, try remaking this program, this time being more function based, so that you can add the clicking thingy
# update if iterations % 50 (or any limit) == 0
# chaos game with restrictions
# working r values: 37.5, 90, 75, 50, 33.33, 62.5, 60
# 100 - r as r doesnt work as intended, to be able to input raw numbers from the web
import turtle
from time import sleep
from random import randint,choice

def printd(string_to_print,delay_time):
	print(string_to_print)
	sleep(delay_time)

def end_program(x,y):
	turtle.bye()
	exit()


WIDTH,HEIGHT = 800,600
MAX_SIDES    = 100
MIN_PERCENT  = 0.5
MAX_PERCENT  = 100 - MIN_PERCENT
DIST_TO_SIDE = HEIGHT//3
#ITERATIONS  = [15,30,60,100,200,400,650,900]
ITERATIONS   = [1,1,1,1,1,1,1,1]
DOT_SIZE     = 2

scr = turtle.Screen()
scr.setup(WIDTH,HEIGHT)
scr.title("The Chaos Game")

cursor = turtle.Turtle()
cursor.shape("circle")
cursor.color("lightgreen","firebrick")
cursor.speed(7)
cursor.up()


choice1 = input("Hey, we gon be playing the Chaos Game! Ever heard of it? (Y/N)\n")
if choice1.upper() == "N":
	printd("Well, tl;dr: it's a game where you take seemingly random points to create something... not so random.",2)
	printd("You'll understand much better when you try out this version of the chaos game,",2)
	printd("where you have three points by default which join to form an equilateral triangle.",2)
	printd("You can change the number of sides of the polygon to be produced,\n and even specify coordinates yourself for an irregular polygon.",2)
	printd("Then you must select a random point on the canvas, or let the program generate one randomly.",2)
	printd("Here's what our game should do:",1)
	printd("It should pick one of the random points or corners of the polygon.\n Then, from the previous point (or the starting point), it will move half the distance (customisable) to the chosen point,\nplace a point,\nand repeat, over and over.",4)
	printd("Will the regular polygon created by joining the points be created, will it be random, or... will something else happen?",1)
	printd("Let's find out :^)\n",2)
elif choice1.upper() == "Y":
	printd("Alright then, let's get straight into the inputs!\n",2)
else:
	printd("I'll... uh, assume that to be a nope. Let's just get into the inputs then!\n",2)

print("To start off...",end=" ")
while 1:
	try:
		number_of_sides = int(input("What is the number of sides or points that you want?\nObvious note: must be greater than or equal to 3, and an integer/whole number. Keep it under 100.\nInput 0 if you want the input to be randomised.\n"))
	except ValueError:
		print("Sorry, but your input wasn't an integer number of sides or points. Try again!\n")
		continue

	if number_of_sides == 0:
		number_of_sides = randint(3,MAX_SIDES)
		printd(f"The random number of sides/corners/points generated is {number_of_sides}.",2)
	elif number_of_sides < 3 or number_of_sides > MAX_SIDES:
		print("Sorry, but the number of sides that you entered was either too big or too small. Try again!\n")
		continue

	break

cursor.left(90)
cursor.fd(DIST_TO_SIDE)
cursor.left(90)

corners = []

print("\nNext up...",end=" ")
while 1:
	choice2 = input("Will (1) the shape formed be a regular polygon, each point being equidistant from other two points,\nor do you want to (2) specify the coordinates of each point yourself?\nEnter the number of your choice.\n")
	if choice2 == "1":
		central_angle = 360/number_of_sides

		for i in range(number_of_sides):
			cursor.circle(DIST_TO_SIDE,central_angle)
			# this should draw an arc that reaches the next point/corner of the shape
			corners.append((cursor.xcor(),cursor.ycor()))
			# and this should store the x and y coordinates of the turtle's position, the point, in a tuple and add it to the corners list
			cursor.dot(5,"darkblue")
			# to mark the point

	elif choice2 == "2":
		while 1:
			choice3 = input("Do you want to give your inputs for each point or corner by:\n(1) Inputting the raw numbers in the console, or\n(2) Clicking on the canvas wherever you want your points to be?\nNote: the graph goes from {0} to -{0} on the x axis, {1} to -{1} on the y axis.\n".format(WIDTH//2,HEIGHT//2))
		
			if choice3 == "1":
				for i in range(number_of_sides):
					while 1:
						try:
							coord_to_add = (int(input(f"Point {i+1}'s x coordinate: ")), int(input("and y coordinate: ")))
						except ValueError:
							print("Must be an integer. Try again.\n")
							continue

						if abs(coord_to_add[0]) > WIDTH//2 or abs(coord_to_add[1]) > HEIGHT//2:
							print("Sorry, but your input exceeds the x and/or y axis. Try again.\n")
							continue

						# if the coordinates input pass all the gruelling tests...
						corners.append(coord_to_add)
						cursor.goto(coord_to_add)
						cursor.dot(5,"darkblue")
						break

			elif choice3 == "2":
				import contextlib
				with contextlib.redirect_stdout(None):
					import pygame
				pygame.init()

				pg_scr = pygame.display.set_mode((WIDTH,HEIGHT))
				pg_scr.fill((255,255,255))
				pygame.display.flip()
				pygame.display.set_caption(f"Choose {number_of_sides} points!")

				print(f"Go ahead, the new canvas is all yours. Choose {number_of_sides} points! They'll be copied to the main canvas each time you click.")
			
				running = True
				while running:
					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							pygame.quit()
							turtle.bye()
							exit()
						elif event.type == pygame.MOUSEBUTTONDOWN:
							x,y = event.pos
							x -= WIDTH//2
							# pygame x starts from left of screen, so decrease half a screen width
							y = (HEIGHT//2) - y
							# pygame y starts from top of screen, HEIGHT//2 is top of screen, so deduct from that

							corners.append((x,y))
							cursor.goto(x,y)
							cursor.dot(5,"darkblue")
							print(f"Point ({x},{y}) has been added. {number_of_sides - len(corners)} left.")
							
							if len(corners) >= number_of_sides:
								print(f"\nThe {number_of_sides} points have been recorded.")
								pygame.quit()
								running = False
								break

			else:
				print("Sorry, but your input was wrong; it should be either 1 or 2. Please try again.\n")
				continue

			break
	else:
		print("Sorry, but your input was wrong; it should be either 1 or 2. Please try again.\n")
		continue

	break

printd("All the points have been generated!",2)
printd("\nAnd then...",2)

while 1:
	try:
		fraction_to_travel = float(input(f"What percentage of the distance between two points will the program travel each time?\ne.g. 50% would result in half the distance being travelled.\nKeep the fraction between {MIN_PERCENT} and {MAX_PERCENT}%. Decimal values are accepted.\nType 0 to generate a random percentage.\n"))
		# will be turned into a decimal value, and later plugged into a formula to find coordinates of point between chosen points
	except ValueError:
		print("Sorry, but your input should've been a number. Please try again.")
		continue

	if fraction_to_travel == 0:
		fraction_to_travel = randint(1,MAX_PERCENT*1000)/1000
		# to be able to get decimal values
		print(f"The percentage is {fraction_to_travel}%")
	elif fraction_to_travel > MAX_PERCENT or fraction_to_travel < MIN_PERCENT:
		print("Sorry, but your input is out of bounds. Please try again.")
		continue

	fraction_to_travel /= 100
	# converted into a decimal
	break

printd("\nAnd finally...\nA starting point will be picked to start the game.",2)

while 1:
	choice4 = input("Do you want to (1) set the coordinate yourself, or\n(2) generate a random coordinate and get on with the game already?\n")
	if choice4 == "1":
		while 1:
			try:
				last_point_coords = (int(input("Starting x coordinate: ")), int(input("and y coordinate: ")))
			except ValueError:
				print("Value must be an integer. Try again.\n")
				continue

			if abs(last_point_coords[0]) > WIDTH//2 or abs(last_point_coords[1]) > HEIGHT//2:
				print("Sorry, but your input exceeds the x and/or y axis. Please try again.\n")
				continue

			break
	elif choice4 == "2":
		last_point_coords = (randint(-WIDTH//2,WIDTH//2), randint(-HEIGHT//2,HEIGHT//2))
		printd(f"Coordinates generated were {last_point_coords}.",1)
	else:
		print("Sorry, but your input is wrong. Try again!")
		continue

	break

cursor.goto(last_point_coords)
cursor.dot(DOT_SIZE,"green")
cursor.speed(3)

printd("Finally, starting the chaos game in five seconds...",5)
print("Begin!")

text = turtle.Turtle()
text.up()
text.ht()
text.speed(0)
text.color("blue")
text.goto((WIDTH//2)-20,(HEIGHT//2)-30)
# will be used to write the number of iterations
iterated = 0

for index in range(len(corners)):
	corners[index] = (round(corners[index][0],2), round(corners[index][1],2))
# to round the corners thingy down so that decimal places don't explode in the running of program and thus slow down the calculation

for speed in range(3,12):
	cursor.speed(speed)

	if speed == 11:
		cursor.speed(0)
		turtle.tracer(0,0)
		# to speed up drawing as much as fucking possible
		turtle.onscreenclick(end_program)

		while 1:
			chosen_point = choice(corners)
		
			nextx = (1 - fraction_to_travel)*last_point_coords[0] + fraction_to_travel*chosen_point[0]
			nexty = (1 - fraction_to_travel)*last_point_coords[1] + fraction_to_travel*chosen_point[1]
			nextx,nexty = round(nextx,2), round(nexty,2)

			cursor.goto(nextx,nexty)
			cursor.dot(DOT_SIZE,"green")
			iterated += 1
			last_point_coords = (nextx,nexty)

			text.clear()
			text.write(f"Iterations: {iterated}",align="right",font=("Calibri",15))
			turtle.update()

	for iteration in range(ITERATIONS[speed-3]):
		chosen_point = choice(corners)
		
		nextx = (1 - fraction_to_travel)*last_point_coords[0] + fraction_to_travel*chosen_point[0]
		nexty = (1 - fraction_to_travel)*last_point_coords[1] + fraction_to_travel*chosen_point[1]
		nextx,nexty = round(nextx,2), round(nexty,2)

		cursor.goto(nextx,nexty)
		cursor.dot(DOT_SIZE,"green")
		iterated += 1
		last_point_coords = (nextx,nexty)

		text.clear()
		text.write(f"Iterations: {iterated}",align="right",font=("Calibri",15))
