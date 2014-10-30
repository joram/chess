from pieces import *
import copy

x_axis = ["a", "b", "c", "d", "e", "f", "g", "h"]


class Board():
    def __init__(self, pieces=None, pgn=None):
        self.pieces = []
        self.position_indexed_pieces = {}
        self.white_squares = []
        self.black_squares = []
        self.move_history = []
        if pgn:
            self._load_from_PGN_string(pgn)
        else:
            if pieces:
                for piece in pieces:
                    self.add_piece(piece)

    # http://en.wikipedia.org/wiki/Portable_Game_Notation
    def _load_from_PGN_string(self, s):
        self.start_board()

        colour = "white"
        moves = s.split(" ")
        for move in [move for move in moves if "." not in move]:

            if "=" in move:
                parts = move.split("=")
                move = parts[0]
                pawn_upgrades_to = parts[1]
                print("pawn upgrades to: %s" % pawn_upgrades_to)

            end_position = move[:2]
            header = move[2:]
            print("end:'%s'   header:'%s'" % (end_position, header))


            # single choice pawn move
            if len(move) == 2:
                x = x_axis.index(move[0].lower())
                y = int(move[1])
                position = (x, y)
                piece = self._pawn_that_can_move_to(position, colour)
#                self.move((piece.position, position))

            if len(move) == 3:
                piece_type = move[0]
                x = x_axis.index(move[1].lower())
                y = int(move[2])
                position = (x, y)
                self._piece_that_can_move_to(piece_type, position, colour)

            colour = "white" if colour == "black" else "black"

    def _pawn_that_can_move_to(self, to_position, colour):
        return self._piece_that_can_move_to("P", to_position, colour)

    def _piece_that_can_move_to(self, piece_type, to_position, colour):
        for piece in self.pieces:
            if piece.colour == colour and piece.piece_type == piece_type and to_position in piece.possible_moves():
                return piece

    def start_board(self):

        # white
        self.add_piece(WhiteCastle((1, 1), self))
        self.add_piece(WhiteKnight((2, 1), self))
        self.add_piece(WhiteBishop((3, 1), self))
        self.add_piece(WhiteQueen((4, 1), self))
        self.add_piece(WhiteKing((5, 1), self))
        self.add_piece(WhiteBishop((6, 1), self))
        self.add_piece(WhiteKnight((7, 1), self))
        self.add_piece(WhiteCastle((8, 1), self))
        for x in range(1, 9):
            self.add_piece(WhitePawn((x, 2), self))

        # black
        self.add_piece(BlackCastle((1, 8), self))
        self.add_piece(BlackKnight((2, 8), self))
        self.add_piece(BlackBishop((3, 8), self))
        self.add_piece(BlackQueen((4, 8), self))
        self.add_piece(BlackKing((5, 8), self))
        self.add_piece(BlackBishop((6, 8), self))
        self.add_piece(BlackKnight((7, 8), self))
        self.add_piece(BlackCastle((8, 8), self))
        for x in range(1, 9):
            self.add_piece(BlackPawn((x, 7), self))

    def add_piece(self, piece):
        self.pieces.append(piece)
        if piece.colour == "white":
            self.white_squares.append(piece.position)
        if piece.colour == "black":
            self.black_squares.append(piece.position)
        self.position_indexed_pieces[piece.position] = piece

    def remove_piece(self, position):
        piece = self.position_indexed_pieces[position]
        self.pieces.remove(piece)
        if piece.colour == "white":
            self.white_squares.remove(piece.position)
        if piece.colour == "black":
            self.black_squares.remove(piece.position)
        self.position_indexed_pieces.pop(piece.position)
        return piece

    def square_occupied_by(self, square, colour):
        return square in self.position_indexed_pieces and self.position_indexed_pieces[square].colour == colour

    def square_occupied(self, square):
        if self.square_occupied_by(square, "white") or self.square_occupied_by(square, "black"):
            return True

    # TODO castling, empassen, check, and checkmate
    def possible_moves(self, colour=None):
        possible_moves = []
        for piece in self.pieces:
            if not colour or piece.colour == colour:
                move_from = piece.position
                for move_to in piece.possible_moves():
                    possible_moves.append((move_from, move_to))
        return possible_moves

    def duplicate(self):
        return copy.deepcopy(self)

    def move(self, move):
        (move_from, move_to) = move
        self.move_history.append(move)

        # pick up piece
        piece = self.remove_piece(move_from)

        # clear a spot
        taken_piece = None
        if self.square_occupied(move_to):
            taken_piece = self.remove_piece(move_to)
            #print("TOOK: %s" % taken_piece.name)

        # place piece
        piece.position = move_to
        # pawn on the back row
        if piece.piece_type == "pawn" and piece.on_back_row():
            if piece.colour == "white":
                piece = WhiteQueen(move_to, self)
            else:
                piece = BlackQueen(move_to, self)
        self.add_piece(piece)

        return taken_piece

    def print_board(self):
        from pieces.piece import COLOURS, TYPES_ABRV
        for y in [9, 8, 7, 6, 5, 4, 3, 2, 1]:
            row = ""
            for x in range(1, 9):
                position = (x, y)
                piece_name = "__"
                if position in self.position_indexed_pieces:
                    piece = self.position_indexed_pieces[position]
                    piece_name = "%s%s" % (COLOURS[piece.colour], TYPES_ABRV[piece.piece_type])
                row += "%s " % piece_name
            #    print("%s %s" % (piece_name, position))
            print(row)

    def __str__(self):
        s = ""
        for piece in self.pieces:
            s = "%s\n%s" % (s, piece)
        return s