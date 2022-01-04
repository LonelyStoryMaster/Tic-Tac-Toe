import math
import pygame

from GameSquareClass import GameSquare
from Util import Winners, Colors

class Board:
	def __init__(self, background, line_color=Colors.WHITISH, x_color=Colors.RED, o_color=Colors.BLUE, bg_color = Colors.GREY, isInBigBoard=False, hasBorder=True, origin=[0,0]):
		# self.display = display
		self.background = background
		self.square_size = 0
		self.border_offset = 0
		self.window_height = 0
		self.window_width = 0
		self.line_weight = 0
		self.piece_line_weight = 0
		self.origin = origin
		self.bordered_origin = None
		self.isInBigBoard = isInBigBoard
		self.hasBorder = hasBorder
		self.bg_color = bg_color.value
		self.line_color = line_color.value
		self.x_color = x_color.value
		self.o_color = o_color.value
		self.current_color = self.x_color
		self.winner = Winners.NONE
		self.current_player = Winners.X
		self.running = 1  # If this is 0, close the window
		self.board_contents = [ [ None, None, None ],
								[ None, None, None ],
								[ None, None, None ]]
		self.win_condition_pos = [[[0, 0], [0, 1], [0, 2]], [[1, 0], [1, 1], [1, 2]], [[2, 0], [2, 1], [2, 2]],
                   				   [[0, 0], [1, 0], [2, 0]], [[0, 1], [1, 1],
                   				       [2, 1]], [[2, 0], [1, 1], [0, 2]],
                   				   [[0, 0], [1, 1], [2, 2]], [[2, 0], [1, 1], [0, 2]]]

		# Generate the necessary values to draw the board
		self.__gen_board_vals()

		# Modify the origin values if necessary
		self.__modify_origin()

		# Draw the board using whichever origin is necessary
		self.__draw_board()

		# Generate the each square in the game
		self.__gen_game_squares()

	# Used to calculate the necessary values to draw the board properly. Only used on creation of new object
	def __gen_board_vals(self):
		self.window_width = self.background.get_size()[0]
		self.window_height = self.background.get_size()[1]
		num_boards = 1
		if self.isInBigBoard:
			num_boards = 9
		sqrt_boards = math.sqrt(num_boards)			# Gets how many games need to fit across the screen
		num_columns = 0
		if self.hasBorder:
			num_columns = sqrt_boards * 4 			# Need 4 columns per board to have room for the borders
		else:
			num_columns = sqrt_boards * 3			# Only need 3 columns per board without borders
			num_columns = int( num_columns )
		self.square_size = int( math.ceil( self.window_width / num_columns ) )
		self.line_weight = int(math.ceil(self.square_size * 0.08))		# Trial and error number that looks nice
		self.piece_line_weight = int( self.line_weight * 0.86 )
		self.border_offset = math.ceil( self.square_size / 2 )			# Using the offset to create a modified origin point
		self.bordered_origin = [ ( self.origin[0] + self.border_offset ), ( self.origin[1] + self.border_offset )]

		# TODO: Add log printout to enable these
		# print(self.window_height, self.window_width, num_columns, self.square_size, self.border_offset, self.line_weight)

	# If game has a border replace self.origin data with self.bordered_origin data
	def __modify_origin(self):
		if self.hasBorder:
			self.origin = self.bordered_origin

	# Drawing the actual lines of the board. Only used on creation of new object
	def __draw_board(self):
		pygame.draw.line(self.background, self.line_color, ( ( self.origin[0] + self.square_size), self.origin[1] ), ( ( self.origin[0] + self.square_size ), ( self.origin[1] + ( self.square_size * 3 ) ) ), self.line_weight)
		pygame.draw.line(self.background, self.line_color, ( ( self.origin[0] +  ( self.square_size * 2 ) ), self.origin[1]), ( ( self.origin[0] + ( self.square_size * 2 ) ), ( self.origin[1] + ( self.square_size * 3 ) ) ), self.line_weight)
		pygame.draw.line(self.background, self.line_color, ( self.origin[0], ( self.origin[1] + self.square_size ) ), ( ( self.origin[0] + ( self.square_size * 3 ) ), ( self.origin[1] + self.square_size ) ), self.line_weight)
		pygame.draw.line(self.background, self.line_color, ( self.origin[0], ( self.origin[1] + ( self.square_size * 2 ) ) ), ( ( self.origin[0] + ( self.square_size * 3 ) ), ( self.origin[1] + ( self.square_size * 2 ) ) ), self.line_weight)

	# Generating the squares
	def __gen_game_squares(self):
		current_origin = self.origin
		for row in range( len( self.board_contents ) ):
			for col in range( len( self.board_contents[ row ] ) ):
				# Creating a new GameSquare with the current origin point and setting its winner to no-one
				self.board_contents[row][col] = GameSquare(current_origin, self.square_size)
				self.board_contents[row][col].set_Winner(Winners.NONE)

				# Draw a circle at the origin and end corner of each square
				# print(current_origin)
				# pygame.draw.circle(self.background, Colors.GREEN.value, current_origin, 3)
				# pygame.draw.circle(self.background, Colors.BLUE.value, self.board_contents[row][col].get_End_Point(), 9)

				# Incrementing over on each row to get the starting corner of the square
				current_origin = [ ( current_origin[0] + self.square_size  ), current_origin[1] ]

			# Setting the X coord back to the game origin when moving down a row
			current_origin = [ self.origin[0], ( current_origin[1] + self.square_size ) ]

	def __is_game_won(self):
		pass

	def __is_square_played(self, play_square):
		if play_square.get_Winner() != Winners.NONE:
			return True

	def __switch_players(self):
		if ( self.current_player == Winners.X ):
			self.current_player = Winners.O
			self.current_color = self.o_color
		elif ( self.current_player == Winners.O):
			self.current_player = Winners.X
			self.current_color = self.x_color
		else:
			self.current_player = Winners.NONE

	def __draw_play(self, square):
		if ( self.current_player == Winners.X ):
			self.__draw_X( square.get_Origin(), square.get_End_Point(), square.get_Square_Size() )
		elif ( self.current_player == Winners.O ):
			self.__draw_O( square.get_Center_Point(), square.get_Square_Size() )

	def __draw_X(self, origin, endpoint, square_size):
		x_offset = square_size * 0.12		# Have to offset differently due to how the lines are drawn
		y_offset = square_size * 0.08		# Numbers are just trial and error for what looks nice
		upper_left_pos = ( ( origin[0] + x_offset ), ( origin[1] + y_offset ) )
		lower_left_pos = ( ( origin[0] + x_offset ), ( endpoint[1] - y_offset ) )
		upper_right_pos = ( ( endpoint[0] - x_offset ), ( origin[1] + y_offset ) )
		lower_right_pos = ( ( endpoint[0] - x_offset ), ( endpoint[1] - y_offset ) )
		pygame.draw.line(self.background, self.current_color, upper_left_pos, lower_right_pos, self.piece_line_weight)
		pygame.draw.line(self.background, self.current_color, lower_left_pos, upper_right_pos, self.piece_line_weight)

	def __draw_O(self, centerpoint, square_size):
		diameter = square_size * 0.8		# The percent the circle is of the size of the square. Whatever looked nice
		pygame.draw.circle(self.background, self.current_color, centerpoint, ( diameter / 2 ), self.piece_line_weight)

	def check_Squares(self, pos_to_check):
		for row in range( len( self.board_contents ) ):
			for col in range( len( self.board_contents[ row ] ) ):
				square_to_check = self.board_contents[ row ][ col ]
				if  ( square_to_check.is_In_Square( pos_to_check ) and not self.__is_square_played( square_to_check ) ):
					square_to_check.set_Winner(self.current_player)
					self.__draw_play(square_to_check)
					self.__switch_players()

	def update_Board(self, display):
		# self.__is_game_won()
		display.blit(self.background, (0,0))
		pygame.display.flip()
