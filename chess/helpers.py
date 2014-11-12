x_axis = ["a", "b", "c", "d", "e", "f", "g", "h"]


def other_colour(colour):
    return "black" if colour == "white" else "white"


def coords_to_alpha_numeric(x, y):
    return "%s%d" % (x_axis[x-1].upper(), y)


def alpha_numeric_to_coords(s):
    c = s[0]
    x = x_axis.index(c.lower())+1
    y = int(s[1])
    return x, y


def coord_move_to_alphanum(coord_move):
    ((x1, y1), (x2, y2)) = coord_move
    start = coords_to_alpha_numeric(x1, y1)
    end = coords_to_alpha_numeric(x2, y2)
    return "%s%s" % (start, end)


def alphanum_move_to_coord(alphanum_move):
    try:
        start = alphanum_move[0:2]
        start = alpha_numeric_to_coords(start)
        end = alphanum_move[2:4]
        end = alpha_numeric_to_coords(end)
        move = (start, end)
    except Exception as e:
        print "exception converting: '%s'" % alphanum_move
        raise e
    return move