limit = int(input("Uptil which number (in denary) will I generate the fractal? "))

binary_list = "".join( (bin(denary_i) for denary_i in range(limit+1)) )
binary_list = binary_list.replace("0b","")


import turtle

WIDTH,HEIGHT = 600,900
COLOUR = "red"

scr = turtle.Screen()
scr.setup(WIDTH,HEIGHT)
scr.title("Binary turn fractal")
turtle.tracer(False)

t = turtle.Turtle()
t.speed(0)
t.ht()
t.pencolor(COLOUR)
t.left(90)

for number in binary_list:
	if int(number):		# number is 1
		t.right(90)
	else:				# number is 0
		t.left(90)

	t.fd(0.5)
	turtle.update()
