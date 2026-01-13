import sys
import time
import random
from array import array
import matplotlib.pyplot as plt

# Увеличим лимит рекурсии
sys.setrecursionlimit(20000)

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class Tree:
    def __init__(self, root=None):
        self.root = root

    def validate_heap(self, A, B):
        """
        Проверяет, является ли дерево кучей в диапазоне высот (A, B) за один проход.
        Возвращает (is_heap, type, height)
        """
        if not self.root:
            return (False, None, 0)

        # Состояние для прохода
        self._count = 0
        self._max_index = 0
        self._max_depth = 0
        self._violates_min = False
        self._violates_max = False

        # Запускаем DFS
        self._dfs(self.root, 0, 1)

        # 1. Проверка на полноту (Complete Binary Tree)
        # Если макс. индекс == кол-во узлов - 1, значит дырок нет
        is_complete = (self._max_index == self._count - 1)
        
        # 2. Проверка высоты
        height_ok = A < self._max_depth < B
        
        # 3. Определение типа кучи
        is_min_heap = is_complete and not self._violates_min
        is_max_heap = is_complete and not self._violates_max
        
        is_heap = (is_min_heap or is_max_heap) and height_ok
        
        heap_type = None
        if is_heap:
            heap_type = "Min-Heap" if is_min_heap else "Max-Heap"
            
        return is_heap, heap_type, self._max_depth

    def _dfs(self, node, index, depth):
        self._count += 1
        if index > self._max_index:
            self._max_index = index
        if depth > self._max_depth:
            self._max_depth = depth

        # Проверка свойств кучи относительно левого ребенка
        if node.left:
            if node.left.value < node.value:
                self._violates_min = True
            if node.left.value > node.value:
                self._violates_max = True
            self._dfs(node.left, 2 * index + 1, depth + 1)

        # Проверка свойств кучи относительно правого ребенка
        if node.right:
            if node.right.value < node.value:
                self._violates_min = True
            if node.right.value > node.value:
                self._violates_max = True
            self._dfs(node.right, 2 * index + 2, depth + 1)

# --- Инструменты для генерации и тестов ---

def build_complete_tree(n, is_max_heap=True):
    """Строит полную бинарную кучу для тестов"""
    if n <= 0: return None
    # Создаем значения (отсортированные для выполнения свойств кучи)
    vals = array('i', sorted([random.randint(0, 1000) for _ in range(n)], reverse=is_max_heap))
    
    nodes = [Node(vals[i]) for i in range(n)] # Используем list только для сборки структуры
    for i in range(n):
        left_idx = 2 * i + 1
        right_idx = 2 * i + 2
        if left_idx < n:
            nodes[i].left = nodes[left_idx]
        if right_idx < n:
            nodes[i].right = nodes[right_idx]
    return nodes[0]

# --- Анализ сложности ---

def benchmark():
    sizes = array('i', [100, 500, 1000, 2000, 4000, 6000, 8000, 10000])
    practical_times = []

    print(f"{'Nodes':<10} | {'Is Heap?':<12} | {'Time (sec)':<15}")
    print("-" * 45)

    for n in sizes:
        root = build_complete_tree(n)
        tree = Tree(root)
        
        start = time.perf_counter()
        res, h_type, h = tree.validate_heap(0, 100) # Широкий диапазон высот
        end = time.perf_counter()
        
        elapsed = end - start
        practical_times.append(elapsed)
        print(f"{n:<10} | {str(res):<12} | {elapsed:<15.6f}")

    # Теоретическое O(N)
    k = practical_times[-1] / sizes[-1]
    theoretical_times = [k * n for n in sizes]

    plt.figure(figsize=(10, 5))
    plt.plot(list(sizes), practical_times, 'ob-', label='Практическое время')
    plt.plot(list(sizes), theoretical_times, 'r--', label='Теоретическое O(N)')
    plt.title('Проверка дерева на свойства кучи за один проход')
    plt.xlabel('Количество узлов (N)')
    plt.ylabel('Время (сек)')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # Тест 1: Валидная Max-куча
    # Высота для 7 узлов = 3 (1-2-4)
    root = build_complete_tree(7, is_max_heap=True)
    t = Tree(root)
    is_h, t_type, h = t.validate_heap(1, 5)
    print(f"Результат теста 1: {is_h}, Тип: {t_type}, Высота: {h}")
    
    # Тест 2: Не куча (нарушена полнота)
    root2 = Node(100)
    root2.right = Node(50) # Нет левого ребенка, но есть правый
    t2 = Tree(root2)
    is_h2, _, _ = t2.validate_heap(0, 10)
    print(f"Результат теста 2 (неполное): {is_h2}")

    # Запуск бенчмарка
    benchmark()