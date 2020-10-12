from utils import distance
import functools


def k_mean_iter(points, centers, func_for_point=lambda x: x[0], func_for_center=lambda x: x[0]):
    len_points = len(points)
    len_centers = len(centers)

    last_centers = [centers[i][0].copy() for i in range(len_centers)]

    yield points, centers
    while True:
        centers_dict = {}
        for i in range(len_centers):
            centers_dict[i] = [0, []]

        for point in range(len_points):
            coord = func_for_point(points[point])

            min_center = 0
            min_distance = float('inf')
            for center in range(len_centers):
                center_coord = func_for_center(centers[center])
                d = distance(coord, center_coord)
                min_distance = min(d, min_distance)
                if min_distance == d:
                    min_center = center

            centers_dict[min_center][0] += 1
            centers_dict[min_center][1].append(point)

            points[point][2] = centers[min_center][2]
        yield points, centers

        for center in range(len_centers):
            data = centers_dict[center]
            x = 0
            y = 0
            for point in data[1]:
                x += points[point][0][0]
                y += points[point][0][1]

            if data[0] == 0:
                continue
            x //= data[0]
            y //= data[0]

            centers[center][0][0] = x
            centers[center][0][1] = y

        yield points, centers

        _ans = [last_centers[i] == centers[i][0] for i in range(len_centers)]
        if all(_ans) is True:
            pass
            break

        last_centers = [centers[i][0].copy() for i in range(len_centers)]
