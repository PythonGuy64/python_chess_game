import abc


class Game:
    def __init__(self):
        self.list_tab = [["  "] * 8 for _ in range(8)]
        self.list_tab_danger = [[False] * 8 for _ in range(8)]
        self.list_pieces = []
        self.str_couleur_actuelle = "b"
        self.bool_echec = None
        self.list_en_passant = Pion.list_en_passant

        for y, c in zip((0, 7, 1, 6), ("n", "b") * 2):
            for x in range(8):
                if y in (0, 7):
                    if x in (1, 6):
                        self.list_tab[y][x] = Chevalier([y, x], c)
                    elif x in (2, 5):
                        self.list_tab[y][x] = Fou([y, x], c)
                    elif x == 3:
                        self.list_tab[y][x] = Reine([y, x], c)
                    elif x == 4:
                        self.list_tab[y][x] = Roi([y, x], c)
                    else:
                        self.list_tab[y][x] = Tour([y, x], c)
                else:
                    self.list_tab[y][x] = Pion([y, x], c)

        for y in 0, 1, 6, 7:
            self.list_pieces.extend(self.list_tab[y])

        self.obj_roi_n = self.list_pieces[4]
        self.obj_roi_b = self.list_pieces[28]

    def fn_afficher_tableau(self):
        print(f"\n  {'_' * 55}{' ' * 47}{'_' * 55}")

        for y in range(8):
            print(f" |{'      |' * 8}{' ' * 45}|{'      |' * 8}"
                  f"\n |  {self.list_tab[y][0]}  |  {self.list_tab[y][1]}  |  {self.list_tab[y][2]}  |  "
                  f"{self.list_tab[y][3]}  |  {self.list_tab[y][4]}  |  {self.list_tab[y][5]}  |  "
                  f"{self.list_tab[y][6]}  |  {self.list_tab[y][7]}  | {8 - y}{' ' * 41}{y + 1} |  "
                  f"{self.list_tab[7 - y][7]}  |  {self.list_tab[7 - y][6]}  |  {self.list_tab[7 - y][5]}  |  "
                  f"{self.list_tab[7 - y][4]}  |  {self.list_tab[7 - y][3]}  |  {self.list_tab[7 - y][2]}  |  "
                  f"{self.list_tab[7 - y][1]}  |  {self.list_tab[7 - y][0]}  |"
                  f"\n |{'______|' * 8}{' ' * 45}|{'______|' * 8}")

        print(f"    A      B      C      D      E      F      G      H{' ' * 52}"
              "H      G      F      E      D      C      B      A")

    def fn_generer_mvt_valides(self) -> None:
        self.bool_echec = False
        list_pieces_dangereuses = []
        list_potentielles_pieces_bloquees = []

        if self.str_couleur_actuelle == "b":
            obj_roi = self.obj_roi_b
        else:
            obj_roi = self.obj_roi_n

        for e in self.list_pieces:
            if e is obj_roi:
                continue

            e.list_mvt_valides = e.fn_mvt_valides(self.list_tab, self.list_tab_danger, self.str_couleur_actuelle)

            if e.str_couleur != self.str_couleur_actuelle:
                while True:
                    if obj_roi.list_position in e.list_mvt_valides:
                        list_pieces_dangereuses.append(e)
                        self.bool_echec = True
                        break

                    if (
                        isinstance(e, (Tour, Reine)) and (e.int_y == obj_roi.int_y or e.int_x == obj_roi.int_x) or
                        isinstance(e, (Fou, Reine)) and abs(e.int_y - obj_roi.int_y) == abs(e.int_x - obj_roi.int_x)
                    ):
                        list_potentielles_pieces_bloquees.append(e)

                    break

        obj_roi.list_mvt_valides = obj_roi.fn_mvt_valides(self.list_tab, self.list_tab_danger, 
                                                          self.str_couleur_actuelle)

        for e in obj_roi.list_mvt_valides[::-1]:
            if self.list_tab_danger[e[0]][e[1]]:
                obj_roi.list_mvt_valides.remove(e)

        if self.bool_echec:
            for e in list_pieces_dangereuses:
                if obj_roi.list_mvt_valides and not isinstance(e, (Chevalier, Pion)):
                    tuple_directions = \
                        Game.fn_direction(obj_roi.int_y - e.int_y), Game.fn_direction(obj_roi.int_x - e.int_x)

                    for e2 in obj_roi.list_mvt_valides[::-1]:
                        if (e2[0] - obj_roi.int_y, e2[1] - obj_roi.int_x) == tuple_directions:
                            obj_roi.list_mvt_valides.remove(e2)
                            break

            if len(list_pieces_dangereuses) == 1:
                obj_piece_dangereuse = list_pieces_dangereuses[0]
                list_bon_mvt = []

                if not isinstance(obj_piece_dangereuse, Chevalier):
                    list_bon_mvt.extend(
                        Game.fn_entre_2_points(obj_roi.list_position, obj_piece_dangereuse.list_position))

                list_bon_mvt.append(obj_piece_dangereuse.list_position)

                for e in self.list_pieces:
                    if e.str_couleur == self.str_couleur_actuelle and not isinstance(e, Roi):
                        for e2 in e.list_mvt_valides[::-1]:
                            if e2 not in list_bon_mvt:
                                e.list_mvt_valides.remove(e2)
            else:
                for e in self.list_pieces:
                    if e.str_couleur == self.str_couleur_actuelle and not isinstance(e, Roi):
                        e.list_mvt_valides.clear()
        elif list_potentielles_pieces_bloquees:
            for e in list_potentielles_pieces_bloquees:
                list_bon_mvt = Game.fn_entre_2_points(e.list_position, obj_roi.list_position)
                list_pieces_rencontrees = []

                for e2 in list_bon_mvt:
                    obj_piece = self.list_tab[e2[0]][e2[1]]

                    if obj_piece != "  ":
                        list_pieces_rencontrees.append(obj_piece)

                if len(list_pieces_rencontrees) == 1:
                    obj_piece = list_pieces_rencontrees[0]

                    if obj_piece.str_couleur == self.str_couleur_actuelle:
                        if isinstance(obj_piece, Chevalier):
                            obj_piece.list_mvt_valides.clear()
                        else:
                            list_bon_mvt.append(e.list_position)

                            for e2 in obj_piece.list_mvt_valides[::-1]:
                                if e2 not in list_bon_mvt:
                                    obj_piece.list_mvt_valides.remove(e2)
                elif len(list_pieces_rencontrees) == 2 and e.int_y == obj_roi.int_y and self.list_en_passant:
                    obj_piece = None

                    for e2 in list_pieces_rencontrees:
                        if isinstance(e2, Pion) and e2.str_couleur == self.str_couleur_actuelle:
                            obj_piece = e2
                            break

                    if obj_piece:
                        for e2 in obj_piece.list_mvt_valides:
                            int_x2 = e2[1]

                            if int_x2 != obj_piece.int_x and self.list_tab[e2[0]][int_x2] == "  ":
                                obj_piece.list_mvt_valides.remove(e2)
                                break

    def fn_game_over(self):
        for e in self.list_pieces:
            if e.str_couleur == self.str_couleur_actuelle and e.list_mvt_valides:
                return False

        return True

    def fn_executer_mvt(self, p_piece, p_destination: list) -> None:
        int_y2, int_x2 = p_destination

        if isinstance(p_piece, Pion) and int_x2 != p_piece.int_x and self.list_tab[int_y2][int_x2] == "  ":
            self.list_pieces.remove(self.list_tab[p_piece.int_y][int_x2])
            self.list_tab[p_piece.int_y][int_x2] = "  "
        elif isinstance(p_piece, Roi):
            int_vx = int_x2 - p_piece.int_x

            if abs(int_vx) == 2:
                if int_vx == 2:
                    obj_tour = self.list_tab[p_piece.int_y][7]
                else:
                    obj_tour = self.list_tab[p_piece.int_y][0]

                self.list_tab[p_piece.int_y][obj_tour.int_x] = "  "
                obj_tour.list_position[1] = obj_tour.int_x = p_piece.int_x + int_vx // 2
                self.list_tab[p_piece.int_y][obj_tour.int_x] = obj_tour

        obj_piece = self.list_tab[int_y2][int_x2]

        if obj_piece != "  ":
            self.list_pieces.remove(obj_piece)

        self.list_tab[int_y2][int_x2] = p_piece
        self.list_tab[p_piece.int_y][p_piece.int_x] = "  "
        p_piece.list_position = p_piece.int_y, p_piece.int_x = p_destination

    @staticmethod
    def fn_entre_2_points(p_position: list, p_destination: list) -> list:
        list_entre_2_points = []
        int_y, int_x = p_position
        int_y2, int_x2 = p_destination
        int_dy = Game.fn_direction(int_y2 - int_y)
        int_dx = Game.fn_direction(int_x2 - int_x)
        int_y += int_dy
        int_x += int_dx

        while int_y != int_y2 or int_x != int_x2:
            list_entre_2_points.append([int_y, int_x])
            int_y += int_dy
            int_x += int_dx

        return list_entre_2_points

    @staticmethod
    def fn_direction(vecteur: int) -> int:
        if vecteur > 0:
            return 1
        elif vecteur < 0:
            return -1

        return 0


class Piece(abc.ABC):
    def __init__(self, p_position: list, p_couleur: str):
        self.list_position = self.int_y, self.int_x = p_position
        self.str_couleur = p_couleur
        self.list_mvt_valides = []

        if isinstance(self, (Pion, Tour, Roi)):
            self.bool_premier_mvt = True

    @abc.abstractmethod
    def fn_mvt_valides(self, p_tab: list, p_tab_danger: list, p_couleur_actuelle: str) -> list:
        pass


class Pion(Piece):
    list_en_passant = []

    def __init__(self, p_position: list, p_couleur: str):
        super().__init__(p_position, p_couleur)

        if self.str_couleur == "b":
            self.int_d = -1  # Direction
        else:
            self.int_d = 1

    def __str__(self):
        return f"P{self.str_couleur}"

    def fn_mvt_valides(self, p_tab: list, p_tab_danger: list, p_couleur_actuelle: str) -> list:
        list_mvt_valides = []
        int_y2 = self.int_y + 1 * self.int_d

        for vx in -1, 1:
            int_x2 = self.int_x + vx

            if -1 < int_x2 < 8:
                if self.str_couleur != p_couleur_actuelle:
                    p_tab_danger[int_y2][int_x2] = True

                list_destination = [int_y2, int_x2]
                obj_piece = p_tab[int_y2][int_x2]

                if obj_piece == "  ":
                    if [self.int_y, int_x2] == Pion.list_en_passant:
                        list_mvt_valides.append(list_destination)
                elif self.str_couleur != obj_piece.str_couleur:
                    list_mvt_valides.append(list_destination)

        if p_tab[int_y2][self.int_x] == "  ":
            list_mvt_valides.append([int_y2, self.int_x])
            int_y2 += self.int_d

            if self.bool_premier_mvt and p_tab[int_y2][self.int_x] == "  ":
                list_mvt_valides.append([int_y2, self.int_x])

        return list_mvt_valides


class Tour(Piece):
    tuple_directions = ((-1, 0), (0, -1), (0, 1), (1, 0))

    def __str__(self):
        return f"T{self.str_couleur}"

    def fn_mvt_valides(self, p_tab: list, p_tab_danger: list, p_couleur_actuelle: str) -> list:
        list_mvt_valides = []

        for d in Tour.tuple_directions:
            for cycle in range(1, 8):
                int_y2 = self.int_y + d[0] * cycle
                int_x2 = self.int_x + d[1] * cycle

                if not (-1 < int_y2 < 8 and -1 < int_x2 < 8):
                    break

                if self.str_couleur != p_couleur_actuelle:
                    p_tab_danger[int_y2][int_x2] = True

                list_destination = [int_y2, int_x2]
                obj_piece = p_tab[int_y2][int_x2]

                if obj_piece == "  ":
                    list_mvt_valides.append(list_destination)
                elif self.str_couleur != obj_piece.str_couleur:
                    list_mvt_valides.append(list_destination)
                    break
                else:
                    break

        return list_mvt_valides


class Chevalier(Piece):
    tuple_vecteurs = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))

    def __str__(self):
        return f"C{self.str_couleur}"

    def fn_mvt_valides(self, p_tab: list, p_tab_danger: list, p_couleur_actuelle: str) -> list:
        list_mvt_valides = []

        for v in Chevalier.tuple_vecteurs:
            int_y2 = self.int_y + v[0]
            int_x2 = self.int_x + v[1]

            if -1 < int_y2 < 8 and -1 < int_x2 < 8:
                if self.str_couleur != p_couleur_actuelle:
                    p_tab_danger[int_y2][int_x2] = True

                if self.str_couleur != str(p_tab[int_y2][int_x2])[1]:
                    list_mvt_valides.append([int_y2, int_x2])

        return list_mvt_valides


class Fou(Piece):
    tuple_directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))

    def __str__(self):
        return f"F{self.str_couleur}"

    def fn_mvt_valides(self, p_tab: list, p_tab_danger: list, p_couleur_actuelle: str) -> list:
        list_mvt_valides = []

        for d in Fou.tuple_directions:
            for cycle in range(1, 8):
                int_y2 = self.int_y + d[0] * cycle
                int_x2 = self.int_x + d[1] * cycle

                if not (-1 < int_y2 < 8 and -1 < int_x2 < 8):
                    break

                if self.str_couleur != p_couleur_actuelle:
                    p_tab_danger[int_y2][int_x2] = True

                list_destination = [int_y2, int_x2]
                obj_piece = p_tab[int_y2][int_x2]

                if obj_piece == "  ":
                    list_mvt_valides.append(list_destination)
                elif self.str_couleur != obj_piece.str_couleur:
                    list_mvt_valides.append(list_destination)
                    break
                else:
                    break

        return list_mvt_valides


class Reine(Piece):
    def __str__(self):
        return f"r{self.str_couleur}"

    def fn_mvt_valides(self, p_tab: list, p_tab_danger: list, p_couleur_actuelle: str) -> list:
        return (
            Tour(self.list_position, self.str_couleur).fn_mvt_valides(p_tab, p_tab_danger, p_couleur_actuelle) +
            Fou(self.list_position, self.str_couleur).fn_mvt_valides(p_tab, p_tab_danger, p_couleur_actuelle)
        )


class Roi(Piece):
    tuple_vecteurs = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

    def __str__(self):
        return f"R{self.str_couleur}"

    def fn_mvt_valides(self, p_tab: list, p_tab_danger: list, p_couleur_actuelle: str) -> list:
        list_mvt_valides = []

        for v in Roi.tuple_vecteurs:
            int_y2 = self.int_y + v[0]
            int_x2 = self.int_x + v[1]

            if -1 < int_y2 < 8 and -1 < int_x2 < 8:
                if self.str_couleur != p_couleur_actuelle:
                    p_tab_danger[int_y2][int_x2] = True

                if self.str_couleur != str(p_tab[int_y2][int_x2])[1]:
                    list_mvt_valides.append([int_y2, int_x2])

        if self.bool_premier_mvt and not p_tab_danger[self.int_y][self.int_x]:
            obj_tour = p_tab[self.int_y][0]

            if (
                isinstance(obj_tour, Tour) and obj_tour.bool_premier_mvt and
                p_tab[self.int_y][1] == p_tab[self.int_y][2] == p_tab[self.int_y][3] == "  " and
                not p_tab_danger[self.int_y][2] and not p_tab_danger[self.int_y][3]
            ):
                list_mvt_valides.append([self.int_y, self.int_x - 2])

            obj_tour = p_tab[self.int_y][7]

            if (
                isinstance(obj_tour, Tour) and obj_tour.bool_premier_mvt and
                p_tab[self.int_y][5] == p_tab[self.int_y][6] == "  " and
                not p_tab_danger[self.int_y][5] and not p_tab_danger[self.int_y][6]
            ):
                list_mvt_valides.append([self.int_y, self.int_x + 2])

        return list_mvt_valides
