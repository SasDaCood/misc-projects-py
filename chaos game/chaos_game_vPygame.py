import pygame
from random import choice,randint
from time import time
pygame.init()


WIDTH,HEIGHT = 800,600
FONT_SIZE = 15
ITERSPEED_DELAY = 1
UPDATE_DELAY = 0.02
BG_COLOUR     = (255,255,255)
VERTEX_COLOUR = (180,0,0)
POINT_COLOUR  = (200,0,0,50)
fraction_to_travel = float(input("Fraction to travel (must be +ve): "))
if fraction_to_travel <= 0: pygame.quit(); exit()

scr = pygame.display.set_mode((WIDTH,HEIGHT))
scr.fill(BG_COLOUR)
pygame.display.set_caption(f"Choose at least 3 points w/ LMB, finish w/ RMB")
pygame.display.flip()
font      = pygame.font.SysFont("Calibri",FONT_SIZE,True)

vertices = []
iterations = 0
iter_time = time()
iter_count_sp = 0
update_time = time()
last_coords = randint(0,WIDTH-1), randint(0,HEIGHT-1)
choosing = True 														# choosing is the first stage where the user chooses points
while 1:
	for event in pygame.event.get():
		if choosing and event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:										# LMB is 1, RMB is 3
				vertices.append(event.pos)
				pygame.draw.circle(scr, VERTEX_COLOUR, event.pos, 4)
				pygame.display.flip()
				pygame.display.set_caption(f"{len(vertices)} points chosen; finish w/ RMB")

			elif event.button == 3 and len(vertices) >= 3:
				choosing = False
				break

		elif event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
			pygame.quit(); exit()

	if not choosing:
		chosen_point = choice(vertices)
		last_coords = round(last_coords[0] + (chosen_point[0] - last_coords[0]) * fraction_to_travel, 2), round(last_coords[1] + (chosen_point[1] - last_coords[1]) * fraction_to_travel, 2)
		rounded_coords = round(last_coords[0]), round(last_coords[1])
		
		scr.set_at(rounded_coords, POINT_COLOUR)
		iterations += 1
		iter_count_sp += 1

		if time() - update_time > UPDATE_DELAY:
			#pygame.draw.circle(scr, POINT_COLOUR, last_coords, 1)
			iter_img  = font.render(f"Iterations: {iterations}", True, (200,100,50))
			iter_rect = iter_img.get_rect()
			iter_rect.midleft = FONT_SIZE//2, FONT_SIZE
			pygame.draw.rect(scr, BG_COLOUR, iter_rect)
			scr.blit(iter_img, iter_rect)

			update_time = time()

		if time() - iter_time > ITERSPEED_DELAY:
			speed_img  = font.render(f"Iters/second: {iter_count_sp//(time() - iter_time)}", True, (230,100,50))
			speed_rect = speed_img.get_rect()
			speed_rect.midleft = FONT_SIZE//2, HEIGHT - FONT_SIZE
			pygame.draw.rect(scr, BG_COLOUR, speed_rect)
			scr.blit(speed_img, speed_rect)

			iter_time = time()
			iter_count_sp = 0

		pygame.display.flip()