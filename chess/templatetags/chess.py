from django.template.defaulttags import register
from django.templatetags.static import static

PIECE_FILENAMES = {
    'BP': "black_pawn.png",
    'BC': "black_castle.png",
    'BN': "black_knight.png",
    'BB': "black_bishop.png",
    'BQ': "black_queen.png",
    'BK': "black_king.png",
    'WP': "white_pawn.png",
    'WC': "white_castle.png",
    'WN': "white_knight.png",
    'WB': "white_bishop.png",
    'WQ': "white_queen.png",
    'WK': "white_king.png"
}


@register.filter
def piece_image(piece_name, size="500x500"):
    filename = PIECE_FILENAMES.get(piece_name)
    if filename:
        url = static('images/pieces/%s/%s' % (size, filename))
        return "<img src='%s'></img>" % url

@register.filter
def piece_image_src(piece_name, size="500x500"):
    filename = PIECE_FILENAMES.get(piece_name)
    if filename:
        url = static('images/pieces/%s/%s' % (size, filename))
        return url