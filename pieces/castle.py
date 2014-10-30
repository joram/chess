from pieces.piece import SlidingPiece


class Castle(SlidingPiece):
    def __init__(self, colour, position, board):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        SlidingPiece.__init__(self, "castle", colour, position, board, directions)


class WhiteCastle(Castle):
    def __init__(self, position, board):
        Castle.__init__(self, "white", position, board)


class BlackCastle(Castle):
    def __init__(self, position, board):
        Castle.__init__(self, "black", position, board)
