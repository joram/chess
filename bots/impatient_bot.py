from bots.bot import ChessBot


class ImpatientBot(ChessBot):

    def __str__(self):
        return "Impatient Bot"

    def move(self, board):
        possible_moves = board.possible_moves(self.colour)
        return possible_moves[0]
