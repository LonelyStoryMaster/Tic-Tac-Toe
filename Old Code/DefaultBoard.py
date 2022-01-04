import pygame
import math
from SmallBoard import SmallBoard

class TwoPlayerBoard:
    def __init__(self, num_boards, col_width, bg_color=(73,73,73), line_color=(214,214,214)):
        self.col_width = col_width
        self.line_weight = math.ceil(self.col_width * 0.12)
        self.num_boards = num_boards
        self.bg_color = bg_color
        self.line_color = line_color
        self.boards = []
        self.won = False
        self.XO = 'X'
        self.XColor = (250,0,0)
        self.OColor = (15,2,255)
        self.XOColor = (250,0,0)
        self.running = 1
        self.win_condition_pos = [[[0,0],[0,1],[0,2]], [[1,0],[1,1],[1,2]], [[2,0],[2,1],[2,2]],
                   [[0,0],[1,0],[2,0]], [[0,1],[1,1],[2,1]], [[2,0],[1,1],[0,2]],
                   [[0,0],[1,1],[2,2]], [[2,0],[1,1],[0,2]]]
        
    def __init_board(self, screen_size, num_boards):
        self.ttt = pygame.display.set_mode((screen_size))
        print(self.ttt)
        self.board_size = self.ttt.get_size()
        self.background = pygame.Surface(self.board_size)
        self.background = self.background.convert()
        self.background.fill(self.bg_color)

        # Board Size Thingy
        self.new_size = self.board_size[0] / num_boards
        self.length = self.board_size[0]

        print(self.board_size[0], self.new_size, self.length)

        # Vertical and Horizontal lines
        for i in range(int(num_boards)):
            pygame.draw.line(self.background, self.line_color, (self.new_size * (i + 1), 0), (self.new_size * (i + 1), self.length), self.line_weight)
            pygame.draw.line(self.background, self.line_color, (0, self.new_size * (i + 1)), (self.length, self.new_size * (i + 1)), self.line_weight)

    def __gen_boards(self):
        num_boards = math.sqrt(self.num_boards)
        num_cols = num_boards * 4
        num_rows = num_cols
        screen_length = int((num_cols + 1) * self.col_width)
        self.__init_board((screen_length, screen_length), num_boards)
        self.col_width = self.board_size[0] / num_cols
        startY = self.col_width / 2
        for i in range(int(num_rows) + 1):
            new_row = []
            startX = self.col_width / 2
            for j in range(int(num_rows) + 1):
                new_row.append(SmallBoard(self.ttt, startX, startY, self.col_width, self.background, self.line_color, self.XColor, self.OColor))
                startX += (self.col_width * 4)
            self.boards.append(new_row)
            startY += (self.col_width * 4)

    def __draw_board_outline(self, board_pos, line_color):
        start_x = self.boards[board_pos[0]][board_pos[1]].startX
        start_y = self.boards[board_pos[0]][board_pos[1]].startY
        part_col = self.col_width / 4
        pygame.draw.line(self.background, line_color, (start_x - part_col, start_y - part_col), (start_x + part_col + (self.col_width * 3), start_y - part_col), self.line_weight)
        pygame.draw.line(self.background, line_color, (start_x - part_col, start_y + part_col + (self.col_width * 3)), (start_x + part_col + (self.col_width * 3), start_y + part_col + (self.col_width * 3)), self.line_weight)
        pygame.draw.line(self.background, line_color, (start_x - part_col, start_y - part_col), (start_x - part_col, start_y + part_col + (self.col_width * 3)), self.line_weight)
        pygame.draw.line(self.background, line_color, (start_x + part_col + (self.col_width * 3), start_y - part_col), (start_x + part_col + (self.col_width * 3), start_y + part_col + (self.col_width * 3)), self.line_weight)

    def __within_tol(self, val, start, stop):
        # print("Start: %d < Val: %d < End: %d" % (start, val, stop))
        return start < val < stop

    def __play_board(self, board_pos):
        new_pos = self.boards[board_pos[0]][board_pos[1]].clickBoard()
        return new_pos

    def game_won(self):
        for condition in self.win_condition_pos:
            pos1 = condition[0]
            pos2 = condition[1]
            pos3 = condition[2]
            board = self.boards
            if board[pos1[0]][pos1[1]].won == board[pos2[0]][pos2[1]].won == board[pos3[0]][pos3[1]].won != False and \
               board[pos1[0]][pos1[1]].win_token == board[pos2[0]][pos2[1]].win_token == board[pos3[0]][pos3[1]].win_token:
                start_pos = board[pos1[0]][pos1[1]].return_center()
                end_pos = board[pos3[0]][pos3[1]].return_center()
                if board[pos1[0]][pos1[1]].win_token == 'O':
                    pygame.draw.line(self.background, self.OColor, (start_pos[0], start_pos[1]), (end_pos[0], end_pos[1]), self.line_weight)
                else:
                    pygame.draw.line(self.background, self.XColor, (start_pos[0], start_pos[1]), (end_pos[0], end_pos[1]), self.line_weight)
                self.won = True
                self.win_token = board[pos1[0]][pos1[1]].win_token
        return self.won

    def print_info(self):
        pass

    def play_game(self):
        self.__gen_boards()
        # main event loop
        board_pos = (1,1)
        last_board_pos = (1,1)
        self.__draw_board_outline(board_pos, self.XOColor)
        while (self.running == 1):
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    self.running = 0
                elif event.type is pygame.MOUSEBUTTONDOWN:
                    new_pos = pygame.mouse.get_pos()
                    # print("Board pos:", self.boards[board_pos[0]][board_pos[1]].self_pos)
                    # print("New pos:", new_pos)
                    if (self.__within_tol(new_pos[0], self.boards[board_pos[0]][board_pos[1]].startX, self.boards[board_pos[0]][board_pos[1]].startX + (self.col_width * 3))) and \
                       (self.__within_tol(new_pos[1], self.boards[board_pos[0]][board_pos[1]].startY, self.boards[board_pos[0]][board_pos[1]].startY + (self.col_width * 3))):
                        board_pos = self.boards[board_pos[0]][board_pos[1]].clickBoard(self.XO)
                        # Making sure the new board isn't just a double click
                        if board_pos is None:
                            board_pos = last_board_pos
                        else:
                            # toggle XO to the other player's move
                            if (self.XO == "X"):
                                self.XO = "O"
                                self.XOColor = self.OColor
                            else:
                                self.XO = "X"
                                self.XOColor = self.XColor

                        print("New pos: %s, Last pos: %s" % (board_pos, last_board_pos))
                        if len(last_board_pos) != 0:
                            self.__draw_board_outline(last_board_pos, self.bg_color)
                        self.__draw_board_outline(board_pos, self.XOColor)
                        last_board_pos = board_pos
                    # print("Next pos:", board_pos)

            for row in self.boards:
                for board in row:
                    board.gameWon()
                    # update the display
                    # TODO Add turn display and proper win/draw message
                    board.showBoard(self.ttt)
            self.game_won()
            # if self.won == True:
            #     self.running = 0

if __name__ == "__main__":
    big_board = TwoPlayerBoard(1, 50)
    big_board.play_game()