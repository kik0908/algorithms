from random import shuffle

def __hoare_partition_iter(array, low, high):
    pivot = array[low]
    i = low - 1
    j = high + 1

    while (True):
        i += 1
        while array[i] < pivot:
            i += 1
        j -= 1
        while array[j] > pivot:
            j -= 1
        if i >= j:
            yield j

        array[i], array[j] = array[j], array[i]
        yield array

def hoare_quickSort_iter(array, low, high):
    if (low < high):
        try:
            i = __hoare_partition_iter(array, low, high)
            while True:
                pi = next(i)
                if isinstance(pi, int):
                    break
                else:
                    yield pi
        except StopIteration:
            pass

        yield array
        yield from hoare_quickSort_iter(array, low, pi)
        yield from hoare_quickSort_iter(array, pi + 1, high)


def printArray(arr, n):
    for i in range(n):
        print(arr[i], end=" ")
    print()


# Driver code
arr = list(range(1, 16))
shuffle(arr)
arr = [2, 1, 15, 8, 10, 5, 7, 6, 9, 3, 4, 11, 13, 14, 12]
print(arr)
n = len(arr)
a = hoare_quickSort_iter(arr, 0, n - 1)
for i in a:
    print(i)
