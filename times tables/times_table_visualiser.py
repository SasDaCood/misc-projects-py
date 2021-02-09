import turtle

WIDTH,HEIGHT  = 800,600
RADIUS		  = min(WIDTH,HEIGHT)//3
NUM_OF_POINTS = 20
CENTRAL_ANGLE = 360/NUM_OF_POINTS
TRACER_ACTIVE = True
MULTIPLY_BY   = 2

scr = turtle.Screen()
scr.setup(WIDTH,HEIGHT)
scr.title("Times tables")

pointer = turtle.Turtle()
pointer.shape("circle")
pointer.color("blue")
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
	new_index = (number[0]*MULTIPLY_BY) % NUM_OF_POINTS	# mod so that if new_index exceeds list bounds, it goes back again because circle
	pointer.goto(number[1])
	pointer.down()
	pointer.goto(points_list[new_index])
	pointer.up()

turtle.update()
