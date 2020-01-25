import re
import sys

GAME_BOARD = """
    A B C D E F G H
  +—————————————————+
1 | {} {} {} {} {} {} {} {} |
2 | {} {} {} {} {} {} {} {} |
3 | {} {} {} {} {} {} {} {} |
4 | {} {} {} {} {} {} {} {} |
5 | {} {} {} {} {} {} {} {} |
6 | {} {} {} {} {} {} {} {} |
7 | {} {} {} {} {} {} {} {} |
8 | {} {} {} {} {} {} {} {} |
  +—————————————————+
"""

ALPHA = ["A", "B", "C", "D", "E", "F", "G", "H"]

PLAYER_ONE = "Player One"
PLAYER_TWO = "Player Two"

BLACK = "x"
WHITE = "o"
BLACK_KINGED = "X"
WHITE_KINGED = "O"

WHITE_START_POSITIONS = [
    (0, 1), (0, 3), (0, 5), (0, 7),
    (1, 0), (1, 2), (1, 4), (1, 6),
    (2, 1), (2, 3), (2, 5), (2, 7)
]

BLACK_START_POSITIONS = [
    (5, 0), (5, 2), (5, 4), (5, 6),
    (6, 1), (6, 3), (6, 5), (6, 7),
    (7, 0), (7, 2), (7, 4), (7, 6),
]


def display_board(board):
    current_board = [board[(x, y)] for x in range(8) for y in range(8)]
    print(GAME_BOARD.format(*current_board))


def setup_board(board):
    for position in WHITE_START_POSITIONS:
        board[position] = WHITE
    for position in BLACK_START_POSITIONS:
        board[position] = BLACK


def find_available_moves(board, player):
    pass


def player_move_prompt(player):
    user_input = None
    while user_input is None \
            or not is_valid_coordinate(user_input) \
            or not is_black_square(*get_move_coordinates(user_input)):
        user_input = input("{} enter your move: ".format(player))


def clean_input(string):
    return string.strip().upper()


def is_valid_coordinate(move):
    return re.match(r"^[0-9][a-hA-H]$", move)


def get_move_coordinates(move):
    return int(move[0]) - 1, alpha_to_coordinate(move[1])


def alpha_to_coordinate(char):
    return ALPHA.index(char)


def is_black_square(x, y):
    return (x + y) % 2 != 0


def switch_players(current_player):
    return PLAYER_ONE if current_player == PLAYER_TWO else PLAYER_TWO


def main():
    current_player = PLAYER_ONE
    board = {(x, y): get_board_square(x, y) for x in range(8) for y in range(8)}
    setup_board(board)
    while True:
        display_board(board)
        player_move_prompt(current_player)
        current_player = switch_players(current_player)


def get_board_square(x, y):
    return "■" if is_black_square(x, y) else "□"


if __name__ == '__main__':
    main()
