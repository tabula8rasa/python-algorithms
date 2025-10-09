from typing import List, Optional

def binary_search(array: List[float], length: int, number: float) -> Optional[int]:
    """
    function returns index first appearance of the element in the array or returns None
    if there is no element in the array.
    :param array: list of float
    :param length: number of elements in the array
    :param number: float
    :return: int or None
    """

    l = 0
    r = length - 1
    point = length // 2

    while l <= r and array[point] != number:
        if number < array[point]:
            r = point - 1
        else:
            l = point + 1
        point = (l + r) // 2

    if l > r:
        return None
    else:
        i = point - 1
        while i >= 0 and array[i] == number:
            i -= 1
        return i + 1


# Массивы для граничных случаев
empty_arr   = []
single_arr  = [42]
two_arr     = [3, 9]
odd_arr     = [1, 2, 3, 4, 5]                 # длина 5
even_arr    = [2, 4, 6, 8, 10, 12]            # длина 6
neg_arr     = [-10, -5, -1, 0, 4, 7]
long_arr    = list(range(1, 11))              # 1..10

print("--- empty ---")
print(binary_search(empty_arr, len(empty_arr), 1) == None)

print("--- single element ---")
print(binary_search(single_arr, len(single_arr), 42) == 0)     # найден единственный
print(binary_search(single_arr, len(single_arr), 41) == None)  # меньше минимума
print(binary_search(single_arr, len(single_arr), 43) == None)  # больше максимума

print("--- two elements ---")
print(binary_search(two_arr, len(two_arr), 3)  == 0)           # первый элемент
print(binary_search(two_arr, len(two_arr), 9)  == 1)           # второй элемент
print(binary_search(two_arr, len(two_arr), 6)  == None)        # между ними
print(binary_search(two_arr, len(two_arr), 2)  == None)        # ниже минимума
print(binary_search(two_arr, len(two_arr), 10) == None)        # выше максимума

print("--- odd length ---")
print(binary_search(odd_arr, len(odd_arr), 1)  == 0)           # край слева
print(binary_search(odd_arr, len(odd_arr), 3)  == 2)           # ровно середина
print(binary_search(odd_arr, len(odd_arr), 5)  == 4)           # край справа
print(binary_search(odd_arr, len(odd_arr), 0)  == None)        # меньше минимума
print(binary_search(odd_arr, len(odd_arr), 6)  == None)        # больше максимума
print(binary_search(odd_arr, len(odd_arr), 2.5) == None)       # между элементами (не целое)

print("--- even length ---")
print(binary_search(even_arr, len(even_arr), 2)   == 0)        # первый
print(binary_search(even_arr, len(even_arr), 12)  == 5)        # последний
print(binary_search(even_arr, len(even_arr), 8)   == 3)        # любой внутренний
print(binary_search(even_arr, len(even_arr), 5)   == None)     # отсутствует между 4 и 6
print(binary_search(even_arr, len(even_arr), 1)   == None)     # ниже минимума
print(binary_search(even_arr, len(even_arr), 100) == None)     # выше максимума

print("--- negatives & zeros ---")
print(binary_search(neg_arr, len(neg_arr), -10) == 0)          # отрицательное, первый
print(binary_search(neg_arr, len(neg_arr), 0)   == 3)          # ноль
print(binary_search(neg_arr, len(neg_arr), 7)   == 5)          # положительное, последний
print(binary_search(neg_arr, len(neg_arr), -6)  == None)       # между -10 и -5
print(binary_search(neg_arr, len(neg_arr), 5)   == None)       # между 4 и 7

print("--- floats near ints ---")
print(binary_search(long_arr, len(long_arr), 5.0)    == 4)     # 5.0 == 5 → найден
print(binary_search(long_arr, len(long_arr), 5.0001) == None)  # не ровно целое → нет
print(binary_search(long_arr, len(long_arr), 4.9999) == None)  # не ровно целое → нет

print("--- large boundaries ---")
print(binary_search(long_arr, len(long_arr), 1)   == 0)        # самый левый
print(binary_search(long_arr, len(long_arr), 10)  == 9)        # самый правый
print(binary_search(long_arr, len(long_arr), 0)   == None)     # меньше минимума
print(binary_search(long_arr, len(long_arr), 11)  == None)     # больше максимума
print("---")
