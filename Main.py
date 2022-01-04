import math, pygame
from Util import Colors
from BoardClass import Board

def startGame( bg_color=Colors.GREY ):
	screen_width = pygame.display.Info().current_w
	screen_height = pygame.display.Info().current_h
	window_size = screen_height * 0.9	# Make the display just a little smaller than the maximum allowed
	print(screen_width)
	print(screen_height)
	
	gameDisplay = pygame.display.set_mode( ( window_size, window_size) )
	display_size = list(gameDisplay.get_size())
	# print(display_size)

	gameSurface = pygame.Surface( [ display_size[0], display_size[1] ] )
	gameSurface.convert()
	gameSurface.fill(bg_color.value)
	return ( gameDisplay, gameSurface )

pygame.init()

screens = startGame()

newBoard = Board(screens[1], screens[1].get_size(), line_color=Colors.WHITISH, hasBorder=True)

clock = pygame.time.Clock()

running = True
mouse_pos = ()

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse_pos = pygame.mouse.get_pos()
			newBoard.check_Squares(mouse_pos)
	newBoard.update_Board(screens[0])

	clock.tick(45)
	pygame.display.flip()

