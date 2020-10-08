from random import shuffle, choice


def bubble_sort_iter(array: list, func=lambda x: x):
    array_len = len(array)
    iterations = 0
    for i in range(array_len):
        for j in range(0, array_len - i - 1):
            yield array
            iterations += 1
            if func(array[j]) > func(array[j + 1]):
                array[j], array[j + 1] = array[j + 1], array[j]

    yield array
    return iterations


def sort_by_choice_iter(array: list, func=lambda x: x):
    array_len = len(array)
    iterations = 0
    for i in range(array_len):
        ind_min = i
        for j in range(i, array_len):
            yield array
            iterations += 1
            if func(array[j]) < func(array[ind_min]):
                ind_min = j

        array[i], array[ind_min] = array[ind_min], array[i]
    yield array
    return iterations


def insertion_sort_iter(array, func=lambda x: x):
    array_len = len(array)
    iterations = 0

    for i in range(1, array_len):
        for j in range(i - 1, -1, -1):
            yield array
            iterations += 1
            if func(array[i]) < func(array[j]):
                array = array[:j] + [array[i]] + array[j:i] + array[i + 1:]
                i -= 1
            else:
                break

    yield array
    return iterations


if __name__ == "__main__":
    pass
