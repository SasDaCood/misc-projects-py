from time import sleep
from random import randint,choice
from PIL import Image
import turtle


WIDTH,HEIGHT = 800,600
MAX_SIDES    = 100
MIN_PERCENT  = 0
MAX_PERCENT  = 100 - MIN_PERCENT
DIST_TO_SIDE = HEIGHT//3
DOT_SIZE     = 2
ITERATIONS   = 15000
INPUT_SIZE   = 7

scr = turtle.Screen()		# getcanvas with this
scr.setup(WIDTH,HEIGHT)
scr.title("The Chaos Game: GIF Generator ver.")

cursor = turtle.Turtle()
cursor.shape("circle")
cursor.color("lightgreen","firebrick")
cursor.speed(0)
cursor.up()
cursor.ht()


while 1:
	input_string = input("""Give your inputs in a string, separated by spaces, in this format:

Starting number of sides +
Ending number of sides (both greater than 3, less than 100) +
Regular [1] or irregular [0] (will be set to 1 unless starting_sides == ending_sides) +
Restrictions [1] or not [0] +
Minimum ratio to start from, in percentage +
Maximum ratio to end at, in percentage (both greater than 0, less than 100) +
Step to increase ratio by, in percentage (cannot be negative).

(Irregular points will be recorded after these inputs have been recorded and validated)


Input here: """).split()

	if len(input_string) != INPUT_SIZE:
		print("Sorry, but your choice string was either too long or too short. Please try again.")
		continue

	try:
		input_string = [float(number) for number in input_string]
		input_string[0] = int(input_string[0])
		input_string[1] = int(input_string[1])
	except ValueError:
		print("Must be numbers! Try again.")
		continue

	starting_sides, ending_sides, is_regular, has_restrictions, start_ratio, end_ratio, step_ratio = input_string

	if starting_sides < 3  or  starting_sides > MAX_SIDES  or  ending_sides < 3  or  ending_sides > MAX_SIDES  or  starting_sides > ending_sides  or  (is_regular != 0 and is_regular != 1)  or  (has_restrictions != 0 and has_restrictions != 1)  or  start_ratio < MIN_PERCENT  or  start_ratio > MAX_PERCENT  or  end_ratio < MIN_PERCENT  or  end_ratio > MAX_PERCENT  or  step_ratio < 0 or start_ratio > end_ratio:
		print("Your choices were out of bounds. Please try again.")
		continue

	if starting_sides != ending_sides: is_regular = 1
	break


if not is_regular:
	import contextlib
	with contextlib.redirect_stdout(None):
		import pygame
	pygame.init()

	pg_scr = pygame.display.set_mode((WIDTH,HEIGHT))
	pg_scr.fill((255,255,255))
	pygame.display.flip()
	pygame.display.set_caption(f"Choose {starting_sides} points!")

	print(f"Go ahead, the new canvas is all yours. Choose {starting_sides} points! They'll be copied to the main canvas.")
		
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
				print(f"Point ({x},{y}) has been added. {starting_sides - len(corners)} left.")
							
				if len(corners) >= starting_sides:
					print(f"\nThe {starting_sides} points have been recorded.")
					pygame.quit()
					running = False
					break

print("All the points have been generated!\nStarting generation in three seconds...")
sleep(3)
print("Begin!")

text = turtle.Turtle()
text.up()
text.ht()
text.speed(0)
text.color("blue")
text.goto((WIDTH//2)-20,(HEIGHT//2)-50)
# will be used to write the number of iterations AND ratio at the END of each set of iterations
# iterated ITERATIONS times

turtle.tracer(0,0)

#if you want to encapsulate this in an increasing number_of_sides loop, add a separate, OUTER index variable that's incremented after every iteration of THIS while loop and used to generate the gif file at the end. gif file should be result{}.gif.format index.

for number_of_sides in range(starting_sides,ending_sides+1):
	cursor.clear()

	fraction_to_travel = start_ratio
	image_index = 0
	corners = []
	if is_regular:
		cursor.goto(0,DIST_TO_SIDE)
		cursor.setheading(180)
		# points cursor to left side
		central_angle = 360/number_of_sides

		for i in range(number_of_sides):
			cursor.circle(DIST_TO_SIDE,central_angle)
			# this should draw an arc that reaches the next point/corner of the shape
			corners.append(( round(cursor.xcor(),2),  round(cursor.ycor(),2) ))
			# and this should store the x and y coordinates of the turtle's position, the point, in a tuple and add it to the corners list; rounded because numbers explode in decimal places otherwise
			cursor.dot(5,"darkblue")
			# to mark the point


	while fraction_to_travel <= end_ratio:
		# let's reset the screen and draw the shape again
		cursor.clear()

		if is_regular:
			cursor.goto(0,DIST_TO_SIDE)
			cursor.setheading(180)
			central_angle = 360/number_of_sides

			for i in range(number_of_sides):
				cursor.circle(DIST_TO_SIDE,central_angle)
				# this should draw an arc that reaches the next point/corner of the shape
				cursor.dot(8,"darkblue")
				# to mark the point
		else:
			for coords in corners:
				cursor.goto(coords)
				cursor.dot(8,"darkblue")

		last_point_coords = (randint(-WIDTH//2,WIDTH//2), randint(-HEIGHT//2,HEIGHT//2))
		# initialise last_point randomly
		cursor.goto(last_point_coords)
		# no dot because i don't want random points outside of the shape to be shown in the actual images
		iterated = 0
		ratio_to_move = fraction_to_travel/100


		if has_restrictions:
			temp_corners = corners[:]
			temp_corners.remove(choice(temp_corners))

			while 1:
				# 2, 3 - temp_corners
				chosen_point = choice(temp_corners)		# 3
				temp_corners = corners[:]				# 2, 3, 5
				temp_corners.remove(chosen_point)		# 2, 5
				# prevents same corner from being selected
			
				nextx = (1 - ratio_to_move)*last_point_coords[0] + ratio_to_move*chosen_point[0]
				nexty = (1 - ratio_to_move)*last_point_coords[1] + ratio_to_move*chosen_point[1]
				nextx,nexty = round(nextx,2), round(nexty,2)
				# to stop values from exploding in the number of decimal places

				cursor.goto(nextx,nexty)
				cursor.dot(DOT_SIZE,"green")
				iterated += 1
				last_point_coords = (nextx,nexty)

				if iterated >= ITERATIONS:
					break
				# greater than included, because infinite loop otherwise in case of bug
		else:
			while 1:
				chosen_point = choice(corners)
			
				nextx = (1 - ratio_to_move)*last_point_coords[0] + ratio_to_move*chosen_point[0]
				nexty = (1 - ratio_to_move)*last_point_coords[1] + ratio_to_move*chosen_point[1]
				nextx,nexty = round(nextx,2), round(nexty,2)

				cursor.goto(nextx,nexty)
				cursor.dot(DOT_SIZE,"green")
				iterated += 1
				last_point_coords = (nextx,nexty)

				if iterated >= ITERATIONS:
					break

		text.clear()
		text.write("Iterations: {0}\nRatio: {1}".format(ITERATIONS,round(fraction_to_travel,2)), align="right", font=("Corbel",15))
		# round fraction_to_travel so that text doesn't get too long
		turtle.update()
		# update the screen after all the calculations are complete

		scr.getcanvas().postscript(file="image{}.eps".format(image_index))
		# should rewrite old files

		fraction_to_travel += step_ratio
		image_index += 1


	filenames = ["image{}.eps".format(index) for index in range(0,image_index)]
	# not image_index + 1, as image_index is incremented at the end of each iteration, meaning actual_iterations = image_index
	images    = [Image.open(file) for file in filenames]
	# creating the list of images generated

	images[0].save("{0}{1}_atSides_{2}_{3}.gif".format(int(has_restrictions),int(is_regular),number_of_sides,step_ratio), save_all=True, append_images=images[1:], duration=3000//len(images), loop=0)
	# entire gif should take 3 seconds or so
