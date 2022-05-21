# wonder if updating screen could be optimised by only colouring pixels when the display's about to be flipped. set_at isnt particularly fast; could use pygame.PixelArray instead

import pygame
from math import sin,cos,radians
from random import randint
from time import time
pygame.init()

ANGLE_CW = 90			# 1
ANGLE_CCW = -90			# 0
DISN = 1
BLACK,WHITE = (0,0,0),(255,255,255)
HUE_INC = 0.2 								# set to a fraction to increase colour range length
COLOUR_HUE = False
DISPLAY = WIDTH,HEIGHT = 1080,1080
MIDPOINT = WIDTH//2, HEIGHT//2
UPDATE_DELAY = 0.1 							# set to 0 to update every frame
NUM_START,NUM_INC = 0,1 					# standard: 0,1

scr = pygame.display.set_mode(DISPLAY)
scr.fill(BLACK)		# or WHITE
pygame.display.set_caption("Binary fractal (LMB to save snapshot, RMB to exit)")
pygame.display.flip()

def binarify(den_num):
	return bin(den_num)[2:]

class Cursor:
	'''adaptation of turtle's Turtle()'''
	def __init__(self,coords,angle=90):
		self.colour = pygame.Color(0,0,0)
		self.hue = 0
		self.x,self.y = coords
		self.angle = angle 					# usually initialised as facing East

	def move(self,bin_num):
		self.angle += ANGLE_CW if bin_num else ANGLE_CCW
		self.x += DISN * cos(radians(self.angle))
		self.y -= DISN * sin(radians(self.angle))
		#self.x,self.y = round(self.x,2), round(self.y,2)
		self.hue = (self.hue + HUE_INC) % (360 if COLOUR_HUE else 512)

	def place_point(self):
		round_h = int(self.hue)
		if COLOUR_HUE:	self.colour.hsva = (round_h, 100, 100, 100)
		else:			self.colour.r = round_h if round_h < 256 else 511 - round_h

		scr.set_at((round(self.x), round(self.y)), self.colour)
		if UPDATE_DELAY==0: pygame.display.update(pygame.Rect(self.x, self.y, 1, 1))


curs = Cursor(MIDPOINT)
current_num = NUM_START
update_time = time()

while 1:
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				pygame.image.save(scr,f"a{ANGLE_CW}{ANGLE_CCW} n{NUM_START}{NUM_INC} h{HUE_INC} r{WIDTH}x{HEIGHT} {randint(1,10000)}.png")
			elif event.button == 3:
				pygame.quit(); exit()

		elif event.type == pygame.QUIT:
			pygame.quit(); exit()

	for b_chr in binarify(current_num):
		curs.move(int(b_chr))
		curs.place_point()

	if UPDATE_DELAY and time() - update_time > UPDATE_DELAY:
		update_time = time()
		pygame.display.flip()

	current_num += NUM_INC
	#DISN *= 0.9999