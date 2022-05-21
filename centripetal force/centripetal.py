import pygame
from math import cos,sin,radians
pygame.init()

DISPLAY = WIDTH,HEIGHT = 800,600
POS_X_V = pygame.math.Vector2(1,0)		# unit vector to represent positive x axis, for calculating angles clockwise from +ve x-axis (y is reversed in pygame)
FRAMERATE = 60
BG_COLOUR = (255,255,255,255)

class Balle:
	def __init__(self, imgname, force, angle, v_init=(3,0), T_MAX=15, T_THICC=6, T_COLOUR=(0,0,0)):
		self.img = self.OG_IMG = pygame.image.load(imgname)		# keep original so that we can rotate the original when needed
		self.rect = self.img.get_rect()
		self.rect.center = WIDTH//2,HEIGHT//2

		self.vel = pygame.math.Vector2(v_init)
		self.force  = force 			# we simplify F=ma to F=a by setting m=1 unit
		self.fangle = angle 			# gradians ofc; this angle is clockwise from velocity direction

		self.TRAIL_MAX    = T_MAX
		self.TRAIL_THICC  = T_THICC
		self.TRAIL_COLOUR = T_COLOUR
		self.trail = []
		self.update_trail()

	def vel_angle(self):
		return POS_X_V.angle_to(self.vel)

	def add_force(self):
		angle_to_x = self.vel_angle() + self.fangle
		f_vector = pygame.math.Vector2( self.force * cos(radians(angle_to_x)), self.force * sin(radians(angle_to_x)) )
		self.vel += f_vector

	def update_trail(self):
		if len(self.trail) >= self.TRAIL_MAX: self.trail = self.trail[1:]
		self.trail.append(self.rect.center)

	def rotate(self):
		self.img = pygame.transform.rotate(self.OG_IMG, -(90 + self.vel_angle()))
		old_centre = self.rect.center
		self.rect = self.img.get_rect()
		self.rect.center = old_centre
	
	def move(self):
		self.rect.move_ip(self.vel.x, self.vel.y)
		self.rotate()
		self.update_trail()

	def draw_trail(self):
		length = len(self.trail)
		if length > 1:
			for i in range(length-1):
				l_colour = ( self.TRAIL_COLOUR[0], self.TRAIL_COLOUR[1], self.TRAIL_COLOUR[2], int((i+1)/length * 255) )
				l_width  = round((i+1)/length * self.TRAIL_THICC)
				pygame.draw.line(sdraw, l_colour, self.trail[i], self.trail[i+1], l_width)


scr = pygame.display.set_mode(DISPLAY)
sdraw = pygame.Surface(DISPLAY, flags=pygame.SRCALPHA)
pygame.display.set_caption("centripetri forci")
clock = pygame.time.Clock()
za_ball = Balle("ball.png",0.25,91)

while 1:
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			za_ball.rect.center = event.pos
			za_ball.trail = []
		elif event.type == pygame.QUIT:
			pygame.quit()
			exit()

	sdraw.fill(BG_COLOUR)

	za_ball.add_force()
	za_ball.move()
	za_ball.draw_trail()
	sdraw.blit(za_ball.img,za_ball.rect)
	scr.blit(sdraw,(0,0))

	pygame.display.flip()
	print(za_ball.vel.magnitude())
	clock.tick(FRAMERATE)