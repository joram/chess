from django.db import models


class Move(models.Model):
    game = models.ForeignKey('Game')
    frm = models.CharField(max_length=2)
    to = models.CharField(max_length=2)
    piece = models.CharField(max_length=2)

    board_start_state = models.CharField(max_length=64)

    @property
    def board_end_state(self):
        return self.board_start_state

    @property
    def board_state(self):
        p = {}
        s = self.board_start_state
        chunks = (s[0+i:4+i] for i in range(0, len(str(s)), 4))
        for chunk in chunks:
            piece = chunk[0:2]
            position = chunk[2:4]
            p[position] = piece
        return p

    class Meta:
        app_label = 'chess'
        db_table = "chess_move"

    def __unicode__(self):
        return "(%s) %s->%s" % (self.piece, self.frm, self.to)
