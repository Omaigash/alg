import random
import time
import math
import matplotlib.pyplot as plt

def merge_intervals(intervals):
    """
    Объединяет перекрывающиеся интервалы.
    :param intervals: List[List[int]]
    :return: List[List[int]]
    """
    if not intervals:
        return []

    # 1. Сортировка по времени начала O(N log N)
    intervals.sort(key=lambda x: x[0])

    merged = []
    
    # 2. Линейный проход O(N)
    for interval in intervals:
        # Если список пуст или текущий интервал не пересекается с предыдущим
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval)
        else:
            # Пересечение есть: объединяем, обновляя конец интервала
            merged[-1][1] = max(merged[-1][1], interval[1])

    return merged

# --- Проверка на примере из условия ---
input_data = [[1,3], [8,10], [2,6], [15,18]]
result = merge_intervals(input_data)
print(f"Input: {input_data}")
print(f"Output: {result}")
# Ожидается: [[1, 6], [8, 10], [15, 18]]

def benchmark_and_plot():
    sizes = [1000 * i for i in range(1, 101)]  # От 1 000 до 100 000 элементов
    times = []

    print("Запуск тестов...")
    for n in sizes:
        # Генерация n случайных интервалов
        # start от 0 до n*2, длина от 1 до 20
        test_data = []
        for _ in range(n):
            start = random.randint(0, n * 2)
            end = start + random.randint(1, 20)
            test_data.append([start, end])
        
        # Замер времени
        start_time = time.perf_counter()
        merge_intervals(test_data)
        end_time = time.perf_counter()
        
        times.append(end_time - start_time)

    # --- Подготовка теоретических данных ---
    # Сложность O(N log N)
    # Находим коэффициент k, чтобы совместить графики (берем последнюю точку)
    # time = k * N * log(N)  =>  k = time / (N * log(N))
    last_n = sizes[-1]
    last_time = times[-1]
    k = last_time / (last_n * math.log(last_n))
    
    theoretical_times = [k * n * math.log(n) for n in sizes]

    # --- Построение графика ---
    plt.figure(figsize=(10, 6))
    
    # Практические замеры
    plt.plot(sizes, times, label='Практическое время', color='blue', linewidth=2)
    
    # Теоретическая кривая
    plt.plot(sizes, theoretical_times, label='Теория O(N log N)', color='red', linestyle='--', linewidth=2)
    
    plt.title('Сложность объединения интервалов (Sorting + Merge)')
    plt.xlabel('Количество интервалов (N)')
    plt.ylabel('Время выполнения (сек)')
    plt.legend()
    plt.grid(True)
    
    filename = 'intervals_complexity.png'
    plt.savefig(filename)
    print(f"График сохранен в файл: {filename}")
    plt.show()

benchmark_and_plot()