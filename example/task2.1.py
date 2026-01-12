import sys
import time
import random
import math
from array import array

# Если вы хотите график, убедитесь, что библиотека установлена: pip install matplotlib
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Внимание: matplotlib не установлен. График не будет построен.")

# Увеличим лимит рекурсии для глубоких деревьев
sys.setrecursionlimit(50000)

# ==========================================
# 1. ОБЩИЕ КЛАССЫ (Структура данных)
# ==========================================

class Node:
    __slots__ = ('val', 'left', 'right')
    
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

class Tree:
    def __init__(self):
        self.root = None

    def insert_random(self, val):
        """Вставка для генерации случайных деревьев (для тестов)"""
        if self.root is None:
            self.root = Node(val)
            return
        curr = self.root
        while True:
            if random.random() < 0.5:
                if curr.left is None:
                    curr.left = Node(val)
                    break
                curr = curr.left
            else:
                if curr.right is None:
                    curr.right = Node(val)
                    break
                curr = curr.right

# ==========================================
# 2. ЗАДАЧА №1: Поиск путей определенной длины
# ==========================================

def find_paths_in_range(tree, a, b):
    """
    Находит пути от корня до листа длиной [a, b].
    Возвращает array('i') в формате: [len1, val1, val2..., len2, val1...]
    """
    results = array('i')
    path_stack = array('i')
    
    if tree.root is None:
        return results

    def _dfs(node, current_length):
        path_stack.append(node.val)
        
        # Если лист
        if node.left is None and node.right is None:
            if a <= current_length <= b:
                results.append(len(path_stack))
                results.extend(path_stack)
        else:
            if node.left:
                _dfs(node.left, current_length + 1)
            if node.right:
                _dfs(node.right, current_length + 1)
        
        path_stack.pop()

    _dfs(tree.root, 0)
    return results

def print_paths_result(results_array):
    """Вспомогательная функция для вывода путей"""
    if not results_array:
        print(" -> Пути не найдены.")
        return
    
    i = 0
    count = 0
    while i < len(results_array):
        path_len = results_array[i]
        i += 1
        # Используем срез для вывода (превратится в list только для print)
        path = results_array[i : i + path_len]
        print(f" -> Путь {count + 1} (Длина={path_len-1}): {path.tolist()}") 
        i += path_len
        count += 1

# ==========================================
# 3. ЗАДАЧА №2: Проверка свойств (Линейный спис. и АВЛ)
# ==========================================

def check_tree_properties(tree, A, B, c, d):
    """
    Проверяет за один проход:
    1. Линейный список с диапазоном значений [c, d].
    2. АВЛ-дерево с высотой (A, B).
    Возвращает (is_linear, is_avl)
    """
    INF = float('inf')
    N_INF = float('-inf')

    def dfs(node):
        # Возврат: (height, min_val, max_val, is_avl, is_linear)
        if node is None:
            return 0, INF, N_INF, True, True

        l_h, l_min, l_max, l_avl, l_lin = dfs(node.left)
        r_h, r_min, r_max, r_avl, r_lin = dfs(node.right)
        
        val = node.val
        
        # --- AVL Checks ---
        is_bst = (l_max < val) and (val < r_min)
        is_balanced = abs(l_h - r_h) <= 1
        cur_avl = l_avl and r_avl and is_bst and is_balanced
        
        cur_h = max(l_h, r_h) + 1
        cur_min = min(val, l_min)
        cur_max = max(val, r_max)

        # --- Linear Checks ---
        in_range = (c <= val <= d)
        no_two_children = not ((node.left is not None) and (node.right is not None))
        cur_lin = l_lin and r_lin and in_range and no_two_children

        return cur_h, cur_min, cur_max, cur_avl, cur_lin

    root_h, _, _, root_is_avl, root_is_linear = dfs(tree.root)

    res_linear = root_is_linear # Условие: Структура линии + значения [c, d]
    # Условие: Структура АВЛ + высота строго между A и B
    res_avl = root_is_avl and (A < root_h < B)

    return res_linear, res_avl

# ==========================================
# 4. ТЕСТИРОВАНИЕ И ГРАФИК
# ==========================================

def performance_graph():
    if not HAS_MATPLOTLIB:
        return

    sizes = [1000, 5000, 10000, 20000, 40000]
    times = []

    print("\n--- Генерация графика сложности (Задача 1) ---")
    for n in sizes:
        # Быстро создаем дерево (почти линию, чтобы не тратить время на рандом)
        t = Tree()
        nodes = [Node(i) for i in range(n)]
        t.root = nodes[0]
        for i in range(1, n):
            # Простое чередование для скорости генерации O(N)
            if i % 2 == 0: nodes[i-1].left = nodes[i]
            else: nodes[i-1].right = nodes[i]
        
        start = time.perf_counter()
        find_paths_in_range(t, 0, n) # Ищем все пути
        end = time.perf_counter()
        times.append(end - start)
        print(f"N={n}, Time={end - start:.4f}s")

    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times, 'o-', label='Практика')
    
    # Теория O(N)
    k = times[-1] / sizes[-1]
    plt.plot(sizes, [k*x for x in sizes], 'r--', label='Теория O(N)')
    
    plt.title('Сложность алгоритма поиска путей')
    plt.xlabel('Количество узлов')
    plt.ylabel('Время (сек)')
    plt.legend()
    plt.grid(True)
    plt.savefig('tree_complexity.png')
    print("График сохранен как tree_complexity.png")
    # plt.show() # Раскомментируйте, если запускаете не на сервере

def main():
    print("=== ЧАСТЬ 1: Демонстрация поиска путей ===")
    # Создаем дерево:
    #      1
    #     / \
    #    2   3
    #   /
    #  4
    t = Tree()
    t.root = Node(1)
    t.root.left = Node(2)
    t.root.right = Node(3)
    t.root.left.left = Node(4)
    
    print("Дерево создано. Ищем пути длиной [1, 2]:")
    paths = find_paths_in_range(t, 1, 2) # Путь 1-3 (len 1), 1-2-4 (len 2)
    print_paths_result(paths)

    print("\n=== ЧАСТЬ 2: Демонстрация проверки свойств ===")
    
    # Тест Линейного списка (1->2->3)
    t_lin = Tree()
    t_lin.root = Node(1)
    t_lin.root.right = Node(2)
    t_lin.root.right.right = Node(3)
    
    # Проверяем: Линейное в [0, 5]? АВЛ с высотой (1, 10)?
    # Для 1-2-3 высота 3. Это не АВЛ (баланс нарушен 0 vs 2).
    is_lin, is_avl = check_tree_properties(t_lin, A=1, B=10, c=0, d=5)
    print(f"Дерево (1->2->3). \n -> Линейное [0,5]? {is_lin} \n -> АВЛ (1<H<10)? {is_avl}")

    # Тест АВЛ (треугольник)
    t_avl = Tree()
    t_avl.root = Node(2)
    t_avl.root.left = Node(1)
    t_avl.root.right = Node(3)
    
    is_lin2, is_avl2 = check_tree_properties(t_avl, A=1, B=5, c=0, d=10)
    print(f"\nДерево (1<-2->3). \n -> Линейное [0,10]? {is_lin2} \n -> АВЛ (1<H<5)? {is_avl2}")

    # Запуск теста производительности
    performance_graph()

if __name__ == "__main__":
    main()
