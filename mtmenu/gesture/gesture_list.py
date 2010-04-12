#BASIC MOVES

DOWN    = [(1,2), (1,1)]
UP      = [(1,1), (1,2)]
RIGHT   = [(1,1), (2,1)]
LEFT    = [(2,1), (1,1)]


def combine(a, b):
    return map(lambda x,y:(x[0]*y[0],x[1]*y[1]), a, b)

