import turtle
from PIL import Image


WIDTH,HEIGHT = 800,600
RADIUS		 = min(WIDTH,HEIGHT)//3
MULTIPLY_BY  = 3
MIN_POINTS   = 5
MAX_POINTS   = 200
#num_of_points = 100
#CENTRAL_ANGLE = 360/num_of_points


scr = turtle.Screen()
scr.setup(WIDTH,HEIGHT)
scr.title("Times tables")

turtle.tracer(0,0)

pointer = turtle.Turtle()
pointer.shape("circle")
pointer.color("blue")
pointer.shapesize(0.5,0.5)
pointer.speed(0)
pointer.up()
pointer.ht()

for num_of_points in range(MIN_POINTS,MAX_POINTS):
	pointer.clear()
	central_angle = 360/num_of_points
	pointer.goto(-RADIUS,0)
	pointer.setheading(270)		# this is down

	points_list = []
	for i in range(num_of_points):
		pointer.circle(RADIUS,central_angle)
		pointer.dot(3,"darkblue")
		points_list.append(pointer.pos())


	for number in enumerate(points_list):		# number = (index, coordinates of point)
		new_index = (number[0]*MULTIPLY_BY) % num_of_points	# mod so that if new_index exceeds list bounds, it goes back again because circle
		pointer.goto(number[1])
		pointer.down()
		pointer.goto(points_list[new_index])
		pointer.up()

	turtle.update()
	scr.getcanvas().postscript(file="image{}.eps".format(num_of_points-MIN_POINTS))

filenames = ["image{}.eps".format(index) for index in range(0,MAX_POINTS-MIN_POINTS)]
images    = [Image.open(file) for file in filenames]

images[0].save("multiplication_table_{}.gif".format(MULTIPLY_BY), save_all=True, append_images=images[1:], duration=30, loop=0)
