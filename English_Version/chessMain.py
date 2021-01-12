import chessClasses as C
import os

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
bool_playing = True

while bool_playing:
    obj_game = C.Game()
    str_message = None
    input("\n Make sure you put full screen (WinKey + Up) and press Enter: ")
    obj_game.fn_generate_valid_moves()

    while True:
        os.system("cls")
        obj_game.fn_display_board()

        if str_message:
            if obj_game.str_current_color == "w":
                print(f"\n {str_message}")
            else:
                print(f"\n{' ' * 103}{str_message}")

        if obj_game.bool_check:
            if obj_game.str_current_color == "w":
                print("\n Check!")
            else:
                print(f"\n{' ' * 103}Check!")

        # Position =====================================================================================================
        if obj_game.str_current_color == "w":
            str_position = input("\n Enter the position of the piece to move (a1-h8): ").lower()
        elif obj_game.str_current_color == "b":
            str_position = input(f"\n{' ' * 103}Enter the position of the piece to move (a1-h8): ").lower()

        if str_position not in dict_coordinates:
            str_message = "Invalid input."
            continue

        list_position = dict_coordinates[str_position]
        int_y = list_position[0]
        obj_piece = obj_game.list_board[int_y][list_position[1]]

        if str(obj_piece)[0] != obj_game.str_current_color:
            str_message = "The position does not correspond to a piece of your color."
            continue

        if not obj_piece.list_valid_moves:
            str_message = "This piece has no possible move."
            continue

        # Destination ==================================================================================================
        print()

        if obj_game.str_current_color == "b":
            print(" " * 102, end="")

        for i in range(len(obj_piece.list_valid_moves)):
            for e in dict_coordinates:
                if dict_coordinates[e] == obj_piece.list_valid_moves[i]:
                    if i != len(obj_piece.list_valid_moves) - 1:
                        if i == 13:
                            print(f" {e},")

                            if obj_game.str_current_color == "b":
                                print(" " * 102, end="")
                        else:
                            print(f" {e},", end="")
                    else:
                        print(f" {e}")

        if obj_game.str_current_color == "w":
            str_destination = input("\n Enter the destination of the piece to move (a1-h8): ").lower()
        elif obj_game.str_current_color == "b":
            str_destination = input(f"\n{' ' * 103}Enter the destination of the piece to move (a1-h8): ").lower()

        if str_destination not in dict_coordinates:
            str_message = "Invalid input."
            continue

        list_destination = dict_coordinates[str_destination]

        if list_destination not in obj_piece.list_valid_moves:
            str_message = "Invalid move."
            continue

        # Move execution ===============================================================================================
        obj_game.fn_execute_move(obj_piece, list_destination)
        str_message = None
        obj_game.list_en_passant.clear()

        if isinstance(obj_piece, C.Pawn):
            obj_piece.bool_first_move = False

            if abs(obj_piece.int_y - int_y) == 2:
                obj_game.list_en_passant.extend(list_destination)
            elif obj_piece.int_y in (0, 7):
                os.system("cls")
                obj_game.fn_display_board()

                while True:
                    if obj_game.str_current_color == "w":
                        str_promotion = input("\n Enter the first letter of the piece you want"
                                              "\n your pawn to transform into (r/n/b/q): ").lower()
                    else:
                        print(f"\n{' ' * 103}Enter the first letter of the piece you want"
                              f"\n{' ' * 103}", end="")
                        str_promotion = input("your pawn to transform into (r/n/b/q): ").lower()

                    if str_promotion == "r":
                        obj_promoted_piece = C.Rook(list_destination, obj_game.str_current_color)
                    elif str_promotion == "n":
                        obj_promoted_piece = C.Knight(list_destination, obj_game.str_current_color)
                    elif str_promotion == "b":
                        obj_promoted_piece = C.Bishop(list_destination, obj_game.str_current_color)
                    elif str_promotion == "q":
                        obj_promoted_piece = C.Queen(list_destination, obj_game.str_current_color)
                    else:
                        os.system("cls")
                        obj_game.fn_display_board()

                        if obj_game.str_current_color == "w":
                            print("\n Invalid input.")
                        else:
                            print(f"\n{' ' * 103}Invalid input.")

                        continue

                    obj_game.list_board[obj_piece.int_y][obj_piece.int_x] = obj_promoted_piece
                    obj_game.list_pieces[obj_game.list_pieces.index(obj_piece)] = obj_promoted_piece
                    break
        elif isinstance(obj_piece, (C.Rook, C.King)):
            obj_piece.bool_first_move = False

        if obj_game.str_current_color == "w":
            obj_game.str_current_color = "b"
        else:
            obj_game.str_current_color = "w"

        for y in range(8):
            for x in range(8):
                obj_game.list_bit_board[y][x] = False

        obj_game.fn_generate_valid_moves()

        # Game analysis ================================================================================================
        if obj_game.fn_game_over():
            os.system("cls")
            obj_game.fn_display_board()

            if obj_game.bool_check:
                if obj_game.str_current_color == "w":
                    print("\n Checkmate!")
                else:
                    print(f"\n{' ' * 103}Checkmate!")
            else:
                print(f"\n{' ' * 58}Stalemate!")

            if input(f"\n{' ' * 58}Do you want to continue? (y/n): ").lower() == "y":
                os.system("cls")
            else:
                bool_playing = False

            break

os.system("cls")
print("\n Goodbye!", end="\n ")
os.system("pause")
