import time
import random
from array import array
import matplotlib.pyplot as plt

def quicksort(arr, low, high):
    """Ручная реализация QuickSort для array.array (так как .sort() нет)"""
    if low < high:
        pivot = arr[(low + high) // 2]
        i = low
        j = high
        while i <= j:
            while arr[i] < pivot: i += 1
            while arr[j] > pivot: j -= 1
            if i <= j:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
                j -= 1
        quicksort(arr, low, j)
        quicksort(arr, i, high)

def find_three_sum(nums_input):
    """
    Находит уникальные тройки с суммой 0.
    Использует array.array для всех операций.
    """
    # Превращаем входные данные в array.array
    nums = array('i', nums_input)
    n = len(nums)
    if n < 3:
        return array('i')

    # 1. Сортировка - O(N log N)
    quicksort(nums, 0, n - 1)
    
    # Результирующий плоский массив (каждые 3 элемента = тройка)
    results = array('i')

    # 2. Основной цикл - O(N^2)
    for i in range(n - 2):
        # Пропускаем дубликаты для первого числа
        if i > 0 and nums[i] == nums[i-1]:
            continue
            
        left = i + 1
        right = n - 1
        
        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]
            
            if current_sum == 0:
                # Нашли тройку
                results.append(nums[i])
                results.append(nums[left])
                results.append(nums[right])
                
                # Пропускаем дубликаты для второго и третьего чисел
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif current_sum < 0:
                left += 1
            else:
                right -= 1
                
    return results

def format_output(res_array):
    """Вспомогательная функция для вывода в формате списка списков"""
    out = []
    for i in range(0, len(res_array), 3):
        out.append([res_array[i], res_array[i+1], res_array[i+2]])
    return out

# --- Тестирование и Анализ ---

def benchmark():
    # Размеры массивов для теста (N)
    # Берем небольшие шаги, так как N^2 растет быстро
    sizes = array('i', [50, 100, 200, 300, 400, 500, 600])
    times = []

    print(f"{'N':<10} | {'Time (sec)':<15}")
    print("-" * 30)

    for n in sizes:
        # Генерируем случайные числа
        test_data = [random.randint(-100, 100) for _ in range(n)]
        
        start = time.perf_counter()
        find_three_sum(test_data)
        end = time.perf_counter()
        
        elapsed = end - start
        times.append(elapsed)
        print(f"{n:<10} | {elapsed:<15.6f}")

    # Теоретическая кривая O(N^2)
    # Нормируем под последний замер: k = t_last / n_last^2
    k = times[-1] / (sizes[-1]**2)
    theoretical_times = [k * (n**2) for n in sizes]

    plt.figure(figsize=(10, 6))
    plt.plot(list(sizes), times, 'ob-', label='Практическое время (O(N^2))')
    plt.plot(list(sizes), theoretical_times, 'r--', label='Теоретическое O(N^2)')
    plt.title('Сложность алгоритма 3Sum (Two Pointers)')
    plt.xlabel('Количество элементов (N)')
    plt.ylabel('Время выполнения (сек)')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # 1. Проверка на примере из условия
    example_input = [-1, 0, 1, 2, -1, -4]
    res_array = find_three_sum(example_input)
    print("Вход:", example_input)
    print("Выход:", format_output(res_array))
    print()

    # 2. Запуск бенчмарка
    benchmark()