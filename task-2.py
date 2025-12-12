
# Двійковий пошук у відсортованому масиві
def binary_search(sorted_array, target):

    low = 0
    high = len(sorted_array) - 1
    iterations = 0
    upper_bound = None

    while low <= high:
        iterations += 1
        mid = (low + high) // 2
        # Якщо елемент менший target, шукаємо в правій половині
        if sorted_array[mid] < target:
            low = mid + 1
        # Якщо елемент більший або рівний target:
        else:
            # Це можлива "верхня межа", запам'ятовуємо її.
            upper_bound = sorted_array[mid]
            # Продовжуємо пошук у лівій частині, щоб знайти ще менший елемент
            high = mid - 1

    return (iterations, upper_bound)



# Тест

# Відсортований масив дробів
arr = [0.1, 0.5, 1.3, 2.4, 3.6, 4.8, 5.5, 7.2, 9.9]

# Пошук відсутного в масиві числа (3.6 - 4.8)
target1 = 4.0
result1 = binary_search(arr, target1)
print(f"Ціль: {target1} -> Результат: {result1}") 

# Пошук наявного в масиві числа
target2 = 7.2
result2 = binary_search(arr, target2)
print(f"Ціль: {target2} -> Результат: {result2}") 

# Пошук числа більшого за всі елементи масиву
target3 = 15.0
result3 = binary_search(arr, target3)
print(f"Ціль: {target3} -> Результат: {result3}") 
