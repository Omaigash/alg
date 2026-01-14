import sys
import time
import random
from array import array
import matplotlib.pyplot as plt

# Увеличим лимит рекурсии для глубоких деревьев (худший случай)
sys.setrecursionlimit(20000)

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class Tree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        """Вставка элемента в дерево (вариант BST для удобства построения)"""
        if self.root is None:
            self.root = Node(value)
            return
        
        current = self.root
        while True:
            if value < current.value:
                if current.left is None:
                    current.left = Node(value)
                    break
                current = current.left
            else:
                if current.right is None:
                    current.right = Node(value)
                    break
                current = current.right

def get_paths_outside_range(tree, a, b):
    """
    Находит пути от корня до листа, длина которых (кол-во узлов) < a или > b.
    Использует только array, без list.
    Возвращает (flat_paths, path_lengths), где flat_paths - сплошной массив значений.
    """
    # Массив для хранения текущего пути в рекурсии
    current_path = array('i')
    
    # Массивы для результата
    # flat_results хранит все найденные пути подряд
    flat_results = array('i')
    # result_lengths хранит длины путей, чтобы потом можно было разделить flat_results
    result_lengths = array('i')
    
    if tree.root is None:
        return flat_results, result_lengths

    def dfs(node):
        # Добавляем значение в текущий путь (аналог append)
        current_path.append(node.value)
        
        # Проверяем, является ли узел листом
        if node.left is None and node.right is None:
            path_len = len(current_path)
            # Условие: длина ВНЕ диапазона [a, b]
            if path_len < a or path_len > b:
                # Сохраняем длину найденного пути
                result_lengths.append(path_len)
                # Копируем текущий путь в результирующий плоский массив
                # array.extend работает эффективно
                flat_results.extend(current_path)
        else:
            if node.left:
                dfs(node.left)
            if node.right:
                dfs(node.right)
        
        # Backtracking: удаляем последний элемент (аналог pop)
        current_path.pop()

    dfs(tree.root)
    return flat_results, result_lengths

# --- Вспомогательные функции для тестов и замеров ---

def generate_random_tree(size):
    t = Tree()
    # Используем array для генерации значений, чтобы не нарушать условие "без list" даже в тесте
    values = array('i', (random.randint(0, 100000) for _ in range(size)))
    for v in values:
        t.insert(v)
    return t

def benchmark():
    sizes = array('i', range(100, 10100, 500)) # 100, 600, 1100...
    times = array('d') # Double precision float
    
    # Диапазон исключения [a, b]. 
    # Возьмем узкий диапазон, чтобы путей находилось больше (худший случай для копирования)
    # Или широкий, чтобы проверить чистый обход.
    # Возьмем средние значения.
    a, b = 10, 20 

    for n in sizes:
        tree = generate_random_tree(n)
        
        start_time = time.perf_counter()
        get_paths_outside_range(tree, a, b)
        end_time = time.perf_counter()
        
        times.append(end_time - start_time)
        
    return sizes, times

# --- Демонстрация работы ---
def print_example():
    print("--- Демонстрация на малом дереве ---")
    # Создадим дерево вручную для наглядности
    #       10
    #      /  \
    #     5    15
    #    /       \
    #   2         20
    #              \
    #               25
    t = Tree()
    t.insert(10)
    t.insert(5)
    t.insert(15)
    t.insert(2)  # Путь 10-5-2 (длина 3)
    t.insert(20)
    t.insert(25) # Путь 10-15-20-25 (длина 4)

    # Ищем пути длиной вне [4, 5]. 
    # Длина 3 < 4 (подходит). Длина 4 в [4, 5] (не подходит).
    flat_res, lens = get_paths_outside_range(t, 4, 5)
    
    print(f"Диапазон исключения [4, 5]. Ожидаем путь длины 3.")
    print(f"Длины найденных путей: {lens}")
    print(f"Все значения путей подряд: {flat_res}")
    
    # Восстановление путей для вывода (визуально)
    offset = 0
    for length in lens:
        # Срез array работает, создавая новый array
        path = flat_res[offset : offset + length]
        print(f"Путь: {path}")
        offset += length

# Запуск
if __name__ == "__main__":
    print_example()
    
    print("\n--- Запуск тестов производительности ---")
    sizes, measured_times = benchmark()
    
    # Построение графика
    # Приводим к 'обычному' виду только для matplotlib, так как он может требовать iterable
    # array является iterable, поэтому можно передавать напрямую.
    
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, measured_times, label='Practical Time', marker='o')
    
    # Теоретическая сложность O(N)
    # Подгоним коэффициент k для графика k*N, взяв последнюю точку
    k = measured_times[-1] / sizes[-1]
    theoretical_times = array('d', (k * x for x in sizes))
    
    plt.plot(sizes, theoretical_times, label='Theoretical O(N)', linestyle='--')
    
    plt.xlabel('Number of Nodes (N)')
    plt.ylabel('Time (seconds)')
    plt.title('Algorithm Complexity Analysis: Binary Tree Path Finding')
    plt.legend()
    plt.grid(True)
    plt.show()
