import os
import chessClasses as C

clear_screen = "cls" if os.name == "nt" else "clear"
dict_coordinates = {
    "a8": [0, 0], "b8": [0, 1], "c8": [0, 2], "d8": [0, 3], "e8": [0, 4], "f8": [0, 5], "g8": [0, 6], "h8": [0, 7],
    "a7": [1, 0], "b7": [1, 1], "c7": [1, 2], "d7": [1, 3], "e7": [1, 4], "f7": [1, 5], "g7": [1, 6], "h7": [1, 7],
    "a6": [2, 0], "b6": [2, 1], "c6": [2, 2], "d6": [2, 3], "e6": [2, 4], "f6": [2, 5], "g6": [2, 6], "h6": [2, 7],
    "a5": [3, 0], "b5": [3, 1], "c5": [3, 2], "d5": [3, 3], "e5": [3, 4], "f5": [3, 5], "g5": [3, 6], "h5": [3, 7],
    "a4": [4, 0], "b4": [4, 1], "c4": [4, 2], "d4": [4, 3], "e4": [4, 4], "f4": [4, 5], "g4": [4, 6], "h4": [4, 7],
    "a3": [5, 0], "b3": [5, 1], "c3": [5, 2], "d3": [5, 3], "e3": [5, 4], "f3": [5, 5], "g3": [5, 6], "h3": [5, 7],
    "a2": [6, 0], "b2": [6, 1], "c2": [6, 2], "d2": [6, 3], "e2": [6, 4], "f2": [6, 5], "g2": [6, 6], "h2": [6, 7],
    "a1": [7, 0], "b1": [7, 1], "c1": [7, 2], "d1": [7, 3], "e1": [7, 4], "f1": [7, 5], "g1": [7, 6], "h1": [7, 7]
}
dict_promotion_pieces = {"r": C.Rook, "n": C.Knight, "b": C.Bishop, "q": C.Queen}
bool_playing = True
input("\n Make sure you put full screen (WinKey + Up) and press Enter: ")

while bool_playing:
    obj_game = C.Game()
    str_error = None
    int_number_of_spaces = 1
    obj_game.fn_generate_valid_moves()

    while True:
        os.system(clear_screen)
        obj_game.fn_display_board()

        if str_error:
            print(f"\n{' ' * int_number_of_spaces}{str_error}")

        if obj_game.bool_check:
            print(f"\n{' ' * int_number_of_spaces}Check!")

        # Position =====================================================================================================
        str_position = input(f"\n{' ' * int_number_of_spaces}Enter the position of the piece to move (a1-h8): ").lower()
        list_position = dict_coordinates.get(str_position)

        if not list_position:
            if str_position == "reset":
                break

            str_error = "Invalid input."
            continue

        int_y = list_position[0]
        obj_piece = obj_game.list_board[int_y][list_position[1]]

        if str(obj_piece)[0] != obj_game.str_current_color:
            str_error = "The position does not correspond to a piece of your color."
            continue

        if not obj_piece.list_valid_moves:
            str_error = "This piece has no possible move."
            continue

        # Destination ==================================================================================================
        print()

        for i in range(len(obj_piece.list_valid_moves)):
            for e in dict_coordinates:
                if dict_coordinates[e] == obj_piece.list_valid_moves[i]:
                    if not (i % 14):
                        print(f"{' ' * int_number_of_spaces}{e}", end="")
                    elif i == 13:
                        print(f", {e},")
                    else:
                        print(f", {e}", end="")

        print()

        str_destination = input(
            f"\n{' ' * int_number_of_spaces}Enter the destination of the piece to move (a1-h8): ").lower()
        list_destination = dict_coordinates.get(str_destination)

        if not list_destination:
            if str_destination == "reset":
                break

            str_error = "Invalid input."
            continue

        if list_destination not in obj_piece.list_valid_moves:
            str_error = "Invalid move."
            continue

        # Move execution ===============================================================================================
        obj_game.fn_execute_move(obj_piece, list_destination)
        str_error = None
        obj_game.list_en_passant.clear()

        if isinstance(obj_piece, C.Pawn):
            obj_piece.bool_first_move = False

            if abs(obj_piece.int_y - int_y) == 2:
                obj_game.list_en_passant.extend(list_destination)
            elif obj_piece.int_y in (0, 7):
                while True:
                    os.system(clear_screen)
                    obj_game.fn_display_board()

                    if str_error:
                        print(f"\n{' ' * int_number_of_spaces}{str_error}")

                    str_promotion = input(
                        f"\n{' ' * int_number_of_spaces}Enter the first letter of the piece you want"
                        f"\n{' ' * int_number_of_spaces}your pawn be promoted to (r/n/b/q): "
                    ).lower()
                    cls_promoted_piece = dict_promotion_pieces.get(str_promotion)

                    if not cls_promoted_piece:
                        str_error = "Invalid input"
                        continue

                    for i in obj_game.ally_range:
                        if obj_game.list_pieces[i] is obj_piece:
                            obj_game.list_board[obj_piece.int_y][obj_piece.int_x] = obj_game.list_pieces[i] = (
                                cls_promoted_piece(list_destination, obj_piece.str_color)
                            )
                            break

                    str_error = None
                    break
        elif isinstance(obj_piece, (C.Rook, C.King)):
            obj_piece.bool_first_move = False

        if obj_game.str_current_color == "w":
            obj_game.str_current_color = "b"
            int_number_of_spaces = obj_game.INT_SPACE_BETWEEN_2_BOARDS + 58
        else:
            obj_game.str_current_color = "w"
            int_number_of_spaces = 1

        obj_game.ally_range, obj_game.enemy_range = obj_game.enemy_range, obj_game.ally_range
        obj_game.fn_generate_valid_moves()

        # Game analysis ================================================================================================
        if obj_game.fn_game_over():
            os.system(clear_screen)
            obj_game.fn_display_board()

            if obj_game.bool_check:
                print(f"\n{' ' * int_number_of_spaces}Checkmate!")
            else:
                print(f"\n{' ' * 58}Stalemate!")

            if input(f"\n{' ' * 58}Do you want to continue? (y/n): ").lower() != "y":
                bool_playing = False

            break

os.system(clear_screen)
print("\n Goodbye!")
input(" Press Enter to exit: ")
