import math, pygame

class SmallBoard:
    def __init__(self, ttt, startx, starty, colWidth, background, lineColor, xcolor, ocolor):
        self.XO   = "X"   # track whose turn it is; X goes first
        self.grid = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
        self.win_condition_pos = [[[0,0],[0,1],[0,2]], [[1,0],[1,1],[1,2]], [[2,0],[2,1],[2,2]],
                   [[0,0],[1,0],[2,0]], [[0,1],[1,1],[2,1]], [[0,2],[1,2],[2,2]],
                   [[0,0],[1,1],[2,2]], [[2,0],[1,1],[0,2]]]
        self.background = background
        self.won = False
        self.win_token = ' '
        self.colWidth = colWidth
        self.line_weight = math.ceil(self.colWidth * 0.08)
        self.startX = startx
        self.startY = starty
        self.center_coords = self.return_center()
        self.line_color = lineColor
        self.x_color = xcolor
        self.o_color = ocolor

        # draw the grid lines
        pygame.draw.line (self.background, self.line_color, (startx + self.colWidth, starty), (startx + self.colWidth, starty + (self.colWidth * 3)), self.line_weight)
        pygame.draw.line (self.background, self.line_color, (startx + (self.colWidth * 2), starty), (startx + (self.colWidth * 2), starty + (self.colWidth * 3)), self.line_weight)
        pygame.draw.line (self.background, self.line_color, (startx, starty + self.colWidth), (startx + (self.colWidth * 3), starty + self.colWidth), self.line_weight)
        pygame.draw.line (self.background, self.line_color, (startx, starty + (self.colWidth * 2)), (startx + (self.colWidth * 3), starty + (self.colWidth * 2)), self.line_weight)

    def __is_played(self, move_pos):
        # Pass in a list for the pos
        return (self.grid[move_pos[0]][move_pos[1]] != ' ')

    def __check_for_draw(self):
        return ((' ' not in self.grid[0]) and (' ' not in self.grid[1]) and (' ' not in self.grid[2]))

    def __check_for_win(self):
        for condition in self.win_condition_pos:
            pos1 = condition[0]
            pos2 = condition[1]
            pos3 = condition[2]
            board = self.grid
            if board[pos1[0]][pos1[1]] == board[pos2[0]][pos2[1]] == board[pos3[0]][pos3[1]] != ' ':
                if self.won is False:
                    # Drawing lineshit
                    startx = (pos1[1] + 1) * self.colWidth - (self.colWidth / 2)
                    starty = (pos1[0] + 1) * self.colWidth - (self.colWidth / 2)
                    endx = (pos3[1] + 1) * self.colWidth - (self.colWidth / 2)
                    endy = (pos3[0] + 1) * self.colWidth - (self.colWidth / 2)
                    # Setting winner stuff
                    self.won = True
                    self.win_token = board[pos1[0]][pos1[1]]
                    # Change of color for win line
                    if self.win_token == 'X':
                        # Draw red for X
                        pygame.draw.line (self.background, self.x_color, (startx + self.startX, starty + self.startY), (endx + self.startX, endy + self.startY), self.line_weight)
                    else:
                        # And blue for O
                        pygame.draw.line (self.background, self.o_color, (startx + self.startX, starty + self.startY), (endx + self.startX, endy + self.startY), self.line_weight)
        return self.won

    def return_center(self):
        return (self.startX + (self.colWidth * 1.5), self.startY + (self.colWidth * 1.5))
    
    def showBoard (self, ttt):
        ttt.blit (self.background, (0, 0))
        pygame.display.flip()

    def boardPos (self, mouseX, mouseY):
        row = None
        col = None
        # determine the row the user clicked
        if ((self.startY) < mouseY < ((self.colWidth * 1) + self.startY)):
            row = 0
        elif ((self.startY) < mouseY < ((self.colWidth * 2) + self.startY)):
            row = 1
        elif ((self.startY) < mouseY < ((self.colWidth * 3) + self.startY)):
            row = 2
        # determine the column the user clicked
        if ((self.startX) < mouseX < ((self.colWidth * 1) + self.startX)):
            col = 0
        elif ((self.startX) < mouseX < ((self.colWidth * 2) + self.startX)):
            col = 1
        elif ((self.startX) < mouseX < ((self.colWidth * 3) + self.startX)):
            col = 2

        # return the tuple containg the row & column
        return (row, col)
    
    def drawMove (self, boardRow, boardCol, Piece):
        # determine the center of the square
        centerX = int(((boardCol) * self.colWidth) + (self.colWidth / 2) + self.startX)
        centerY = int(((boardRow) * self.colWidth) + (self.colWidth / 2) + self.startY)

        piece_size = self.colWidth / 4.54545454545454

        # draw the appropriate piece
        if (Piece == 'O'):
            pygame.draw.circle (self.background, self.line_color, (centerX, centerY), int(piece_size * 2), int(self.line_weight / 1.5))
        else:
            pygame.draw.line (self.background, self.line_color, (centerX - piece_size, centerY - piece_size), \
                             (centerX + piece_size, centerY + piece_size), int(self.line_weight / 1.5))
            pygame.draw.line (self.background, self.line_color, (centerX + piece_size, centerY - piece_size), \
                             (centerX - piece_size, centerY + piece_size), int(self.line_weight / 1.5))

        # mark the space as used
        self.grid[boardRow][boardCol] = Piece
    
    def clickBoard(self, piece):
        (mouseX, mouseY) = pygame.mouse.get_pos()
        (row, col) = self.boardPos(mouseX, mouseY)

        # make sure no one's used this space
        if self.__is_played((row, col)) == True:
            return None

        # draw an X or O
        self.drawMove(row, col, piece)
        return (row, col)

    def gameWon(self):
        return self.__check_for_draw() or self.__check_for_win()