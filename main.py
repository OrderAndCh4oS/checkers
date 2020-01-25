import re

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

BLACK_SQUARE = "■"
WHITE_SQUARE = "."

BLACK = "x"
WHITE = "o"
BLACK_KINGED = "X"
WHITE_KINGED = "O"

WHITE_PIECES = (WHITE, WHITE_KINGED)
BLACK_PIECES = (BLACK, BLACK_KINGED)

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


def is_legal_move(board, player, piece_coordinate, move_coordinate):
    if player is PLAYER_ONE:
        return move_coordinate in allowed_piece_moves(board, player, piece_coordinate, ((-1, -1), (-1, 1)))
    elif player is PLAYER_TWO:
        return move_coordinate in allowed_piece_moves(board, player, piece_coordinate, ((1, 1), (1, -1)))


def is_white_piece(board, coordinate):
    return board[coordinate] in WHITE_PIECES


def is_black_piece(board, coordinate):
    return board[coordinate] in BLACK_PIECES


def is_in_board_bounds(x, y):
    return 0 <= x <= 7 and 0 <= y <= 7


def allowed_piece_moves(board, player, piece_coordinate, possible_move_coordinates):
    x, y = piece_coordinate
    allowed_moves = []
    for move_coordinate in possible_move_coordinates:
        move = (x + move_coordinate[0], y + move_coordinate[1])
        if not is_in_board_bounds(*move):
            continue
        if player is PLAYER_ONE:
            if is_white_piece(board, move):
                move = (move[0] + move_coordinate[0], move[1] + move_coordinate[1])
                if not is_in_board_bounds(*move) or not is_black_square(*move):
                    continue
            elif is_black_piece(board, move):
                continue
        elif player is PLAYER_TWO:
            if is_black_piece(board, move):
                move = (move[0] + move_coordinate[0], move[1] + move_coordinate[1])
                if not is_in_board_bounds(*move) or not is_black_square(*move):
                    continue
                pass
            elif is_white_piece(board, move):
                continue
        if board[move] == BLACK_SQUARE:
            allowed_moves.append(move)
            continue

    return allowed_moves


def make_move(board, piece_coordinate, move_coordinate):
    board[move_coordinate], board[piece_coordinate] = board[piece_coordinate], board[move_coordinate]


def is_current_player_piece(board, player, coordinate):
    if player is PLAYER_ONE:
        return board[coordinate] in BLACK_PIECES
    elif player is PLAYER_TWO:
        return board[coordinate] in WHITE_PIECES


def select_piece(board, player):
    user_input = None
    while user_input is None \
            or not is_valid_coordinate(user_input) \
            or not is_black_square(*get_move_coordinates(user_input)) \
            or not is_current_player_piece(board, player, get_move_coordinates(user_input)):
        user_input = input("{} select piece to move: ".format(player))

    return get_move_coordinates(user_input)


def enter_move(board, player, piece):
    user_input = None
    while user_input is None or \
            not is_legal_move(board, player, piece, get_move_coordinates(user_input)):
        user_input = input("{} enter your move: ".format(player))

    return get_move_coordinates(user_input)


def clean_input(string):
    return string.strip().upper()


def is_valid_coordinate(move):
    return re.match(r"^[0-9][a-hA-H]$", move)


def get_move_coordinates(move):
    return int(move[0]) - 1, alpha_to_coordinate(move[1])


def alpha_to_coordinate(char):
    return ALPHA.index(char.upper())


def is_black_square(x, y):
    return (x + y) % 2 != 0


def switch_players(current_player):
    if current_player == PLAYER_ONE:
        return PLAYER_TWO
    elif current_player == PLAYER_TWO:
        return PLAYER_ONE


def main():
    current_player = PLAYER_ONE
    board = {(x, y): get_board_square(x, y) for x in range(8) for y in range(8)}
    setup_board(board)
    while True:
        display_board(board)
        piece_coordinate = select_piece(board, current_player)
        move_coordinate = enter_move(board, current_player, piece_coordinate)
        make_move(board, piece_coordinate, move_coordinate)
        if abs(piece_coordinate[0] - move_coordinate[0]) > 1:
            capture = (
                (piece_coordinate[0] + move_coordinate[0]) / 2,
                (piece_coordinate[1] + move_coordinate[1]) / 2,
            )
            print(piece_coordinate, capture, move_coordinate)
            board[capture] = BLACK_SQUARE
        else:
            current_player = switch_players(current_player)


def get_board_square(x, y):
    return BLACK_SQUARE if is_black_square(x, y) else WHITE_SQUARE


if __name__ == '__main__':
    main()
