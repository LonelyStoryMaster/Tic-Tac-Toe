import math
import pygame
from pygame.color import Color

from GameSquareClass import GameSquare
from Util import Winners, Colors

class Board:
	def __init__(self, background, dimensions, line_color=Colors.WHITISH, x_color=Colors.RED, o_color=Colors.BLUE, bg_color = Colors.GREY, amount_boards=(1, 1), hasBorder=True, origin=[0,0]):
		# self.display = display
		self.background = background
		self.dimensions = dimensions
		self.square_size = 0
		self.border_offset = 0
		self.height = self.dimensions[1]
		self.width = self.dimensions[0]
		self.line_weight = 0
		self.piece_line_weight = 0
		self.origin = origin
		self.bordered_origin = self.origin
		self.end_point = None
		self.center_point = None
		self.amount_boards = amount_boards
		self.hasBorder = hasBorder
		self.bg_color = bg_color
		self.line_color = line_color
		self.x_color = x_color
		self.o_color = o_color
		self.current_color = self.x_color.value
		self.winner = Winners.NONE
		self.game_won = False
		self.win_line_drawn = False
		self.play_made = False
		self.squares_disabled = False
		self.current_player = Winners.X
		self.running = 1  # If this is 0, close the window
		self.board_contents = [ ]
		self.win_condition_pos = [[[0, 0], [0, 1], [0, 2]], [[1, 0], [1, 1], [1, 2]], [[2, 0], [2, 1], [2, 2]],
                   				   [[0, 0], [1, 0], [2, 0]], [[0, 1], [1, 1],
                   				       [2, 1]], [[2, 0], [1, 1], [0, 2]],
                   				   [[0, 0], [1, 1], [2, 2]], [[2, 0], [1, 1], [0, 2]]]

		# Generate the necessary values to draw the board
		self.__gen_board_vals()

		# Generate the neccesary amount of spaces for desired board size
		self.__gen_board_contents()

		# Draw the board using whichever origin is necessary
		self.__draw_board()

		# Generate the each square in the game
		self.__gen_game_squares()

	# Used to calculate the necessary values to draw the board properly. Only used on creation of new object
	def __gen_board_vals(self):
		num_columns = max( self.amount_boards[0], 3 )
		if self.hasBorder:
			num_columns += 1
		self.square_size = int( math.ceil( self.width / num_columns ) )
		self.line_weight = int(math.ceil(self.square_size * 0.08))		# Trial and error number that looks nice
		self.piece_line_weight = int( self.line_weight * 0.86 )
		self.border_offset = math.ceil( self.square_size / 2 )			# Using the offset to create a modified origin point
		self.bordered_origin = ( ( self.origin[0] + self.border_offset ), ( self.origin[1] + self.border_offset ) )
		
		# Modify the origin values if necessary
		self.__modify_origin()
		
		self.end_point = ( ( self.origin[0] + self.square_size ), ( self.origin[1] + self.square_size ) )
		self.center_point = ( ( self.origin[0] + int( self.square_size / 2 ) ), ( self.origin[1] + int( self.square_size / 2 ) ) )

	# Generate number of squares needed for desired game size
	def __gen_board_contents(self):
		for row in range( max( self.amount_boards[0], 3 ) ):
			new_row = [ ]
			for col in range( max( self.amount_boards[1], 3 ) ):
				new_row.append(None)
			self.board_contents.append(new_row)

	# If game has a border replace self.origin data with self.bordered_origin data
	def __modify_origin(self):
		if self.hasBorder:
			self.origin = self.bordered_origin

	# Drawing the actual lines of the board. Only used on creation of new object
	def __draw_board(self):
		num_rows = len( self.board_contents )
		num_cols = len( self.board_contents[1] )
		for row in range( 1, num_rows ):
			# pygame.draw.line(self.background, self.line_color.value, ( ( self.origin[0] + self.square_size), self.origin[1] ), ( ( self.origin[0] + self.square_size ), ( self.origin[1] + ( self.square_size * 3 ) ) ), self.line_weight)
			pygame.draw.line(self.background, self.line_color.value, ( ( self.origin[0] +  ( self.square_size * row ) ), self.origin[1]), ( ( self.origin[0] + ( self.square_size * row ) ), ( self.origin[1] + ( self.square_size * num_rows ) ) ), self.line_weight)
		for col in range ( 1, num_cols ):
			# pygame.draw.line(self.background, self.line_color.value, ( self.origin[0], ( self.origin[1] + self.square_size ) ), ( ( self.origin[0] + ( self.square_size * 3 ) ), ( self.origin[1] + self.square_size ) ), self.line_weight)
			pygame.draw.line(self.background, self.line_color.value, ( self.origin[0], ( self.origin[1] + ( self.square_size * col ) ) ), ( ( self.origin[0] + ( self.square_size * num_cols ) ), ( self.origin[1] + ( self.square_size * col ) ) ), self.line_weight)

	# Generating the squares
	def __gen_game_squares(self):
		current_origin = self.origin
		for row in range( len( self.board_contents ) ):
			for col in range( len( self.board_contents[ row ] ) ):
				# Creating a new GameSquare or Board depending on the game size
				if ( self.amount_boards[0] > 1 ):
					self.board_contents[row][col] = Board(self.background, ( self.square_size, self.square_size ), line_color=self.line_color, x_color=self.x_color, o_color=self.o_color, origin=current_origin)
				else:
					self.board_contents[row][col] = GameSquare(current_origin, self.square_size)
				self.board_contents[row][col].set_Winner(Winners.NONE)

				# Incrementing over on each row to get the starting corner of the square
				current_origin = [ ( current_origin[0] + self.square_size  ), current_origin[1] ]

			# Setting the X coord back to the game origin when moving down a row
			current_origin = [ self.origin[0], ( current_origin[1] + self.square_size ) ]

	def __is_game_won(self):
		for condition in self.win_condition_pos:
			pos1 = condition[0]
			pos2 = condition[1]
			pos3 = condition[2]

			square1 = self.board_contents[ pos1[0] ][ pos1[1] ]
			square2 = self.board_contents[ pos2[0] ][ pos2[1] ]
			square3 = self.board_contents[ pos3[0] ][ pos3[1] ]

			if ( square1.get_Winner() == square2.get_Winner() == square3.get_Winner() ):
				if ( ( square1.get_Winner() == Winners.X ) or ( square1.get_Winner() == Winners.O ) ):
					self.winner = square1.get_Winner()
					
					if not self.win_line_drawn:
						self.__draw_Winner_Line(self.background, square1, square3, Colors.BLACK.value, self.line_weight)
						self.win_line_drawn = True

					self.game_won = True
					break
				
	def __is_square_played(self, play_square):
		if ( play_square.get_Winner() != Winners.NONE ):
			return True

	def __switch_players(self):
		print(self.current_player)
		if ( self.current_player == Winners.X ):
			self.current_player = Winners.O
			self.current_color = self.o_color.value
		elif ( self.current_player == Winners.O):
			self.current_player = Winners.X
			self.current_color = self.x_color.value
		else:
			self.current_player = Winners.NONE

	def __draw_play(self, square):
		if ( self.current_player == Winners.X ):
			self.__draw_X( square.get_Origin(), square.get_End_Point(), square.get_Side_Length() )
		elif ( self.current_player == Winners.O ):
			self.__draw_O( square.get_Center_Point(), square.get_Side_Length() )

	def __draw_X(self, origin, endpoint, square_size):
		offset = square_size * 0.12		# Inset the X a little so it's not right agianst the square's edges
		upper_left_pos = ( ( origin[0] + offset ), ( origin[1] + offset ) )
		lower_left_pos = ( ( origin[0] + offset ), ( endpoint[1] - offset ) )
		upper_right_pos = ( ( endpoint[0] - offset ), ( origin[1] + offset ) )
		lower_right_pos = ( ( endpoint[0] - offset ), ( endpoint[1] - offset ) )
		self.__draw_Rounded_Line(self.background, self.current_color, upper_left_pos, lower_right_pos, self.piece_line_weight)
		self.__draw_Rounded_Line(self.background, self.current_color, lower_left_pos, upper_right_pos, self.piece_line_weight)

	def __draw_O(self, centerpoint, square_size):
		diameter = square_size * 0.8		# The percent the circle is of the size of the square. Whatever looked nice
		pygame.draw.circle(self.background, self.current_color, centerpoint, ( diameter / 2 ), self.piece_line_weight)

	def __draw_Rounded_Line(self, surface, color, start_pos, end_pos, width):
		pygame.draw.line(surface, color, start_pos, end_pos, width)
		pygame.draw.circle(surface, color, start_pos, int( width * 0.45 ) )
		pygame.draw.circle(surface, color, end_pos, int( width * 0.45 ) )

	def __draw_Winner_Line(self, surface, square1, square2, color, width, hv_exstension=0.15):
		square1_center_pos = square1.get_Center_Point()
		square1_side_length = square1.get_Side_Length()
		square1_origin = square1.get_Origin()
		square1_end_point = square1.get_End_Point()

		square2_center_pos = square2.get_Center_Point()
		square2_side_length = square2.get_Side_Length()
		square2_origin = square2.get_Origin()
		square2_end_point = square2.get_End_Point()

		square1_offsets = ( int( ( square1_center_pos[0] - square1_origin[0] ) / 2 ), int( ( square1_center_pos[1] - square1_origin[1] ) / 2) )
		square2_offsets = ( int( ( square2_end_point[0] - square2_center_pos[0] ) / 2), int( ( square2_end_point[1] - square2_center_pos[1] ) / 2) )

		rise = square2_center_pos[1] - square1_center_pos[1]
		run = square2_center_pos[0] - square1_center_pos[0]
		
		if (run == 0):
			slope = None
		else:
			slope = ( rise / run )

		start_pos = 0
		end_pos = 0

		if ( slope == None):
			start_pos = ( square1_center_pos[0], ( square1_center_pos[1] - int( square1_side_length * hv_exstension ) ) )
			end_pos = ( square2_center_pos[0], ( square2_center_pos[1] + int( square2_side_length * hv_exstension ) ) )
		elif ( slope == 0 ):
			start_pos = ( ( square1_center_pos[0] - int( square1_side_length * hv_exstension ) ), square1_center_pos[1] )
			end_pos = ( ( square2_center_pos[0] + int( square2_side_length * hv_exstension ) ), square2_center_pos[1] )
		elif ( slope > 0 ):
			start_pos = ( ( square1_origin[0] + square1_offsets[0] ), ( square1_origin[1] + square1_offsets[1] ) )
			end_pos = ( ( square2_end_point[0] - square2_offsets[0] ), ( square2_end_point[1] - square2_offsets[1] ) )
		elif ( slope < 0):
			start_pos = ( ( square1_center_pos[0] - square1_offsets[0] ), ( square1_center_pos[1] + square1_offsets[1] ) )
			end_pos = ( ( square2_end_point[0] - square2_offsets[0] ), ( square2_origin[1] + square2_offsets[1] ) )
		
		print( start_pos, end_pos )
		self.__draw_Rounded_Line(surface, color, start_pos, end_pos, width)

	def __disable_Squares(self):
		for row in range( len( self.board_contents ) ):
			for col in range( len( self.board_contents[ row ] ) ):
				square = self.board_contents[ row ][ col ]
				if ( ( square.get_Winner() != Winners.X ) and ( square.get_Winner() != Winners.O ) ):
					# print( [ row, col ] )
					square.set_Winner(Winners.DRAW)

	def check_Squares(self, pos_to_check):
		for row in range( len( self.board_contents ) ):
			for col in range( len( self.board_contents[ row ] ) ):
				square_to_check = self.board_contents[ row ][ col ]

				if isinstance(square_to_check, Board):
					square_to_check.check_Squares(pos_to_check)
				else:
					if  ( square_to_check.is_In_Square( pos_to_check ) and not self.__is_square_played( square_to_check ) ):
						square_to_check.set_Winner(self.current_player)
						self.play_made = True
						self.__draw_play(square_to_check)

	def get_Winner(self):
		return self.winner

	def get_Center_Point(self):
		return self.center_point

	def get_End_Point(self):
		return self.end_point

	def set_Winner(self, winner):
		self.winner = winner

	def set_Current_Player(self, player_to_set):
		self.current_player = player_to_set

	def update_Board(self, display):
		if ( self.amount_boards[0] > 1 ):
			for col in range( len( self.board_contents ) ):
				for row in range( len( self.board_contents[ col ] ) ):
					self.board_contents[row][col].update_Board(display)
		self.__is_game_won()
		if self.game_won:
			if not self.squares_disabled:
				self.__disable_Squares()
				self.squares_disabled = True
		else:
			if self.play_made:
				self.__switch_players()
				self.play_made = False			
		display.blit(self.background, (0,0))
		pygame.display.flip()
