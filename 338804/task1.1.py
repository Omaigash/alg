import time
import random
import matplotlib.pyplot as plt
from array import array
import sys

# Увеличим лимит рекурсии для глубоких деревьев
sys.setrecursionlimit(20000)

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class Tree:
    def __init__(self):
        self.root = None

    def is_symmetric(self):
        if not self.root:
            return True
        return self._is_mirror(self.root.left, self.root.right)

    def _is_mirror(self, t1, t2):
        # Если оба узла отсутствуют - симметрично
        if not t1 and not t2:
            return True
        # Если отсутствует только один или значения разные - не симметрично
        if not t1 or not t2:
            return False
        if t1.value != t2.value:
            return False
        
        # Рекурсивная проверка: лево-право и право-лево
        return (self._is_mirror(t1.left, t2.right) and 
                self._is_mirror(t1.right, t2.left))

# Вспомогательная функция для сборки дерева без использования списков
def build_perfect_symmetric_tree(depth, val=1):
    """Создает идеально симметричное дерево заданной глубины."""
    if depth == 0:
        return None
    root = Node(val)
    root.left = build_perfect_symmetric_tree(depth - 1, val)
    root.right = build_perfect_symmetric_tree(depth - 1, val)
    return root

def benchmark():
    # Используем array.array вместо list по условию
    sizes = array('i')  # Кол-во узлов
    times = array('d')  # Время выполнения
    
    # Генерация данных: глубина от 1 до 14 (от 1 до ~16к узлов)
    for depth in range(1, 16):
        tree = Tree()
        tree.root = build_perfect_symmetric_tree(depth)
        
        # Считаем количество узлов: 2^depth - 1
        num_nodes = (2**depth) - 1
        
        # Замер времени (несколько прогонов для точности)
        start_time = time.perf_counter()
        for _ in range(10): 
            tree.is_symmetric()
        end_time = time.perf_counter()
        
        avg_time = (end_time - start_time) / 10
        
        sizes.append(num_nodes)
        times.append(avg_time)
        print(f"Nodes: {num_nodes:6} | Time: {avg_time:.8f} s")

    return sizes, times

# Запуск тестов
sizes, times = benchmark()

# Визуализация
plt.figure(figsize=(10, 6))
plt.plot(sizes, times, 'ob-', label='Практическое время (O(N))')

# Для сравнения построим теоретическую прямую k*N
k = times[-1] / sizes[-1]
theoretical_times = array('d', (k * s for s in sizes))
plt.plot(sizes, theoretical_times, 'r--', label='Теоретическая сложность O(N)')

plt.title('Анализ временной сложности проверки симметрии дерева')
plt.xlabel('Количество узлов (N)')
plt.ylabel('Время выполнения (секунды)')
plt.legend()
plt.grid(True)
plt.show()

def manual_test():
    print("\n--- Ручные тесты ---")
    
    # 1. Симметричное дерево
    #      1
    #    /   \
    #   2     2
    t1 = Tree()
    t1.root = Node(1)
    t1.root.left = Node(2)
    t1.root.right = Node(2)
    print(f"Test 1 (Symmetric): {t1.is_symmetric()}") # True

    # 2. Несимметричное дерево (значения)
    #      1
    #    /   \
    #   2     3
    t2 = Tree()
    t2.root = Node(1)
    t2.root.left = Node(2)
    t2.root.right = Node(3)
    print(f"Test 2 (Values differ): {t2.is_symmetric()}") # False

    # 3. Несимметричное дерево (структура)
    #      1
    #    /   \
    #   2     2
    #    \
    #     3
    t3 = Tree()
    t3.root = Node(1)
    t3.root.left = Node(2)
    t3.root.right = Node(2)
    t3.root.left.right = Node(3)
    print(f"Test 3 (Structure differ): {t3.is_symmetric()}") # False

manual_test()