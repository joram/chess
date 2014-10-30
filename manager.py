#!/usr/bin/python
from board import Board
from bots import RandomBot, ImpatientBot, AngryBot


class GameManager:

    def __init__(self, WhiteBotClass, BlackBotClass):
        self.debug = False
        self.game_over = False
        self.winner = None
        self.board = Board()
        self.white_bot = WhiteBotClass("white")
        self.black_bot = BlackBotClass("black")

    def bot(self, colour):
        return self.white_bot if colour == "white" else self.black_bot

    def move(self, colour):
        opponent_colour = "white" if colour == "black" else "black"

        try:
            # white's move
            move = self.bot(colour).move(self.board.duplicate())
            if move in self.board.possible_moves(colour):
                if self.debug:
                    print("%s %s: %s" % (len(self.board.move_history), colour, str(move)))
                self.board.move(move)
            else:
                if self.debug:
                    print("%s %s: %s (invalid move. forfeit)" % (len(self.board.move_history), colour, str(move)))
                self.winner = opponent_colour
                self.game_over = True

        except Exception as e:
            if self.debug:
                print(e)
            self.winner = opponent_colour
            self.game_over = True

    def play_chess(self):
        self.board.start_board()

        if self.debug:
            self.board.print_board()

        while not self.game_over:
            for colour in ["white", "black"]:
                if not self.winner:
                    self.move(colour)

        if self.debug:
            self.board.print_board()

        return self.winner

    def compete(self, num_games):
        print("%s VS %s" % (self.white_bot, self.black_bot))

        white_wins, black_wins = self._compete_once(num_games)
        print("%s/%s %s (white)" % (white_wins, num_games, self.white_bot))
        print("%s/%s %s (black)" % (black_wins, num_games, self.black_bot))
        print("")

        white_wins, black_wins = self._compete_once(num_games)
        print("%s/%s %s (white)" % (white_wins, num_games, self.black_bot))
        print("%s/%s %s (black)" % (black_wins, num_games, self.white_bot))

    def _compete_once(self, num_games):
        white_wins = 0
        black_wins = 0
        for i in range(0, num_games):
            winner = self.play_chess()
            if winner == "white":
                white_wins += 1
            if winner == "black":
                black_wins += 1
            print(winner)
        return white_wins, black_wins



GameManager(RandomBot, AngryBot).compete(10)