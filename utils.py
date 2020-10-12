def gradient_iter(start, end, size):
    dr = abs(end[0] - start[0]) // (size - 1)
    dr *= -1 if end[0] < start[0] else 1
    dg = abs(end[1] - start[1]) // (size - 1)
    dg *= -1 if end[1] < start[1] else 1
    db = abs(end[2] - start[2]) // (size - 1)
    db *= -1 if end[2] < start[2] else 1
    color = start

    for i in range(size):
        yield color
        color = (color[0] + dr, color[1] + dg, color[2] + db)
    yield end


def distance(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5
