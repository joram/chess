from pieces import *
from pieces.king import King
from chess.helpers import alpha_numeric_to_coords, alphanum_move_to_coord, other_colour
import copy

x_axis = ["a", "b", "c", "d", "e", "f", "g", "h"]

PEICE_STR = {
   "WP": WhitePawn,
   "WN": WhiteKnight,
   "WC": WhiteCastle,
   "WB": WhiteBishop,
   "WQ": WhiteQueen,
   "WK": WhiteKing,
   "BP": BlackPawn,
   "BN": BlackKnight,
   "BC": BlackCastle,
   "BB": BlackBishop,
   "BQ": BlackQueen,
   "BK": BlackKing,
}


class ForfeitException(Exception):
    pass


class Board():

    def __init__(self, pieces=None, pgn=None, board_string=None):
        self.pieces = []
        self.position_indexed_pieces = {}
        self.white_squares = []
        self.black_squares = []
        self.move_history = []
        if pgn:
            self._load_from_PGN_string(pgn)
        if board_string:
            self._load_from_board_string(board_string)
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

            end_position = move[:2]
            header = move[2:]

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

    def _load_from_board_string(self, s):
        num_chunks = (len(s)/4)-1
        for i in range(0, num_chunks):
            chunk = s[i*4:(i+1)*4]
            piece_str = chunk[0:2]
            position_str = chunk[2:4]
            position = alpha_numeric_to_coords(position_str)
            self.add_piece(PEICE_STR[piece_str](position, self))

    def _pawn_that_can_move_to(self, to_position, colour):
        return self._piece_that_can_move_to("P", to_position, colour)

    def _piece_that_can_move_to(self, piece_type, to_position, colour):
        for piece in self.pieces:
            if piece.colour == colour and piece.piece_type == piece_type and to_position in piece.possible_moves():
                return piece

    def start_board(self):
        self.game_over = False
        self.winner = None

        # white
        y = 1
        self.add_piece(WhiteCastle((1, y), self))
        self.add_piece(WhiteKnight((2, y), self))
        self.add_piece(WhiteBishop((3, y), self))
        self.add_piece(WhiteQueen((4, y), self))
        self.add_piece(WhiteKing((5, y), self))
        self.add_piece(WhiteBishop((6, y), self))
        self.add_piece(WhiteKnight((7, y), self))
        self.add_piece(WhiteCastle((8, y), self))
        for x in range(1, 9):
            self.add_piece(WhitePawn((x, 2), self))

        # black
        y = 8
        self.add_piece(BlackCastle((1, y), self))
        self.add_piece(BlackKnight((2, y), self))
        self.add_piece(BlackBishop((3, y), self))
        self.add_piece(BlackQueen((4, y), self))
        self.add_piece(BlackKing((5, y), self))
        self.add_piece(BlackBishop((6, y), self))
        self.add_piece(BlackKnight((7, y), self))
        self.add_piece(BlackCastle((8, y), self))
        for x in range(1, 9):
            self.add_piece(BlackPawn((x, 7), self))

    def add_piece(self, piece):
        self.pieces.append(piece)
        if piece.colour == "white":
            self.white_squares.append(piece.position)
        if piece.colour == "black":
            self.black_squares.append(piece.position)
        self.position_indexed_pieces[piece.position] = piece

    def get_pieces(self, piece_class=None, colour=None):
        pieces_list = []
        for p in self.pieces:
            if not piece_class or isinstance(p, piece_class):
                if not colour or p.colour == colour:
                    pieces_list.append(p)
        return pieces_list

    def get_piece(self, piece_class):
        for p in self.pieces:
            if isinstance(p, piece_class):
                return p

    def threatened(self, piece, ignore_kings=False):
        other_pieces = self.get_pieces(colour=other_colour(piece.colour))
        for other_piece in other_pieces:
            if not (ignore_kings and isinstance(other_piece, King)):
                for move in other_piece.possible_moves():
                    if move == piece.position:
                        return True
        return False

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
        all_possible_moves = []
        for piece in self.get_pieces(colour=colour):
            move_from = piece.position
            for move_to in piece.possible_moves():
                move = (move_from, move_to)
                all_possible_moves.append(move)

        if not self.check(colour):
            return all_possible_moves

        possible_moves = []
        for move in all_possible_moves:
            if self.avoids_check(move, colour):
                possible_moves.append(move)
        return possible_moves

    def duplicate(self):
        return copy.deepcopy(self)

    def move(self, move):
        if type(move) == str:
            move = alphanum_move_to_coord(move)
        (move_from, move_to) = move

        # pick up piece
        try:
            piece = self.remove_piece(move_from)
        except KeyError:
            raise ForfeitException("attempted to move a piece that did not exist at position: %s" % move_from)
        self.move_history.append((move, piece))

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

    def undo_move(self):
        (move, piece) = self.move_history[-1]
        self.move_history.remove((move, piece))
        (move_from, move_to) = move

        # pick up piece
        try:
            piece = self.remove_piece(move_to)
        except KeyError:
            raise ForfeitException("attempted to move a piece that did not exist at position: %s" % move_from)
        self.move_history.append((move, piece))

        # place piece
        piece.position = move_from
        # TODO undo queen-ing of a pawn
        self.add_piece(piece)


    def check(self, colour):
        king_class = WhiteKing if colour == "white" else BlackKing
        king = self.get_piece(king_class)
        if king:
            return self.threatened(king, 1)

    def avoids_check(self, move, colour):
        future_board = self.duplicate()
        future_board.move(move)
        if not future_board.check(colour=colour):
            return True
        return False

    def checkmate(self, colour):
        if not self.check(colour):
            return False
        for move in self.possible_moves(colour):
            if self.avoids_check(move, colour):
                return False
        return True


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

    def state(self):
        s = {}
        for piece in self.pieces:
            s[piece.position_str()] = piece.name
        return s

    def state_str(self):
        state = self.state()
        s = ""
        for piece_position in state.keys():
            piece_name = state[piece_position]
            s += "%s%s" % (piece_name, piece_position)
        return s

    def __str__(self):
        s = ""
        for piece in self.pieces:
            s = "%s\n%s" % (s, piece)
        return s