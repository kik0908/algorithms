from random import shuffle, choice


def bubble_sort_iter(array: list, func=lambda x: x):
    array_len = len(array)
    iterations = 0
    for i in range(array_len):
        for j in range(0, array_len - i - 1):
            iterations += 1
            if func(array[j]) > func(array[j + 1]):
                array[j], array[j + 1] = array[j + 1], array[j]
                yield array

    yield array
    return iterations


def sort_by_choice_iter(array: list, func=lambda x: x):
    array_len = len(array)
    iterations = 0
    for i in range(array_len):
        ind_min = i
        for j in range(i, array_len):
            iterations += 1
            if func(array[j]) < func(array[ind_min]):
                ind_min = j

        array[i], array[ind_min] = array[ind_min], array[i]
        yield array

    yield array
    return iterations


def double_selection_sort_iter(array: list, func=lambda x: x):
    array_len = len(array)
    c = 0
    iterations = 0
    for i in range(array_len//2):
        ind_min = i
        ind_max = i
        for j in range(i, array_len-c):
            iterations += 1
            if func(array[j]) < func(array[ind_min]):
                ind_min = j
            if func(array[j]) > func(array[ind_max]):
                ind_max = j

        array[i], array[ind_min] = array[ind_min], array[i]
        if ind_max == i:
            ind_max = ind_min
        array[array_len-c-1], array[ind_max] = array[ind_max], array[array_len-c-1]
        c += 1
        yield array


    yield array
    return iterations


def insertion_sort_iter(array, func=lambda x: x):
    array_len = len(array)
    iterations = 0

    for i in range(1, array_len):
        for j in range(i - 1, -1, -1):

            iterations += 1
            if func(array[i]) < func(array[j]):
                array = array[:j] + [array[i]] + array[j:i] + array[i + 1:]
                yield array
                i -= 1
            else:
                break

    yield array
    return iterations


def __lomuto_partition_iter(arr, low, high, func):
    pivot = func(arr[high])
    i = (low - 1)
    for j in range(low, high):

        if (func(arr[j]) <= pivot):
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            yield arr
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    yield arr
    yield (i + 1)


def lomuto_quickSort_iter(arr, low=0, high=None, func=lambda x: x):
    if high is None:
        high = len(arr)-1

    if (low < high):

        try:
            i = __lomuto_partition_iter(arr, low, high, func)
            while True:
                pi = next(i)
                if not isinstance(pi, int):
                    yield pi
        except StopIteration:
            pass

        yield arr
        yield from lomuto_quickSort_iter(arr, low, pi - 1, func)
        yield from lomuto_quickSort_iter(arr, pi + 1, high, func)


def __hoare_partition_iter(array, low, high, func):
    pivot = func(array[low])
    i = low - 1
    j = high + 1

    while True:
        i += 1
        while func(array[i]) < pivot:
            i += 1
        j -= 1
        while func(array[j]) > pivot:
            j -= 1
        if i >= j:
            yield j

        array[i], array[j] = array[j], array[i]
        yield array


def hoare_quickSort_iter(array, low=0, high=None, func=lambda x: x):
    if high is None:
        high = len(array)-1
    if low < high:
        try:
            i = __hoare_partition_iter(array, low, high, func=lambda x: x)
            while True:
                pi = next(i)
                if isinstance(pi, int):
                    break
                else:
                    yield pi
        except StopIteration:
            pass

        yield array
        yield from hoare_quickSort_iter(array, low, pi, func=lambda x: x)
        yield from hoare_quickSort_iter(array, pi + 1, high, func=lambda x: x)


def merge_sort_iter(data: list, func=lambda x: x):
    if len(data) > 2:
        part_1 = next(merge_sort_iter(data[:len(data) // 2]))
        part_2 = next(merge_sort_iter(data[len(data) // 2:]))
        data = part_1 + part_2
        yield data
        last_index = len(data) - 1

        for i in range(last_index):
            min_value = func(data[i])
            min_index = i

            for j in range(i + 1, last_index + 1):
                if min_value > func(data[j]):
                    min_value = func(data[j])
                    min_index = j

            if min_index != i:
                data[i], data[min_index] = data[min_index], data[i]
                yield data

    elif len(data) > 1 and func(data[0]) > func(data[1]):
        data[0], data[1] = data[1], data[0]
        yield data

    yield data


def cocktail_sort_iter(array, func=lambda x: x[0]):
    left = 0
    right = len(array) - 1

    while left <= right:
        for i in range(left, right, +1):
            if func(array[i]) > func(array[i + 1]):
                array[i], array[i + 1] = array[i + 1], array[i]
        right -= 1

        for i in range(right, left, -1):
            if func(array[i - 1]) > func(array[i]):
                array[i], array[i - 1] = array[i - 1], array[i]
        left += 1
        yield array

if __name__ == "__main__":
    pass
