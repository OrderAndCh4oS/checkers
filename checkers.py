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

KINGED_MOVES = (-1, -1), (-1, 1), (1, 1), (1, -1)
BLACK_MOVES = (-1, -1), (-1, 1)
WHITE_MOVES = (1, 1), (1, -1)

WHITE_PIECES = (WHITE, WHITE_KINGED)
BLACK_PIECES = (BLACK, BLACK_KINGED)

WHITE_START_POSITIONS = [
    (0, 1),
    (0, 3),
    (0, 5),
    (0, 7),
    (1, 0),
    (1, 2),
    (1, 4),
    (1, 6),
    (2, 1),
    (2, 3),
    (2, 5),
    (2, 7),
]

BLACK_START_POSITIONS = [
    (5, 0),
    (5, 2),
    (5, 4),
    (5, 6),
    (6, 1),
    (6, 3),
    (6, 5),
    (6, 7),
    (7, 0),
    (7, 2),
    (7, 4),
    (7, 6),
]


def display_board(board):
    current_board = [board[(x, y)] for x in range(8) for y in range(8)]
    print(GAME_BOARD.format(*current_board))


def setup_board(board):
    for position in WHITE_START_POSITIONS:
        board[position] = WHITE
    for position in BLACK_START_POSITIONS:
        board[position] = BLACK


def get_piece_moves(player, piece):
    if piece in (WHITE_KINGED, BLACK_KINGED):
        return KINGED_MOVES
    elif player is PLAYER_ONE:
        return BLACK_MOVES
    elif player is PLAYER_TWO:
        return WHITE_MOVES


def is_legal_move(board, player, piece_coordinate, move_coordinate):
    possible_piece_moves = get_piece_moves(player, board[piece_coordinate])
    return move_coordinate in allowed_moves_for_piece(
        board, player, piece_coordinate, possible_piece_moves
    )


def is_white_piece(board, coordinate):
    return board[coordinate] in WHITE_PIECES


def is_black_piece(board, coordinate):
    return board[coordinate] in BLACK_PIECES


def is_in_board_bounds(x, y):
    return 0 <= x <= 7 and 0 <= y <= 7


def allowed_moves_for_piece(board, player, piece_coordinate, possible_move_coordinates):
    x, y = piece_coordinate
    allowed_moves = []
    for move_coordinate in possible_move_coordinates:
        move = (x + move_coordinate[0], y + move_coordinate[1])
        if not is_in_board_bounds(*move):
            continue
        if player is PLAYER_ONE:
            if is_white_piece(board, move):
                move = (move[0] + move_coordinate[0], move[1] + move_coordinate[1])
                if not is_in_board_bounds(*move) or board[move] != BLACK_SQUARE:
                    continue
            elif is_black_piece(board, move):
                continue
        elif player is PLAYER_TWO:
            if is_black_piece(board, move):
                move = (move[0] + move_coordinate[0], move[1] + move_coordinate[1])
                if not is_in_board_bounds(*move) or board[move] != BLACK_SQUARE:
                    continue
                pass
            elif is_white_piece(board, move):
                continue
        if board[move] == BLACK_SQUARE:
            allowed_moves.append(move)
            continue

    return allowed_moves


def get_capturing_moves_for_piece(
    board, player, piece_coordinate, possible_move_coordinates
):
    x, y = piece_coordinate
    capturing_moves = []
    for move_coordinate in possible_move_coordinates:
        move = (x + move_coordinate[0] * 2, y + move_coordinate[1] * 2)
        if not is_in_board_bounds(*move):
            continue
        if board[move] != BLACK_SQUARE:
            continue
        capture_coordinates = get_capture_coordinates(move, piece_coordinate)
        if player is PLAYER_ONE and can_capture_piece(
            board, capture_coordinates, WHITE_PIECES
        ):
            capturing_moves.append(move)
        elif player is PLAYER_TWO and can_capture_piece(
            board, capture_coordinates, BLACK_PIECES
        ):
            capturing_moves.append(move)

    return capturing_moves


def make_move(board, piece_coordinate, move_coordinate):
    board[move_coordinate], board[piece_coordinate] = (
        board[piece_coordinate],
        board[move_coordinate],
    )


def is_current_player_piece(board, player, coordinate):
    if player is PLAYER_ONE:
        return board[coordinate] in BLACK_PIECES
    elif player is PLAYER_TWO:
        return board[coordinate] in WHITE_PIECES


def select_piece(board, player):
    user_input = None
    while (
        user_input is None
        or not is_valid_coordinate(user_input)
        or not is_black_square(*get_move_coordinates(user_input))
        or not is_current_player_piece(board, player, get_move_coordinates(user_input))
    ):
        user_input = clean_input(input("{} select piece to move: ".format(player)))

    return get_move_coordinates(user_input)


def enter_move(board, player, piece):
    user_input = None
    while (
        user_input is None
        or not is_valid_coordinate(user_input)
        or not is_legal_move(board, player, piece, get_move_coordinates(user_input))
    ):
        user_input = clean_input(input("{} enter your move: ".format(player)))

    return get_move_coordinates(user_input)


def clean_input(string):
    return string.strip().upper()


def is_valid_coordinate(move):
    return re.match(r"^[0-9][a-hA-H]$", move) is not None


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


def can_capture_piece(board, capture_coordinates, opponents_pieces):
    return board[capture_coordinates] in opponents_pieces


def get_capture_coordinates(move_coordinate, piece_coordinate):
    return (
        (piece_coordinate[0] + move_coordinate[0]) / 2,
        (piece_coordinate[1] + move_coordinate[1]) / 2,
    )


def has_captured_piece(move_coordinate, piece_coordinate):
    if abs(piece_coordinate[0] - move_coordinate[0]) == 1:
        return False
    return True


def capture_piece(board, piece_coordinate, move_coordinate):
    capture = get_capture_coordinates(move_coordinate, piece_coordinate)
    board[capture] = BLACK_SQUARE


def get_board_square(x, y):
    return BLACK_SQUARE if is_black_square(x, y) else WHITE_SQUARE


def choose_follow_up_move(capturing_moves):
    if not len(capturing_moves):
        return None

    # Todo: handle forced capturing moves
    #   Allow choice if multiple pieces can be captured
    allowed_follow_ups = [coordinates_to_string(*move) for move in capturing_moves]
    print(", ".join(allowed_follow_ups))
    user_input = None
    while (
        user_input is None
        or not is_valid_coordinate(user_input)
        or user_input not in allowed_follow_ups
    ):
        user_input = clean_input(input("Select a follow up capture: "))

    return capturing_moves[allowed_follow_ups.index(user_input)]


def coordinates_to_string(x, y):
    return str(x + 1) + ALPHA[y]


def main():
    current_player = PLAYER_ONE
    board = {(x, y): get_board_square(x, y) for x in range(8) for y in range(8)}
    setup_board(board)
    while True:
        moved_to_coordinate, piece_coordinate = initial_player_move(
            board, current_player
        )
        moved_to_coordinate, piece_coordinate = follow_up_player_move(
            board, current_player, moved_to_coordinate, piece_coordinate
        )
        make_kinged_piece(board, current_player, moved_to_coordinate, piece_coordinate)
        black_piece_count, white_piece_count = count_pieces(board)

        if white_piece_count is 0:
            print("Player one wins")
            break

        if black_piece_count is 0:
            print("Player two wins")
            break

        current_player = switch_players(current_player)


def count_pieces(board):
    white_piece_count = 0
    black_piece_count = 0
    for coordinate in board:
        if board[coordinate] in BLACK_PIECES:
            black_piece_count += 1
        elif board[coordinate] in WHITE_PIECES:
            white_piece_count += 1
    return black_piece_count, white_piece_count


def make_kinged_piece(board, current_player, moved_to_coordinate, piece_coordinate):
    if moved_to_coordinate is None:
        moved_to_coordinate = piece_coordinate
    if current_player is PLAYER_ONE and moved_to_coordinate[0] is 0:
        board[moved_to_coordinate] = BLACK_KINGED
    elif current_player is PLAYER_TWO and moved_to_coordinate[0] is 7:
        board[moved_to_coordinate] = WHITE_KINGED


def follow_up_player_move(board, current_player, moved_to_coordinate, piece_coordinate):
    while moved_to_coordinate is not None and has_captured_piece(
        moved_to_coordinate, piece_coordinate
    ):
        capture_piece(board, piece_coordinate, moved_to_coordinate)
        possible_move_coordinates = get_piece_moves(
            current_player, board[moved_to_coordinate]
        )
        capturing_moves = get_capturing_moves_for_piece(
            board, current_player, moved_to_coordinate, possible_move_coordinates
        )
        follow_up_coordinate = choose_follow_up_move(capturing_moves)
        if follow_up_coordinate is not None:
            make_move(board, moved_to_coordinate, follow_up_coordinate)
            capture_piece(board, moved_to_coordinate, follow_up_coordinate)
        piece_coordinate = moved_to_coordinate
        moved_to_coordinate = follow_up_coordinate
    return moved_to_coordinate, piece_coordinate


def initial_player_move(board, current_player):
    display_board(board)
    piece_coordinate = select_piece(board, current_player)
    moved_to_coordinate = enter_move(board, current_player, piece_coordinate)
    make_move(board, piece_coordinate, moved_to_coordinate)
    return moved_to_coordinate, piece_coordinate


if __name__ == "__main__":
    main()
