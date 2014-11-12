from django.db import models
from move import Move
from play_game import play_single_game
from chess.helpers import coords_to_alpha_numeric
from board import Board


class GameManager(models.Manager):

    def create_for_cmds(self, white_cmd, white_name, black_cmd, black_name):
        white = {'cmd': white_cmd, 'name': white_name, "colour": "white"}
        black = {'cmd': black_cmd, 'name': black_name, "colour": "black"}
        finished_board = play_single_game(white, black)
        winner_name = white_name if finished_board.winner == "white" else black_name

        game = Game.objects.create(
            white_player=white_name,
            black_player=black_name,
            winner=winner_name)

        board = Board()
        board.start_board()
        for (move, piece) in finished_board.move_history:
            print "%s %s" % (piece.name, move)
            ((frm_x, frm_y), (to_x, to_y)) = move
            frm = coords_to_alpha_numeric(frm_x, frm_y)
            to = coords_to_alpha_numeric(to_x, to_y)
            Move.objects.create(
                game=game,
                frm=frm,
                to=to,
                piece=piece.name,
                board_start_state=board.state_str())
            board.move(move)


class Game(models.Model):
    white_player = models.CharField(max_length=100)
    black_player = models.CharField(max_length=100)
    winner = models.CharField(max_length=100)
    objects = GameManager()

    @property
    def moves(self):
        return list(Move.objects.filter(game_id=self.id).order_by('id'))

    @property
    def moves_count(self):
        return len(Move.objects.filter(game_id=self.id))

    class Meta:
        app_label = 'chess'
        db_table = "chess_game"
