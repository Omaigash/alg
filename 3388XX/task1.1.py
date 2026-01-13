import sys
import time
import random
from array import array
import matplotlib.pyplot as plt

# Увеличим лимит рекурсии для глубоких деревьев
sys.setrecursionlimit(20000)

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class Tree:
    def __init__(self, root_node=None):
        self.root = root_node
        # Хранилища для результатов
        self.max_sum = -float('inf')
        self.min_sum = float('inf')
        self.max_path = array('i')
        self.min_path = array('i')

    def find_min_max_paths(self):
        """Интерфейс для запуска поиска за один обход"""
        if not self.root:
            return None
        
        # Сброс состояний перед поиском
        self.max_sum = -float('inf')
        self.min_sum = float('inf')
        self.max_path = array('i')
        self.min_path = array('i')
        
        current_path = array('i')
        self._dfs(self.root, 0, current_path)
        return self.min_path, self.max_path

    def _dfs(self, node, current_sum, current_path):
        # Добавляем значение текущего узла
        val = node.value
        current_sum += val
        current_path.append(val)

        # Проверка на лист
        if node.left is None and node.right is None:
            # Проверка максимума
            if current_sum > self.max_sum:
                self.max_sum = current_sum
                # Копируем array (срез создает новый объект array)
                self.max_path = array('i', current_path)
            
            # Проверка минимума
            if current_sum < self.min_sum:
                self.min_sum = current_sum
                self.min_path = array('i', current_path)
        else:
            if node.left:
                self._dfs(node.left, current_sum, current_path)
            if node.right:
                self._dfs(node.right, current_sum, current_path)

        # Backtracking: удаляем последний элемент перед возвратом на уровень выше
        current_path.pop()

def build_random_tree(n):
    """Вспомогательная функция для генерации дерева заданной сложности"""
    if n <= 0:
        return None
    root = Node(random.randint(-100, 100))
    nodes = [root] # Здесь list используется только для генерации теста, 
                   # сам алгоритм поиска его не использует.
    for i in range(1, n):
        parent = nodes[(i - 1) // 2]
        new_node = Node(random.randint(-100, 100))
        if i % 2 == 1:
            parent.left = new_node
        else:
            parent.right = new_node
        nodes.append(new_node)
    return Tree(root)

# --- Блок тестирования и анализа сложности ---

def benchmark():
    sizes = array('i', [100, 500, 1000, 2000, 5000, 7000, 10000])
    times = [] # Для построения графика (внешняя библиотека допускает list)
    
    print(f"{'Nodes':<10} | {'Time (sec)':<15}")
    print("-" * 30)
    
    for n in sizes:
        tree = build_random_tree(n)
        
        start_time = time.perf_counter()
        tree.find_min_max_paths()
        end_time = time.perf_counter()
        
        elapsed = end_time - start_time
        times.append(elapsed)
        print(f"{n:<10} | {elapsed:<15.6f}")

    # Теоретическая сложность O(N)
    # Нормируем теорию под масштаб практических данных для визуализации
    k = times[-1] / sizes[-1]
    theoretical_times = [k * n for n in sizes]

    plt.figure(figsize=(10, 6))
    plt.plot(list(sizes), times, 'ob-', label='Практическое время')
    plt.plot(list(sizes), theoretical_times, 'r--', label='Теоретическое O(N)')
    plt.title('Сложность алгоритма поиска путей в дереве')
    plt.xlabel('Количество узлов (N)')
    plt.ylabel('Время выполнения (сек)')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # 1. Простая проверка
    root = Node(10)
    root.left = Node(5)
    root.right = Node(20)
    root.left.left = Node(-2)
    root.left.right = Node(7)
    
    t = Tree(root)
    min_p, max_p = t.find_min_max_paths()
    print("Пример работы:")
    print(f"Путь с мин. суммой ({t.min_sum}): {min_p.tolist()}")
    print(f"Путь с макс. суммой ({t.max_sum}): {max_p.tolist()}\n")
    
    # 2. Бенчмарк
    benchmark()