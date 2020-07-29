'''
Game of Life
Board Class
Martin A. Aaberge
'''

from cell import Cell
from random import randint
from math import *
import sys
import pygame

screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)

class Board:
    def __init__(self, rows, columns):
        '''
        constructor holds input from user and populates the grid with cells. 
        initialises pygame
        '''
        pygame.init()
        self._rows = rows
        self._columns = columns
        self._grid = [[Cell() for column_cells in range(self._columns)] for row_cells in range(self._rows)]

        self._generate_board()

    def draw_board(self):
        '''
        method that draws the actual board in the terminal
        '''
        print('\n' * 10)
        print('printing board')
        screen.fill((0, 0, 0))
        box_size = floor(1920/self._columns)
        x_countdown = self._columns
        y_countdown = self._rows
        for event in pygame.event.get():

            # If X button is clicked
            if event.type == pygame.QUIT:
                print("Exiting Game")
                sys.exit()
        for row in self._grid:
            for column in row:
                if(column.get_print_character() == "."):
                    pass
                else:
                    pygame.draw.rect(screen, (255, 255, 255),
                                (((self._columns * box_size) - (x_countdown * box_size)), ((self._rows * box_size) - (y_countdown * box_size)), box_size, box_size))

                x_countdown -= 1
                print(column.get_print_character(), end='')
            x_countdown = self._columns
            y_countdown -= 1
            print()  # to create a new line pr. row.
        pygame.display.update()

    def _generate_board(self):
        '''
        method that sets the random state of all cells.
        '''
        mouse_down = []
        user_random = input('do you want it randomly generated? ')

        if user_random == 'yes':
            for row in self._grid:
                for column in row:
                    # there is a 33% chance the cells spawn alive.
                    chance_number = randint(0, 2)
                    if chance_number == 1:
                        column.set_alive()
        else:
            picking = True
            while picking:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            picking = False

                box_size = floor(1920 / self._columns)
                mouse_cord = []
                pre_mouse_down = mouse_down
                mouse_cord = pygame.mouse.get_pos()
                mouse_down = pygame.mouse.get_pressed()

                x_mouse = floor(mouse_cord[0] / box_size)
                y_mouse = floor(mouse_cord[1] / box_size)
                print("x: " + str(x_mouse) + " y: " + str(y_mouse) + " " + str(mouse_down))
                print(len(self._grid[0]))
                if mouse_down[0] == 1 and pre_mouse_down[0] == 0:
                    if x_mouse + 1 > self._columns or y_mouse + 1 > self._rows:
                        pass

                    else:
                        cell_object = self._grid[y_mouse][x_mouse]
                        status_cell = cell_object.is_alive()
                        if status_cell:
                            self._grid[y_mouse][x_mouse].set_dead()
                            pygame.draw.rect(screen, (0, 0, 0),
                                             ((x_mouse * box_size),
                                              (y_mouse * box_size), box_size, box_size))
                            pygame.display.update()
                        else:
                            self._grid[y_mouse][x_mouse].set_alive()
                            pygame.draw.rect(screen, (255, 255, 255),
                                             ((x_mouse * box_size),
                                              (y_mouse * box_size), box_size, box_size))
                            pygame.display.update()

    def update_board(self):
        '''
        method that updates the board based on
        the check of each cell pr. generation
        '''
        # cells list for living cells to kill and cells to resurrect or keep alive
        goes_alive = []
        gets_killed = []

        for row in range(len(self._grid)):
            for column in range(len(self._grid[row])):
                # check neighbour pr. square:
                check_neighbour = self.check_neighbour(row, column)

                living_neighbours_count = []

                for neighbour_cell in check_neighbour:
                    # check live status for neighbour_cell:
                    if neighbour_cell.is_alive():
                        living_neighbours_count.append(neighbour_cell)

                cell_object = self._grid[row][column]
                status_main_cell = cell_object.is_alive()

                # If the cell is alive, check the neighbour status.
                if status_main_cell == True:
                    if len(living_neighbours_count) < 2 or len(living_neighbours_count) > 3:
                        gets_killed.append(cell_object)

                    if len(living_neighbours_count) == 3 or len(living_neighbours_count) == 2:
                        goes_alive.append(cell_object)

                else:
                    if len(living_neighbours_count) == 3:
                        goes_alive.append(cell_object)

        # sett cell statuses
        for cell_items in goes_alive:
            cell_items.set_alive()

        for cell_items in gets_killed:
            cell_items.set_dead()

    def check_neighbour(self, check_row, check_column):
        '''
        method that checks all the neighbours for all the cells
        and returns the list of the valid neighbours so the update 
        method can set the new status
        '''
        # how deep the search is:
        search_min = -1
        search_max = 2

        # empty list to append neighbours into.
        neighbour_list = []
        for row in range(search_min, search_max):
            for column in range(search_min, search_max):
                neighbour_row = check_row + row
                neighbour_column = check_column + column

                valid_neighbour = True

                if (neighbour_row) == check_row and (neighbour_column) == check_column:
                    valid_neighbour = False

                if (neighbour_row) < 0 or (neighbour_row) >= self._rows:
                    valid_neighbour = False

                if (neighbour_column) < 0 or (neighbour_column) >= self._columns:
                    valid_neighbour = False

                if valid_neighbour:
                    neighbour_list.append(self._grid[neighbour_row][neighbour_column])
        return neighbour_list