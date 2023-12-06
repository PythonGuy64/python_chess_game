import abc


class Game:
    INT_SPACE_BETWEEN_2_BOARDS = 45

    def __init__(self):
        self.list_board = [["  "] * 8 for _ in range(8)]
        self.list_squares_under_attack = [[False] * 8 for _ in range(8)]
        self.list_pieces = []
        self.str_current_color = "w"
        self.bool_check = None
        self.list_en_passant = Pawn.list_en_passant
        self.index_first_white_piece = 16
        self.ally_range = range(-1, -self.index_first_white_piece - 1, -1)
        self.enemy_range = range(self.index_first_white_piece)

        self.list_board[0][0] = Rook([0, 0], "b")
        self.list_board[0][1] = Knight([0, 1], "b")
        self.list_board[0][2] = Bishop([0, 2], "b")
        self.list_board[0][3] = Queen([0, 3], "b")
        self.list_board[0][4] = King([0, 4], "b")
        self.list_board[0][5] = Bishop([0, 5], "b")
        self.list_board[0][6] = Knight([0, 6], "b")
        self.list_board[0][7] = Rook([0, 7], "b")

        self.list_board[7][0] = Rook([7, 0], "w")
        self.list_board[7][1] = Knight([7, 1], "w")
        self.list_board[7][2] = Bishop([7, 2], "w")
        self.list_board[7][3] = Queen([7, 3], "w")
        self.list_board[7][4] = King([7, 4], "w")
        self.list_board[7][5] = Bishop([7, 5], "w")
        self.list_board[7][6] = Knight([7, 6], "w")
        self.list_board[7][7] = Rook([7, 7], "w")

        for x in range(8):
            self.list_board[1][x] = Pawn([1, x], "b")
            self.list_board[6][x] = Pawn([6, x], "w")

        for y in 0, 1, 6, 7:
            self.list_pieces.extend(self.list_board[y])

        self.obj_b_king = self.list_pieces[4]
        self.obj_w_king = self.list_pieces[28]

    def fn_display_board(self) -> None:
        print(f"\n  {'_' * 55}{' ' * (Game.INT_SPACE_BETWEEN_2_BOARDS + 2)}{'_' * 55}")

        for y in range(8):
            print(
                f" |{'      |' * 8}{' ' * Game.INT_SPACE_BETWEEN_2_BOARDS}|{'      |' * 8}"
                f"\n |  {self.list_board[y][0]}  |  {self.list_board[y][1]}  |  {self.list_board[y][2]}  |  "
                f"{self.list_board[y][3]}  |  {self.list_board[y][4]}  |  {self.list_board[y][5]}  |  "
                f"{self.list_board[y][6]}  |  {self.list_board[y][7]}  | {8 - y}{' ' * 41}{y + 1} |  "
                f"{self.list_board[7 - y][7]}  |  {self.list_board[7 - y][6]}  |  {self.list_board[7 - y][5]}  |  "
                f"{self.list_board[7 - y][4]}  |  {self.list_board[7 - y][3]}  |  {self.list_board[7 - y][2]}  |  "
                f"{self.list_board[7 - y][1]}  |  {self.list_board[7 - y][0]}  |"
                f"\n |{'______|' * 8}{' ' * Game.INT_SPACE_BETWEEN_2_BOARDS}|{'______|' * 8}"
            )

        print(
            f"    A      B      C      D      E      F      G      H{' ' * (Game.INT_SPACE_BETWEEN_2_BOARDS + 7)}"
            "H      G      F      E      D      C      B      A"
        )

    def fn_generate_valid_moves(self) -> None:
        self.bool_check = False
        list_checks = []
        list_potential_pinners = []

        if self.str_current_color == "w":
            obj_king = self.obj_w_king
        else:
            obj_king = self.obj_b_king

        for y in range(8):
            for x in range(8):
                self.list_squares_under_attack[y][x] = False

        for i in self.enemy_range:
            obj_piece = self.list_pieces[i]
            obj_piece.list_valid_moves.clear()
            obj_piece.fn_valid_moves(self.list_board, self.list_squares_under_attack, self.str_current_color)

            if len(list_checks) < 2 and obj_king.list_position in obj_piece.list_valid_moves:
                list_checks.append(obj_piece)
                self.bool_check = True
            elif (
                isinstance(obj_piece, (Rook, Queen)) and
                (obj_piece.int_y == obj_king.int_y or obj_piece.int_x == obj_king.int_x) or
                isinstance(obj_piece, (Bishop, Queen)) and
                abs(obj_piece.int_y - obj_king.int_y) == abs(obj_piece.int_x - obj_king.int_x)
            ):
                list_potential_pinners.append(obj_piece)

        if len(list_checks) < 2:
            for i in self.ally_range:
                obj_piece = self.list_pieces[i]
                obj_piece.list_valid_moves.clear()
                obj_piece.fn_valid_moves(self.list_board, self.list_squares_under_attack, self.str_current_color)
        else:
            obj_king.list_valid_moves.clear()
            obj_king.fn_valid_moves(self.list_board, self.list_squares_under_attack, self.str_current_color)

        if obj_king.bool_first_move and not self.bool_check:
            obj_rook = self.list_board[obj_king.int_y][0]

            if (
                isinstance(obj_rook, Rook) and obj_rook.bool_first_move and
                self.list_board[obj_king.int_y][1] == self.list_board[obj_king.int_y][2] ==
                self.list_board[obj_king.int_y][3] == "  " and not self.list_squares_under_attack[obj_king.int_y][2] and
                not self.list_squares_under_attack[obj_king.int_y][3]
            ):
                obj_king.list_valid_moves.append([obj_king.int_y, obj_king.int_x - 2])

            obj_rook = self.list_board[obj_king.int_y][7]

            if (
                isinstance(obj_rook, Rook) and obj_rook.bool_first_move and
                self.list_board[obj_king.int_y][5] == self.list_board[obj_king.int_y][6] == "  " and
                not self.list_squares_under_attack[obj_king.int_y][5] and
                not self.list_squares_under_attack[obj_king.int_y][6]
            ):
                obj_king.list_valid_moves.append([obj_king.int_y, obj_king.int_x + 2])

        for i in range(len(obj_king.list_valid_moves) - 1, -1, -1):
            list_destination = obj_king.list_valid_moves[i]

            if self.list_squares_under_attack[list_destination[0]][list_destination[1]]:
                del obj_king.list_valid_moves[i]

        if self.bool_check:
            for e in list_checks:
                if obj_king.list_valid_moves and not isinstance(e, (Knight, Pawn)):
                    tuple_directions = (
                        Game.fn_direction(obj_king.int_y - e.int_y), Game.fn_direction(obj_king.int_x - e.int_x)
                    )

                    for i in range(len(obj_king.list_valid_moves) - 1, -1, -1):
                        list_destination = obj_king.list_valid_moves[i]

                        if (
                            (list_destination[0] - obj_king.int_y, list_destination[1] - obj_king.int_x) ==
                                tuple_directions
                        ):
                            del obj_king.list_valid_moves[i]
                            break

            if len(list_checks) == 1:
                obj_dangerous_piece = list_checks[0]
                list_good_moves = []

                if not isinstance(obj_dangerous_piece, (Knight, Pawn)):
                    list_good_moves.extend(
                        Game.fn_between_2_points(obj_king.list_position, obj_dangerous_piece.list_position))

                list_good_moves.append(obj_dangerous_piece.list_position)

                for i in self.ally_range:
                    obj_piece = self.list_pieces[i]

                    if not isinstance(obj_piece, King):
                        for i in range(len(obj_piece.list_valid_moves) -1, -1, -1):
                            if obj_piece.list_valid_moves[i] not in list_good_moves:
                                del obj_piece.list_valid_moves[i]

        if list_potential_pinners:
            for e in list_potential_pinners:
                list_good_moves = Game.fn_between_2_points(e.list_position, obj_king.list_position)
                list_encountered_pieces = []

                for e2 in list_good_moves:
                    obj_piece = self.list_board[e2[0]][e2[1]]

                    if obj_piece != "  ":
                        list_encountered_pieces.append(obj_piece)

                if len(list_encountered_pieces) == 1:
                    obj_piece = list_encountered_pieces[0]

                    if obj_piece.str_color == self.str_current_color:
                        if isinstance(obj_piece, Knight):
                            obj_piece.list_valid_moves.clear()
                        else:
                            list_good_moves.append(e.list_position)

                            for i in range(len(obj_piece.list_valid_moves) -1, -1, -1):
                                if obj_piece.list_valid_moves[i] not in list_good_moves:
                                    del obj_piece.list_valid_moves[i]
                elif len(list_encountered_pieces) == 2 and e.int_y == obj_king.int_y and self.list_en_passant:
                    obj_piece = None

                    for e2 in list_encountered_pieces:
                        if isinstance(e2, Pawn):
                            if e2.str_color == self.str_current_color:
                                obj_piece = e2
                        else:
                            return

                    if obj_piece:
                        for i in range(len(obj_piece.list_valid_moves)):
                            int_y2, int_x2 = obj_piece.list_valid_moves[i]

                            if int_x2 != obj_piece.int_x and self.list_board[int_y2][int_x2] == "  ":
                                del obj_piece.list_valid_moves[i]
                                break

    def fn_game_over(self) -> bool:
        for i in self.ally_range:
            if self.list_pieces[i].list_valid_moves:
                return False

        return True

    def fn_execute_move(self, p_piece, p_destination: list) -> None:
        int_y2, int_x2 = p_destination

        if isinstance(p_piece, Pawn) and int_x2 != p_piece.int_x and self.list_board[int_y2][int_x2] == "  ":
            self.list_pieces.remove(self.list_board[p_piece.int_y][int_x2])
            self.list_board[p_piece.int_y][int_x2] = "  "

            if self.str_current_color == "w":
                self.index_first_white_piece -= 1
        elif isinstance(p_piece, King):
            int_vx = int_x2 - p_piece.int_x

            if abs(int_vx) == 2:
                if int_vx == 2:
                    obj_rook = self.list_board[p_piece.int_y][7]
                else:
                    obj_rook = self.list_board[p_piece.int_y][0]

                self.list_board[p_piece.int_y][obj_rook.int_x] = "  "
                obj_rook.list_position[1] = obj_rook.int_x = p_piece.int_x + int_vx // 2
                self.list_board[p_piece.int_y][obj_rook.int_x] = obj_rook

        obj_piece = self.list_board[int_y2][int_x2]

        if obj_piece != "  ":
            if obj_piece.str_color == "b":
                self.index_first_white_piece -= 1

            self.list_pieces.remove(obj_piece)

        self.list_board[p_piece.int_y][p_piece.int_x] = "  "
        self.list_board[int_y2][int_x2] = p_piece
        p_piece.list_position = p_piece.int_y, p_piece.int_x = p_destination

    @staticmethod
    def fn_between_2_points(p_position: list, p_destination: list) -> list:
        list_between = []
        int_y, int_x = p_position
        int_y2, int_x2 = p_destination
        int_dy = Game.fn_direction(int_y2 - int_y)
        int_dx = Game.fn_direction(int_x2 - int_x)

        while True:
            int_y += int_dy
            int_x += int_dx

            if int_y == int_y2 and int_x == int_x2:
                break

            list_between.append([int_y, int_x])

        return list_between

    @staticmethod
    def fn_direction(p_vector: int) -> int:
        if p_vector > 0:
            return 1
        elif p_vector < 0:
            return -1

        return 0


class Piece(abc.ABC):
    def __init__(self, p_position: list, p_color: str):
        self.list_position = self.int_y, self.int_x = p_position
        self.str_color = p_color
        self.list_valid_moves = []

        if isinstance(self, (Pawn, Rook, King)):
            self.bool_first_move = True

    @abc.abstractmethod
    def fn_valid_moves(self, p_board: list, p_squares_under_attack: list, p_current_color: str) -> None:
        if isinstance(self, (Rook, Bishop, Queen)):
            for d in type(self).tuple_directions:
                for cycle in range(1, 8):
                    int_y2 = self.int_y + d[0] * cycle
                    int_x2 = self.int_x + d[1] * cycle

                    if not (-1 < int_y2 < 8 and -1 < int_x2 < 8):
                        break

                    if self.str_color != p_current_color:
                        p_squares_under_attack[int_y2][int_x2] = True

                    obj_piece = p_board[int_y2][int_x2]
                    list_destination = [int_y2, int_x2]

                    if obj_piece == "  ":
                        self.list_valid_moves.append(list_destination)
                    elif self.str_color == obj_piece.str_color:
                        break
                    else:
                        self.list_valid_moves.append(list_destination)
                        break
        elif isinstance(self, (Knight, King)):
            for v in type(self).tuple_vectors:
                int_y2 = self.int_y + v[0]
                int_x2 = self.int_x + v[1]

                if -1 < int_y2 < 8 and -1 < int_x2 < 8:
                    if self.str_color != p_current_color:
                        p_squares_under_attack[int_y2][int_x2] = True

                    if self.str_color != str(p_board[int_y2][int_x2])[0]:
                        self.list_valid_moves.append([int_y2, int_x2])


class Pawn(Piece):
    list_en_passant = []

    def __init__(self, p_position: list, p_couleur: str):
        super().__init__(p_position, p_couleur)
        self.int_d = -1 if self.str_color == "w" else 1 # Direction

    def __str__(self):
        return f"{self.str_color}P"

    def fn_valid_moves(self, p_board: list, p_squares_under_attack: list, p_current_color: str) -> None:
        int_y2 = self.int_y + self.int_d

        for vx in -1, 1:
            int_x2 = self.int_x + vx

            if -1 < int_x2 < 8:
                if self.str_color != p_current_color:
                    p_squares_under_attack[int_y2][int_x2] = True

                obj_piece = p_board[int_y2][int_x2]
                list_destination = [int_y2, int_x2]

                if obj_piece != "  ":
                    if self.str_color != obj_piece.str_color:
                        self.list_valid_moves.append(list_destination)
                elif [self.int_y, int_x2] == Pawn.list_en_passant:
                    self.list_valid_moves.append(list_destination)

        if p_board[int_y2][self.int_x] == "  ":
            self.list_valid_moves.append([int_y2, self.int_x])
            int_y2 += self.int_d

            if self.bool_first_move and p_board[int_y2][self.int_x] == "  ":
                self.list_valid_moves.append([int_y2, self.int_x])


class Rook(Piece):
    tuple_directions = ((-1, 0), (0, -1), (0, 1), (1, 0))

    def __str__(self):
        return f"{self.str_color}R"

    def fn_valid_moves(self, p_board: list, p_squares_under_attack: list, p_current_color: str) -> None:
        super().fn_valid_moves(p_board, p_squares_under_attack, p_current_color)


class Knight(Piece):
    tuple_vectors = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))

    def __str__(self):
        return f"{self.str_color}N"

    def fn_valid_moves(self, p_board: list, p_squares_under_attack: list, p_current_color: str) -> None:
        super().fn_valid_moves(p_board, p_squares_under_attack, p_current_color)


class Bishop(Piece):
    tuple_directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))

    def __str__(self):
        return f"{self.str_color}B"

    def fn_valid_moves(self, p_board: list, p_squares_under_attack: list, p_current_color: str) -> None:
        super().fn_valid_moves(p_board, p_squares_under_attack, p_current_color)


class Queen(Piece):
    tuple_directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

    def __str__(self):
        return f"{self.str_color}Q"

    def fn_valid_moves(self, p_board: list, p_squares_under_attack: list, p_current_color: str) -> None:
        super().fn_valid_moves(p_board, p_squares_under_attack, p_current_color)


class King(Piece):
    tuple_vectors = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

    def __str__(self):
        return f"{self.str_color}K"

    def fn_valid_moves(self, p_board: list, p_squares_under_attack: list, p_current_color: str) -> None:
        super().fn_valid_moves(p_board, p_squares_under_attack, p_current_color)
