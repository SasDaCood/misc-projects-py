import turtle

WIDTH,HEIGHT  = 800,600
RADIUS		  = min(WIDTH,HEIGHT)//3
NUM_OF_POINTS = 100
CENTRAL_ANGLE = 360/NUM_OF_POINTS
TRACER_ACTIVE = False
color = 0
# change index later on to change main color

scr = turtle.Screen()
scr.setup(WIDTH,HEIGHT)
scr.title("Times tables")
scr.colormode(255)

pointer = turtle.Turtle()
pointer.shape("circle")
pointer.color((0,color,0))	# change index here
pointer.shapesize(0.5,0.5)
pointer.speed(0)
pointer.up()

pointer.goto(-RADIUS,0)
pointer.setheading(270)		# this is down

if TRACER_ACTIVE: turtle.tracer(0,0)

points_list = []
for i in range(NUM_OF_POINTS):
	pointer.circle(RADIUS,CENTRAL_ANGLE)
	pointer.dot(3,"darkblue")
	points_list.append(pointer.pos())

turtle.update()				# in the case TRACER_ACTIVE; doesn't affect cases where TRACER_ACTIVE == False

for number in enumerate(points_list):		# number = (index, coordinates of point)
	new_index = (number[0]*2) % NUM_OF_POINTS	# mod so that if new_index exceeds list bounds, it goes back again because circle
	pointer.goto(number[1])
	pointer.color((0,color,0))

	pointer.down()
	pointer.goto(points_list[new_index])
	pointer.up()

	color = (color+2)%256

turtle.update()
