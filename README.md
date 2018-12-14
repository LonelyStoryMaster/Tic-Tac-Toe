# Tic-Tac-Toe
Final Project for Introduction to Programming class

## THE GAME

### RUNNING IT:

In order to run, pygame must be installed on the computer.
Plese refer to the [Pygame Wiki](https://www.pygame.org/wiki/GettingStarted) for instructions.

Then all you need to do is double click on the **DefaultBoard.py** file as of now

### RULES:

X is Red
O is Blue

Game starts on the center board of the grid.
X Goes first. The next player plays on the board corresponding
to that square. The next board that is to be played will be highlighted in your color.

### HOW TO WIN:

To win this game, you need to get three tic-tac-toes in a row.
Doesn't need to be the same column or row, just three boards where you've won in a row.





## ABOUT:

### Class:
- Intro to Programming, On ground class

### What I used in this program:
- Two Custom classes:
	- TwoPlayerGame
	- SmallBoard
- Matrices
- Modules
	- math
	- pygame
- GUI
	- pygame

### Things I intend to add:
- Save/Load feature
- Multiple rule sets
	- Square played is next board
	- Square played points to next board
- Computer opponent
	- Use of random module for move selection
- Menu
	- GUI

### Personal Thoughts:
- Likes:
	- I like how the tile-able board sizing worked out. Don't have the rules worked out to play with a 4x4 or bigger yet but the square pointing to the board would work for this
	- I enjoyed developing it with text-based first
- Dislikes:
	- Finding a GUI that worked for me took a little bit and each one seems to be missing some things that others have.
		- Tkinter has buttons and such but limited drawing and mouse ability
		- Pygame has great drawing and mouse ability but not built-in buttons
	- Troubleshooting
		- I forgot one of the win conditions and couldn't figure out which one because it's just a series of coordinates in a list
		- Getting the mouse to click on the right small board
