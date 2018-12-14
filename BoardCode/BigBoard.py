class Board:
    def __init__(self):
        self.board_contents = [['x',' ',' '],[' ','x',' '],[' ','x',' ']]
        self.won = False

    def __is_played(self, move_pos):
        # Pass in a list for the pos
        return (self.board_contents[move_pos[0]][move_pos[1]] != ' ')

    def display_row(self, row):
        pos = 0
        print(" ", end='')
        for col in row:
            print(col, end='')
            if pos != 2:
                print(' │ ', end='')
            pos += 1
    
    def display_board(self):
        row_num = 0
        for row in self.board_contents:
            self.display_row(row)
            if row_num != 2:
                print("\n───┼───┼───", end='')
            row_num += 1
            print()

class BigBoard(Board):
    def __init__(self):
        Board.__init__(self)
        self.board_contents = [[Board(), Board(), Board()], [Board(), Board(), Board()], [Board(), Board(), Board()]]

    def display_board(self):
        print('╔═══════════╦═══════════╦═══════════╗')
        # To get inside each list of Board objects
        row_num = 0
        for row in self.board_contents:
            # To access each individual Board object in the row
            col_num = 0
            for col in row:
                pos = 0
                # To access each row inside the Board object's board_contents list
                for sub_row in col.board_contents:
                    print('║', end='')
                    super().display_row(sub_row)
                    if pos != 2:
                        print(' ', end='')
                    elif pos == 2:
                        if col_num != 2:
                            print(' ║', end='')
                            print('\n║───┼───┼───║───┼───┼───║───┼───┼───║', end='')
                        else:
                            print(' ║', end='')
                    pos += 1
                col_num += 1
                print()
            if row_num != 2:
                print('╠═══════════╬═══════════╬═══════════╣')
            row_num += 1
        print('╚═══════════╩═══════════╩═══════════╝')

little_test = Board()
# little_test.display_board()

test = BigBoard()
test.display_board()
