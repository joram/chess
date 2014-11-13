
TYPES_ABRV = {"pawn": "P",
              "castle": "C",
              "knight": "N",
              "bishop": "B",
              "queen": "Q",
              "king": "K"}

PIECE_VALUES = {"pawn": 1,
                "castle": 3,
                "knight": 2,
                "bishop": 3,
                "queen": 5,
                "king": 100}

COLOURS = {"white": 'W',
           "black": 'B'}

ALPHABET = ["?", "A", "B", "C", "D", "E", "F", "G", "H"]


class Piece():

    def __init__(self, piece_type, colour, position, board):
        self.piece_type = piece_type
        self.colour = colour
        self.value = PIECE_VALUES[piece_type]
        self.name = "%s%s" % (COLOURS[colour], TYPES_ABRV[piece_type])
        self.direction = 1 if self.colour == "white" else -1
        self.opposing_colour = "white" if self.colour == "black" else "black"
        self.position = position
        self.board = board

    def possible_moves(self):
        return []

    def _within_board(self, position):
        (x, y) = position
        if 1 <= x <= 8:
            if 1 <= y <= 8:
                return True

    def on_back_row(self):
        if self.colour == "white" and self.position[1] == 8:
            return True
        if self.colour == "black" and self.position[1] == 1:
            return True

    def position_str(self):
        (x, y) = self.position
        return "%s%s" % (ALPHABET[x], y)

    def __str__(self):
        (x, y) = self.position
        return "%s%s %s%s" % (COLOURS[self.colour],
                              TYPES_ABRV[self.piece_type],
                              ALPHABET[x], y)


class SlidingPiece(Piece):

    def __init__(self, piece_type, colour, position, board, slide_direction):
        self.slide_direction = slide_direction
        Piece.__init__(self, piece_type, colour, position, board)

    def possible_moves(self):
        possible_moves = []
        for offset in self.slide_direction:
            for distance in range(0, 8):
                x = self.position[0] + offset[0]*distance
                y = self.position[1] + offset[1]*distance
                new_square = (x, y)

                # off the board
                if not self._within_board(new_square):
                    break

                # slide until you're stopped
                if self.board.square_occupied(new_square):

                    # take opposing piece
                    if self.board.square_occupied_by(new_square, self.opposing_colour):
                        possible_moves.append(new_square)

                    break
                else:
                    possible_moves.append(new_square)

        return possible_moves