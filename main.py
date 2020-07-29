'''
Game of Life
Martin A. Aaberge
'''

from board import Board
import pygame

clock = pygame.time.Clock()


def main():
    # assume the user types in a number
    user_rows = int(input('how many rows? '))
    user_columns = int(input('how many columns? '))
    user_TPS = int(input('how many ticks per second do you want to run at? '))

    # create a board:
    game_of_life_board = Board(user_rows, user_columns)

    # run the first iteration of the board:
    game_of_life_board.draw_board()

    game_going = True
    while game_going:
        game_of_life_board.update_board()
        game_of_life_board.draw_board()
        clock.tick(user_TPS)


main()
