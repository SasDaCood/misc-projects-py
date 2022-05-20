# fps counter - DONE
# animated sprites? could be the same for new and improved flappy birb
# only allow certain events into the queue to reduce lag - DONE
# remove usage of console. render the "controls" text onscreen, and once game starts, have the text bounce around w/ own ai
# imperfect bounces + bounce sound scaling + can rest on the floor
# maybe even more gravity options like northeast and stuff, or even, dare I say, an angled gravity option? uses unit circle + trigo to determine velocity to add each update tick
# oh yeah, about that: gravity updates will be tied to the framerate instead of time passed? that'd solve the gravity stalling problem
# some kinda squashing animation where the img gets compressed whenever it hits a wall or sth
# a flag to toggle whether or not the extra balls spawned actually use their bounce despawn system or nah (spawning more and more)
# intro: the ball keeps bouncing around in 0 gravity while the intro font screen (might be a ball/inherited) spawns right outside the window and flips gravity a few times and stabilises. anytime during this or afterwards (well, only if the text surface is inside the window) you can press the start button, which'll randomise the text's velocity and start the game
# fps counter that might use a class, has an init function (not __init__) that sets a startign time and prints the fps depending on the framrate given to it (frames are incremented after each gameloop)
# when clipping out of a wall, do the normal velocity reversion but also always correct the velocity before moving so that there's no chance of going out of the screen 
# font text will bounce around too??? could be a Ball that communicates w/ the FPS class to change font
# pygame rects can only store ints so i needta have another set of attributes for more accurate movement

# UPDATE 2022: max number of dust clones? add an attribute to dust clones to identify them or make another subclass
# maybe add non-rect walls, or prep for it by handling collisions by finding point of contact of ball w/ wall


# pygame.mixer.pause/unpause
# pygame.mixer.Sound.volume
# pygame.mixer.find_channel()
# clicking and holding (pygame.mouse) should tempo disable motion and keep teleporting every frame
# gravitational strength decrease and increase buttons + 2 gravity rotation buttons
# wasd buttons increment speed in that direction; keys pressed together are accounted for
# speed multiplier/frenzy key?
# pygame.keyboard?
# gravity mouse thingo where you click on the screen and it calculates new gravity based on angle + horizontal & vertical disn relative to the WIDTH and HEIGHT. Middle mouse button?
# after finishing the base shits, make an option (or even another button) to display all the stats (bouncy, gravity etc) of the main_ball onscreen
# terraria dust effect: spawn lots of clones of the ball during move() using randint==1 using spawn_clone(), each having variable sizes but also a fraction of the original velocity of the mother ball (prob w/ some variance/comparing w/ and w/o variance). Really short frames_left too
# another stat to control: variance?
# merge all Ball.change- functions into one, with "pygame.K_sth" as the parameter
# click on any point on the screen to make the ball nyoom towards it
import pygame
from random import randint,choice
from math import sin,cos,atan,radians,degrees
pygame.init()
pygame.mixer.init()


DISPLAY 	= WIDTH,HEIGHT = 1000,700	# 800,600
MIDPOINT 	= WIDTH//2,HEIGHT//2
BG_COLOUR 	= 150,150,150
FRAMERATE 	= 120
KILL_BALLS 	= True						# whether balls 
UNIVERSAL_VARIANCE,VARIANCE_DIGITS = 0.3,1
clock 	= pygame.time.Clock()

wallhit_sounds = (pygame.mixer.Sound("assets\\wallhit0.wav"), pygame.mixer.Sound("assets\\wallhit1.wav"), pygame.mixer.Sound("assets\\wallhit2.wav"), pygame.mixer.Sound("assets\\wallhit3.wav"))
base_ball = pygame.image.load("assets\\ball.png")

intro_text_content = """helo helo and welcom to le ballse
you are ballman, control bal
r u want to become one with the ball?
then look no more
for now you can truly becom
ball"""


class Ball:
	'''Class defining each of the bouncy thingos that can be spawned in-"game"'''
	MAX_SPEED = 6			# wonder if i should just move this inside of init, so that each instance can have custom max speeds; consistency, though?
	MAX_GRAVITY = 5 		# same for this as ^
	DASH_SPEED 	= MAX_SPEED/2
	VOLUME_MULT = 3 		# speed of ball relative to max speed * sturdiness or (1-bounciness) = volume, but scale volume and cap it at 1
	DUST_SPEED_RATIO = 0.25

	GRAVITY_INC = 0.1
	ANGLE_INC 	= 5
	#SPEED_INC 	= 0.2
	BOUNCY_INC 	= 0.05
	AIR_RES_INC = 0.05

	instances = []			# will be used for collision detection and shits, prob
	def __init__(self, image: pygame.Surface, spawn=MIDPOINT, wallhit_soundlist=wallhit_sounds, bounciness=1, frames_left=-1, velocity=(0,0), gravity=0.2, air_res = 0.01 ):
		self.img = self.og_img = image		# rotate/transform the original image and store the result in img instead of just repeatedly transforming one img to avoid img quality loss or sth idk; for fonts, i'll have to do sth more complex
		self.rect = self.og_img.get_rect()
		self.rect.center = spawn
		self.true_centre_x,self.true_centre_y = self.rect.center
		self.rotation = 0					# radians, ig?

		self.velocity = list(velocity)
		self.grav_magnitude = gravity
		self.grav_angle     = 90 			# degrees
		self.calculate_gravity()
		self.air_res_inv = 1 - air_res

		self.bouncy 		= bounciness 	# 0 to 1, measure of how much velocity (momentum) is returned during a bounce, and inverse of how much is absorbed for the sound
		self.sound_wallhits	= wallhit_soundlist
		self.change_sound_wallhit()
		
		self.frames_left = frames_left		# frames left before the ball is automatically killed. -1 for infinite
		self.instances.insert(0,self)		# prepend to instances so that the oldest Ball gets drawn last and therefore gets drawn over everything else

	def kill(self):							# automatically called during a move attempt if frames_left is exhausted
		Ball.instances.remove(self)
		del self

	def update_rect_pos(self, new_centre_x=None, new_centre_y=None):			# add=False?
		if new_centre_x is not None: self.true_centre_x = new_centre_x
		if new_centre_y is not None: self.true_centre_y = new_centre_y
		
		self.rect.center = int(round_float(self.true_centre_x)), int(round_float(self.true_centre_y))

	def move(self):
		if self.frames_left > 0:
			self.frames_left -= 1 			# decremeneted here as this function's called every frame
			if self.frames_left == 0: self.kill()

		self.update_rect_pos(self.true_centre_x + self.velocity[0], self.true_centre_y + self.velocity[1])

	def randomise_velocity(self):
		self.velocity = [randint(-self.MAX_SPEED*10, self.MAX_SPEED*10)/10, randint(-self.MAX_SPEED*10, self.MAX_SPEED*10)/10]

	def randomise_pos(self):
		self.update_rect_pos(randint(self.rect.width//2, WIDTH-self.rect.width//2), randint(self.rect.height//2, HEIGHT-self.rect.height//2))

	def dash(self, direction):				# no switch statement pepesad
		if direction == pygame.K_RIGHT:  self.velocity[0] = self.velocity[0] + self.DASH_SPEED if self.velocity[0] >= 0 else self.DASH_SPEED
		elif direction == pygame.K_DOWN: self.velocity[1] = self.velocity[1] + self.DASH_SPEED if self.velocity[1] >= 0 else self.DASH_SPEED
		elif direction == pygame.K_LEFT: self.velocity[0] = self.velocity[0] - self.DASH_SPEED if self.velocity[0] <= 0 else self.DASH_SPEED
		else:                            self.velocity[1] = self.velocity[1] - self.DASH_SPEED if self.velocity[1] <= 0 else self.DASH_SPEED

	def change_grav_magnitude(self, increase=True):
		if increase:
			if self.grav_magnitude < self.MAX_GRAVITY: self.grav_magnitude += self.GRAVITY_INC				# increase gravity only if current < |MAX_GRAVITY|
		elif self.grav_magnitude > -self.MAX_GRAVITY:  self.grav_magnitude -= self.GRAVITY_INC
		self.calculate_gravity()

	def change_grav_angle(self, cw=True):
		self.grav_angle = (self.grav_angle + self.ANGLE_INC)%360 if cw else (self.grav_angle - self.ANGLE_INC)%360
		self.calculate_gravity()

	def calculate_gravity(self):				# Only called when gravity needs to be changed/during initialisation. Remains constant other than that
		self.grav_vector = round_float(self.grav_magnitude * cos(radians(self.grav_angle)), 2), round_float(self.grav_magnitude * sin(radians(self.grav_angle)), 2)

	def grav_airres_update(self):
		self.velocity = [(self.velocity[0]+self.grav_vector[0]) * self.air_res_inv, (self.velocity[1]+self.grav_vector[1]) * self.air_res_inv]

	def change_airres(self,increase=True):
		if increase:
			if self.air_res_inv < 1: self.air_res_inv += self.air_res_inv_INC
		elif self.air_res_inv > 0: 	 self.air_res_inv -= self.air_res_inv_INC

	def change_bouncy(self, increase=True):
		if increase:
			if self.bouncy < 1: self.bouncy += self.BOUNCY_INC
		elif self.bouncy > 0: 	self.bouncy -= self.BOUNCY_INC
		self.change_sound_wallhit()

	def change_sound_wallhit(self):
		for index in range(len(self.sound_wallhits)):
			if self.bouncy <= (index+1)/len(self.sound_wallhits):				# some func for changing wallhit sfx according to how bouncy the ball is
				self.sound_wallhit = self.sound_wallhits[index]
				return
		else:									# this part will only be reached if bouncy=1
			self.sound_wallhit = self.sound_wallhits[-1]

	def check_wall_collision(self, clones=False):
		# Of course, since i can't do things the physics way (calculating normal and then angle of incidence/reflection and all that shit), and i don't really need to because of rectangular walls and no way to change that... not gon be torturing myself any more, just normal velocity correction
		if (self.rect.left < 0 and self.velocity[0] < 0) or (self.rect.right > WIDTH and self.velocity[0] > 0):		# if out of bounds and continuing to go out of bounds (if vel_x = 0, do nothing and let the ball stay as if resting on the surface)
			self.on_wall_collision(0,clones)
		if (self.rect.top < 0 and self.velocity[1] < 0) or (self.rect.bottom > HEIGHT and self.velocity[1] > 0):	# same here, for vertical
			self.on_wall_collision(1,clones)

	def on_wall_collision(self, vel_index, clones):			# ...just how many methods am i even making to avoid copypasting code
		if abs(self.velocity[vel_index]) > 4 * abs(self.grav_magnitude):
			self.velocity[vel_index] = -self.velocity[vel_index] * self.bouncy
			self.play_wallhit(self.velocity[vel_index])
			if clones: self.spawn_clone(self.img, (1,2), 0.5, FRAMERATE*1)
		else:
			self.velocity[vel_index] = 0					# to keep the ball resting on the ground instead of repeatedly falling through it when the velocity is low enough

	def play_wallhit(self, collision_speed):
		channel = pygame.mixer.find_channel(True)
		channel.set_volume(collision_speed/self.MAX_SPEED * (1-self.bouncy) * self.VOLUME_MULT)
		channel.play(self.sound_wallhit)

	def spawn_clone(self, image=base_ball, number_range=(1,4), resize_factor=0.25, c_frames_left=FRAMERATE*4, velocity=None, c_gravity=0, bounciness=1):
		if not velocity: velocity = (self.velocity[0] * self.DUST_SPEED_RATIO, self.velocity[1] * self.DUST_SPEED_RATIO)

		for i in range(randint(number_range[0], number_range[1])):
			temp_resize_factor	= variance(resize_factor)
			temp_img 			= pygame.transform.scale( image, (int(image.get_width()*temp_resize_factor), int(image.get_height()*temp_resize_factor)) )
			temp_velocity		= (variance(velocity[0]), variance(velocity[1]))
			temp_spawn_area		= (int(self.rect.width*UNIVERSAL_VARIANCE), int(self.rect.height*UNIVERSAL_VARIANCE))
			temp_spawn			= randint(self.rect.left - temp_spawn_area[0], self.rect.right + temp_spawn_area[0]), randint(self.rect.top - temp_spawn_area[1], self.rect.bottom + temp_spawn_area[1])
			temp_bouncy			= variance(bounciness)
			if temp_bouncy<0: temp_bouncy = 0				# not as much concerned about temp_bouncy exceeding 1, as temp_bouncy<0 would keep reversing the velocity on wall collision

			Ball(temp_img, spawn=temp_spawn, bounciness=temp_bouncy, frames_left=int(variance(c_frames_left)), velocity=temp_velocity, gravity=variance(c_gravity))


class FontBall(Ball):
	'''Ball object with font data because why not'''
	VOLUME_MULT = 1.5
	INTERLINE_SPACE_RATIO = 0.125
	#FONT_VARIANCE = 3
	FONTS = ("timesnewroman","comicsansms","arialblack","calibri",None,"impact","verdana","couriernew")
	def __init__(self, f_text: str, font_name: str, font_size: int, font_colour: tuple, spawn=MIDPOINT, wallhit_soundlist=wallhit_sounds, f_frames_left=-1, f_gravity=0.2, f_bold=False, f_italic=True):
		self.font = pygame.font.SysFont(font_name, font_size, f_bold, f_italic)
		self.COLOUR = font_colour

		super().__init__(self.make_multiline_img(f_text,font_size) if "\n" in f_text else self.font.render(f_text, True, self.COLOUR), spawn, wallhit_soundlist, frames_left=f_frames_left, gravity=f_gravity)

	def render(self, text):					# called when new text needs to be rendered, like in FpsCounter or any randomchance easter eggs
		self.img = self.og_img = self.font.render(text, True, self.COLOUR)
		self.old_topright = self.rect.topright
		self.rect = self.og_img.get_rect()
		self.rect.topright = self.old_topright

	def make_multiline_img(self, text, font_size):
		split_text = text.split("\n")
		font_rect_list = []
		font_img_list  = []
		current_font_top = 0

		for line in split_text:
			temp_font_size  = int(variance(font_size))
			interline_space = int(font_size * self.INTERLINE_SPACE_RATIO)
			temp_font = pygame.font.SysFont(choice(self.FONTS), temp_font_size, bool(randint(0,1)), bool(randint(0,1)))

			temp_img  = temp_font.render(line, False, self.COLOUR)
			font_img_list.append(temp_img)
			temp_rect = temp_img.get_rect()
			temp_rect.midtop = MIDPOINT[0], current_font_top
			font_rect_list.append(temp_rect)
			current_font_top += temp_rect.height + interline_space

		joined_rect = font_rect_list[0].unionall(font_rect_list[1:])
		joined_img  = pygame.Surface(joined_rect.size)
		joined_img.fill((255,255,255))
		joined_img.set_colorkey((255,255,255))

		for index in range(len(font_rect_list)):
			font_rect_list[index].centerx = joined_rect.width//2
			joined_img.blit(font_img_list[index], font_rect_list[index])

		return joined_img


class FpsCounter(FontBall):
	'''FontBall + keeping track of the framerate'''
	VOLUME_MULT = 1
	def __init__(self, f_text, font_name, font_size, font_colour, update_int: float, spawn, wallhit_soundlist=wallhit_sounds, bounce_limit=-1, f_gravity=0.2, f_bold=True, f_italic=False, round_frames=2, update_interval=0.5):
		super().__init__(f_text, font_name, font_size, font_colour, spawn, wallhit_soundlist, bounce_limit, f_gravity, f_bold, f_italic)
		self.rect.topright = spawn 		# anchor this bad boy to topright
		
		self.UPDATE_INTERVAL = update_interval		# interval (in s) after which the fps will be calculated and the text updated
		self.ROUND = round_frames
		self.time = 0					# ms since last update; will be reset after a pause
		self.frames = 0

	def reset(self):					# called automatically in check(); call this to manually reset
		self.time = pygame.time.get_ticks()
		self.frames = 0

	def check(self):#*
		self.frames += 1
		time_difference = (pygame.time.get_ticks() - self.time)/1000
		if time_difference >= self.UPDATE_INTERVAL:
			self.render(f"FPS: {round_float(self.frames/time_difference, self.ROUND)}")
			self.reset()

# utility funcs
def round_float(x,tolerance=0):
	tolerance = 10**tolerance
	return int(x*tolerance + 0.5)/tolerance if x > 0 else int(x*tolerance - 0.5)/tolerance

def variance(x):						# instead of UNIVERSAL_VARIANCE, i could also pass in a variance argument to customise variance
	return x * randint( int((1-UNIVERSAL_VARIANCE) * 10**VARIANCE_DIGITS), int((1+UNIVERSAL_VARIANCE) * 10**VARIANCE_DIGITS) )/10

def calculate_angle(point2, origin=MIDPOINT):
	if point2 == origin:   return 0
	difference = point2[0] - origin[0], point2[1] - origin[1]
	if difference[0] == 0: return 90 if difference[1] > 0 else 270
	b_a_a = degrees(atan(abs(difference[1]/difference[0])))

	if difference[1] <= 0: horizontal_quadrant = 3,4		# would've normally used a single line statement, but this is descriptive
	else:                  horizontal_quadrant = 2,1
	horizontal_quadrant = horizontal_quadrant[0] if difference[0] < 0 else horizontal_quadrant[1]

	return 360-b_a_a if horizontal_quadrant==4 else 180+b_a_a if horizontal_quadrant==3 else 180-b_a_a if horizontal_quadrant == 2 else b_a_a


def adios():
	for ball in Ball.instances:
		ball.grav_angle = calculate_angle(ball.rect.center)
		ball.grav_magnitude = 0.1				# to give more time to appreciate this useless ass feature
		ball.calculate_gravity()

	balls_onscreen = True
	while balls_onscreen:
		pygame.event.clear()
		fps_counter.check()

		display.fill(BG_COLOUR)
		balls_onscreen = False
		for ball in Ball.instances:
			ball.grav_airres_update()
			ball.move()
			display.blit(ball.img, ball.rect)
			# if we manage to get through the for loop without any balls being in screen range, adios away
			if ball.rect.right>0 and ball.rect.left<WIDTH and ball.rect.bottom>0 and ball.rect.top<HEIGHT:
				balls_onscreen = True

		pygame.display.flip()
		clock.tick(FRAMERATE)		

	pygame.quit()
	raise SystemExit			# since exit() apparently doesn't like to work with executables?	


def initialise():
	# start up the screen and shit
	global display, main_ball, intro_ball, fps_counter, pause_ball, gameloop_key_funcs
	display = pygame.display.set_mode(DISPLAY)
	pygame.display.set_caption("le ballse")

	pygame.event.set_blocked(None)		# contrary to how this reads, this blocks ALL events from entering the queue
	pygame.event.set_allowed((pygame.KEYDOWN, pygame.QUIT))

	pygame.mixer.set_num_channels(16)
	
	fps_counter = FpsCounter("FPS: ", "comicsansms", 20, (40,40,80), 0.5, (int(15/16 * WIDTH), int(1/16 * HEIGHT)))		# this will always be the top ball (:flushe:)
	intro_ball  = FontBall(intro_text_content, "arial", 30, (0,0,0))
	main_ball   = Ball(base_ball)

	pause_ball  = FontBall("game pauseth.\npresses p to unpause,\nor q to q u i t", "comicsansms", 40, (80,40,120))
	pause_ball.air_res_inv = 1
	pause_ball.grav_magnitude = 0
	pause_ball.calculate_gravity()
	Ball.instances.remove(pause_ball)

	# time for the worst trickery known to man
	gameloop_key_funcs = {
		pygame.K_RIGHT : main_ball.dash,
		pygame.K_DOWN  : main_ball.dash,
		pygame.K_LEFT  : main_ball.dash,
		pygame.K_UP    : main_ball.dash,

		pygame.K_q : pause_loop,
		pygame.K_g : main_ball.change_grav_magnitude,
		pygame.K_a : main_ball.change_grav_angle,
		pygame.K_b : main_ball.change_bouncy,
		pygame.K_r : main_ball.change_airres,
		pygame.K_o : main_ball.randomise_velocity,
		pygame.K_p : main_ball.randomise_pos,
		pygame.K_c : main_ball.spawn_clone
	}


def pause_loop():
	Ball.instances.insert(-2, pause_ball)
	pause_ball.randomise_velocity()
	pause_ball.randomise_pos()

	paused = True
	while paused:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:   paused = False
				elif event.key == pygame.K_q: adios()

		pause_ball.grav_airres_update()
		pause_ball.check_wall_collision()
		pause_ball.move()
		fps_counter.check()

		display.fill(BG_COLOUR)
		for ball in Ball.instances: display.blit(ball.img, ball.rect)
		pygame.display.flip()
		clock.tick(FRAMERATE)

	Ball.instances.remove(pause_ball)
	

def menu_loop():
	intro_ball.update_rect_pos(new_centre_y=-intro_ball.rect.height)
	fps_counter.reset()

	introtext_gravity_switch = 2			# decreases each time gravity switches; at 0 it gives up and stops at MIDPOINT 
	menu_active = True
	while menu_active:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN: menu_active = False
			elif event.type == pygame.QUIT:  adios()

		if randint(1,300) == 1: main_ball.randomise_velocity()
		main_ball.check_wall_collision()

		if introtext_gravity_switch==0 and intro_ball.rect.centery>=MIDPOINT[1]:
			intro_ball.update_rect_pos(MIDPOINT[0], MIDPOINT[1])
		else:
			intro_ball.grav_airres_update()
			intro_ball.move()
			if (introtext_gravity_switch==2 and intro_ball.rect.centery>=MIDPOINT[1]) or (introtext_gravity_switch==1 and intro_ball.rect.centery<=MIDPOINT[1]):
				intro_ball.grav_magnitude *= -1
				intro_ball.calculate_gravity()
				introtext_gravity_switch -= 1

		main_ball.move()
		display.fill(BG_COLOUR)
		fps_counter.check()

		for ball in Ball.instances: display.blit(ball.img, ball.rect)
		pygame.display.flip()
		clock.tick(FRAMERATE) 			# tick_busy_loop for more accurate but cpu heavy func
		#clock.get_fps()


def game_loop():
	main_ball.bouncy = 0.8
	main_ball.change_sound_wallhit()
	intro_ball.randomise_velocity()
	fps_counter.randomise_velocity()

	game_active = True
	while game_active:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				try:              gameloop_key_funcs[event.key]()
				except TypeError: gameloop_key_funcs[event.key](event.key)						# some funcs require argument; for now that argument's always the key number
				except KeyError:  pass
			elif event.type == pygame.QUIT: adios()

		display.fill(BG_COLOUR)
		fps_counter.check()
		for index,ball in enumerate(Ball.instances):
			ball.grav_airres_update()
			ball.check_wall_collision(True if index==len(Ball.instances)-3 else False)			# spawn clones only for 3rd last ball (main_ball), at least for now
			ball.move()
			display.blit(ball.img, ball.rect)

		pygame.display.flip()

		clock.tick(FRAMERATE)



if __name__ == "__main__":
	initialise()
	menu_loop()
	game_loop()
