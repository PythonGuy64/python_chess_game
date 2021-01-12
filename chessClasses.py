import abc


class Game:
    def __init__(self):
        self.list_board = [["  "] * 8 for _ in range(8)]
        self.list_bit_board = [[False] * 8 for _ in range(8)]
        self.list_pieces = []
        self.str_current_color = "w"
        self.bool_check = None
        self.list_en_passant = Pawn.list_en_passant

        for y, c in zip((0, 7, 1, 6), ("b", "w") * 2):
            for x in range(8):
                if y in (0, 7):
                    if x in (1, 6):
                        self.list_board[y][x] = Knight([y, x], c)
                    elif x in (2, 5):
                        self.list_board[y][x] = Bishop([y, x], c)
                    elif x == 3:
                        self.list_board[y][x] = Queen([y, x], c)
                    elif x == 4:
                        self.list_board[y][x] = King([y, x], c)
                    else:
                        self.list_board[y][x] = Rook([y, x], c)
                else:
                    self.list_board[y][x] = Pawn([y, x], c)

        for y in 0, 1, 6, 7:
            self.list_pieces.extend(self.list_board[y])

        self.obj_b_king = self.list_pieces[4]
        self.obj_w_king = self.list_pieces[28]

    def fn_display_board(self) -> None:
        print(f"\n  {'_' * 55}{' ' * 47}{'_' * 55}")

        for y in range(8):
            print(f" |{'      |' * 8}{' ' * 45}|{'      |' * 8}"
                  f"\n |  {self.list_board[y][0]}  |  {self.list_board[y][1]}  |  {self.list_board[y][2]}  |  "
                  f"{self.list_board[y][3]}  |  {self.list_board[y][4]}  |  {self.list_board[y][5]}  |  "
                  f"{self.list_board[y][6]}  |  {self.list_board[y][7]}  | {8 - y}{' ' * 41}{y + 1} |  "
                  f"{self.list_board[7 - y][7]}  |  {self.list_board[7 - y][6]}  |  {self.list_board[7 - y][5]}  |  "
                  f"{self.list_board[7 - y][4]}  |  {self.list_board[7 - y][3]}  |  {self.list_board[7 - y][2]}  |  "
                  f"{self.list_board[7 - y][1]}  |  {self.list_board[7 - y][0]}  |"
                  f"\n |{'______|' * 8}{' ' * 45}|{'______|' * 8}")

        print(f"    A      B      C      D      E      F      G      H{' ' * 52}"
              "H      G      F      E      D      C      B      A")

    def fn_generate_valid_moves(self) -> None:
        self.bool_check = False
        list_dangerous_pieces = []
        list_potential_blocked_pieces = []

        if self.str_current_color == "w":
            obj_king = self.obj_w_king
        else:
            obj_king = self.obj_b_king

        for e in self.list_pieces:
            if e is obj_king:
                continue

            e.list_valid_moves = e.fn_valid_moves(self.list_board, self.list_bit_board, self.str_current_color)

            if e.str_color != self.str_current_color:
                while True:
                    if obj_king.list_position in e.list_valid_moves:
                        list_dangerous_pieces.append(e)
                        self.bool_check = True
                        break

                    if (
                        isinstance(e, (Rook, Queen)) and (e.int_y == obj_king.int_y or e.int_x == obj_king.int_x) or
                        isinstance(e, (Bishop, Queen)) and
                        abs(e.int_y - obj_king.int_y) == abs(e.int_x - obj_king.int_x)
                    ):
                        list_potential_blocked_pieces.append(e)

                    break

        obj_king.list_valid_moves = obj_king.fn_valid_moves(self.list_board, self.list_bit_board,
                                                            self.str_current_color)

        for e in obj_king.list_valid_moves[::-1]:
            if self.list_bit_board[e[0]][e[1]]:
                obj_king.list_valid_moves.remove(e)

        if self.bool_check:
            for e in list_dangerous_pieces:
                if obj_king.list_valid_moves and not isinstance(e, (Knight, Pawn)):
                    tuple_directions = \
                        Game.fn_direction(obj_king.int_y - e.int_y), Game.fn_direction(obj_king.int_x - e.int_x)

                    for e2 in obj_king.list_valid_moves[::-1]:
                        if (e2[0] - obj_king.int_y, e2[1] - obj_king.int_x) == tuple_directions:
                            obj_king.list_valid_moves.remove(e2)
                            break

            if len(list_dangerous_pieces) == 1:
                obj_dangerous_piece = list_dangerous_pieces[0]
                list_good_moves = []

                if not isinstance(obj_dangerous_piece, Knight):
                    list_good_moves.extend(
                        Game.fn_between_2_points(obj_king.list_position, obj_dangerous_piece.list_position))

                list_good_moves.append(obj_dangerous_piece.list_position)

                for e in self.list_pieces:
                    if e.str_color == self.str_current_color and not isinstance(e, King):
                        for e2 in e.list_valid_moves[::-1]:
                            if e2 not in list_good_moves:
                                e.list_valid_moves.remove(e2)
            else:
                for e in self.list_pieces:
                    if e.str_color == self.str_current_color and not isinstance(e, King):
                        e.list_valid_moves.clear()
        elif list_potential_blocked_pieces:
            for e in list_potential_blocked_pieces:
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

                            for e2 in obj_piece.list_valid_moves[::-1]:
                                if e2 not in list_good_moves:
                                    obj_piece.list_valid_moves.remove(e2)
                elif len(list_encountered_pieces) == 2 and e.int_y == obj_king.int_y and self.list_en_passant:
                    obj_piece = None

                    for e2 in list_encountered_pieces:
                        if isinstance(e2, Pawn) and e2.str_color == self.str_current_color:
                            obj_piece = e2
                            break

                    if obj_piece:
                        for e2 in obj_piece.list_valid_moves:
                            int_x2 = e2[1]

                            if int_x2 != obj_piece.int_x and self.list_board[e2[0]][int_x2] == "  ":
                                obj_piece.list_valid_moves.remove(e2)
                                break

    def fn_game_over(self) -> bool:
        for e in self.list_pieces:
            if e.str_color == self.str_current_color and e.list_valid_moves:
                return False

        return True

    def fn_execute_move(self, p_piece, p_destination: list) -> None:
        int_y2, int_x2 = p_destination

        if isinstance(p_piece, Pawn) and int_x2 != p_piece.int_x and self.list_board[int_y2][int_x2] == "  ":
            self.list_pieces.remove(self.list_board[p_piece.int_y][int_x2])
            self.list_board[p_piece.int_y][int_x2] = "  "
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
        int_y += int_dy
        int_x += int_dx

        while int_y != int_y2 or int_x != int_x2:
            list_between.append([int_y, int_x])
            int_y += int_dy
            int_x += int_dx

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
    def fn_valid_moves(self, p_board: list, p_bit_board: list, p_current_color: str) -> list:
        pass


class Pawn(Piece):
    list_en_passant = []

    def __init__(self, p_position: list, p_color: str):
        super().__init__(p_position, p_color)

        if self.str_color == "w":
            self.int_d = -1  # Direction
        else:
            self.int_d = 1

    def __str__(self):
        return f"{self.str_color}P"

    def fn_valid_moves(self, p_board: list, p_bit_board: list, p_current_color: str) -> list:
        list_valid_moves = []
        int_y2 = self.int_y + 1 * self.int_d

        for vx in -1, 1:
            int_x2 = self.int_x + vx

            if -1 < int_x2 < 8:
                if self.str_color != p_current_color:
                    p_bit_board[int_y2][int_x2] = True

                obj_piece = p_board[int_y2][int_x2]
                list_destination = [int_y2, int_x2]

                if obj_piece != "  ":
                    if self.str_color != obj_piece.str_color:
                        list_valid_moves.append(list_destination)
                elif [self.int_y, int_x2] == Pawn.list_en_passant:
                    list_valid_moves.append(list_destination)

        if p_board[int_y2][self.int_x] == "  ":
            list_valid_moves.append([int_y2, self.int_x])
            int_y2 += self.int_d

            if self.bool_first_move and p_board[int_y2][self.int_x] == "  ":
                list_valid_moves.append([int_y2, self.int_x])

        return list_valid_moves


class Rook(Piece):
    tuple_directions = ((-1, 0), (0, -1), (0, 1), (1, 0))

    def __str__(self):
        return f"{self.str_color}R"

    def fn_valid_moves(self, p_board: list, p_bit_board: list, p_current_color: str) -> list:
        list_valid_moves = []

        for d in Rook.tuple_directions:
            for cycle in range(1, 8):
                int_y2 = self.int_y + d[0] * cycle
                int_x2 = self.int_x + d[1] * cycle

                if not (-1 < int_y2 < 8 and -1 < int_x2 < 8):
                    break

                if self.str_color != p_current_color:
                    p_bit_board[int_y2][int_x2] = True

                obj_piece = p_board[int_y2][int_x2]
                list_destination = [int_y2, int_x2]

                if obj_piece == "  ":
                    list_valid_moves.append(list_destination)
                elif self.str_color != obj_piece.str_color:
                    list_valid_moves.append(list_destination)
                    break
                else:
                    break

        return list_valid_moves


class Knight(Piece):
    tuple_vectors = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))

    def __str__(self):
        return f"{self.str_color}N"

    def fn_valid_moves(self, p_board: list, p_bit_board: list, p_current_color: str) -> list:
        list_valid_moves = []

        for v in Knight.tuple_vectors:
            int_y2 = self.int_y + v[0]
            int_x2 = self.int_x + v[1]

            if -1 < int_y2 < 8 and -1 < int_x2 < 8:
                if self.str_color != p_current_color:
                    p_bit_board[int_y2][int_x2] = True

                if self.str_color != str(p_board[int_y2][int_x2])[0]:
                    list_valid_moves.append([int_y2, int_x2])

        return list_valid_moves


class Bishop(Piece):
    tuple_directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))

    def __str__(self):
        return f"{self.str_color}B"

    def fn_valid_moves(self, p_board: list, p_bit_board: list, p_current_color: str) -> list:
        list_valid_moves = []

        for d in Bishop.tuple_directions:
            for cycle in range(1, 8):
                int_y2 = self.int_y + d[0] * cycle
                int_x2 = self.int_x + d[1] * cycle

                if not (-1 < int_y2 < 8 and -1 < int_x2 < 8):
                    break

                if self.str_color != p_current_color:
                    p_bit_board[int_y2][int_x2] = True

                obj_piece = p_board[int_y2][int_x2]
                list_destination = [int_y2, int_x2]

                if obj_piece == "  ":
                    list_valid_moves.append(list_destination)
                elif self.str_color != obj_piece.str_color:
                    list_valid_moves.append(list_destination)
                    break
                else:
                    break

        return list_valid_moves


class Queen(Piece):
    def __str__(self):
        return f"{self.str_color}Q"

    def fn_valid_moves(self, p_board: list, p_bit_board: list, p_current_color: str) -> list:
        return (
            Rook(self.list_position, self.str_color).fn_valid_moves(p_board, p_bit_board, p_current_color) +
            Bishop(self.list_position, self.str_color).fn_valid_moves(p_board, p_bit_board, p_current_color)
        )


class King(Piece):
    tuple_vectors = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

    def __str__(self):
        return f"{self.str_color}K"

    def fn_valid_moves(self, p_board: list, p_bit_board: list, p_current_color: str) -> list:
        list_valid_moves = []

        for v in King.tuple_vectors:
            int_y2 = self.int_y + v[0]
            int_x2 = self.int_x + v[1]

            if -1 < int_y2 < 8 and -1 < int_x2 < 8:
                if self.str_color != p_current_color:
                    p_bit_board[int_y2][int_x2] = True

                if self.str_color != str(p_board[int_y2][int_x2])[0]:
                    list_valid_moves.append([int_y2, int_x2])

        if self.bool_first_move and not p_bit_board[self.int_y][self.int_x]:
            obj_rook = p_board[self.int_y][0]

            if (
                isinstance(obj_rook, Rook) and obj_rook.bool_first_move and
                p_board[self.int_y][1] == p_board[self.int_y][2] == p_board[self.int_y][3] == "  " and
                not p_bit_board[self.int_y][2] and not p_bit_board[self.int_y][3]
            ):
                list_valid_moves.append([self.int_y, self.int_x - 2])

            obj_rook = p_board[self.int_y][7]

            if (
                isinstance(obj_rook, Rook) and obj_rook.bool_first_move and
                p_board[self.int_y][5] == p_board[self.int_y][6] == "  " and
                not p_bit_board[self.int_y][5] and not p_bit_board[self.int_y][6]
            ):
                list_valid_moves.append([self.int_y, self.int_x + 2])

        return list_valid_moves
