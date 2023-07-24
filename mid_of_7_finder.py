from fractions import Fraction


def get_cartesian_point(column, row):
    x = column - (width / 2)
    y = -(row - (height / 2))
    return x, y


def get_opencv_point(x, y):
    column = x + (width / 2)
    row = -(y - (height / 2))
    column = Fraction(column / width)
    row = Fraction(row / height)
    return str(column), str(row)


# https://stackoverflow.com/a/20677983
def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


def calculate(top_right, bottom_left):
    p1 = get_cartesian_point(top_right[0], top_right[1])
    p2 = get_cartesian_point(bottom_left[0], bottom_left[1])

    p3 = get_cartesian_point(0, height / 2)
    p4 = get_cartesian_point(width, height / 2)

    intersection_point = line_intersection((p1, p2), (p3, p4))
    mid_point = get_opencv_point(intersection_point[0], intersection_point[1])
    return mid_point


width = height = 1024
top_right = (width, 0)
bottom_left = (128, height)
print(calculate(top_right, bottom_left))
