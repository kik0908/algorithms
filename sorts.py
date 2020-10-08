from random import shuffle


def bubble_sort_iter(array: list, func=lambda x: x):
    array_len = len(array)
    iterations = 0
    for i in range(array_len):
        for j in range(0, array_len - i - 1):
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
            iterations += 1
            if func(array[j]) < func(array[ind_min]):
                ind_min = j
            yield array

        array[i], array[ind_min] = array[ind_min], array[i]


    return iterations


if __name__ == "__main__":
    a = list(range(50))
    shuffle(a)
    print(a)
    print(list(sort_by_choice_iter(a))[0])
    a = list(range(10))
    shuffle(a)
    print(a)
    list(bubble_sort_iter(a))
