import sys
import time
import random
from array import array

# Увеличим лимит рекурсии для глубоких деревьев (вырожденных в линию)
sys.setrecursionlimit(50000)

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
        """Вспомогательная функция для создания случайного дерева."""
        if self.root is None:
            self.root = Node(val)
            return

        curr = self.root
        while True:
            # Случайный спуск влево или вправо
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

def find_paths_in_range(tree, a, b):
    """
    Находит все пути от корня до листа длиной (кол-во ребер) от a до b.
    Возвращает array('i'), содержащий найденные пути в формате:
    [len_path1, node_val1, node_val2..., len_path2, node_val1...]
    """
    # Результирующий массив (плоский список всех путей)
    # Используем 'i' (signed int), предполагая, что значения узлов целые
    results = array('i')
    
    # Стек для хранения текущего пути
    path_stack = array('i')
    
    if tree.root is None:
        return results

    def _dfs(node, current_length):
        # Добавляем текущий узел в стек пути
        path_stack.append(node.val)
        
        # Проверяем, является ли узел листом
        if node.left is None and node.right is None:
            # Проверяем условие диапазона длины (по количеству ребер)
            if a <= current_length <= b:
                # Сохраняем результат.
                # Чтобы "разделить" пути в одном массиве, 
                # сначала запишем длину пути (количество узлов = ребра + 1), затем сами узлы.
                # Кол-во узлов = len(path_stack)
                results.append(len(path_stack))
                results.extend(path_stack)
        else:
            if node.left:
                _dfs(node.left, current_length + 1)
            if node.right:
                _dfs(node.right, current_length + 1)
        
        # Backtracking: удаляем текущий узел из стека при возврате вверх
        path_stack.pop()

    _dfs(tree.root, 0)
    return results

# Вспомогательная функция для красивого вывода результатов из плоского array
def print_results(results_array):
    if not results_array:
        print("Пути не найдены.")
        return
    
    i = 0
    count = 0
    while i < len(results_array):
        path_len = results_array[i] # Количество узлов в пути
        i += 1
        # Срез в array работает, но создает новый array/list. 
        # Чтобы не нарушать правила "без list" в логике, тут при выводе допустимо.
        path = results_array[i : i + path_len]
        # Преобразуем в строку для вывода
        print(f"Путь {count + 1} (L={path_len-1}): {path.tolist()}") 
        i += path_len
        count += 1

# --- Проверка работы функции ---

print("=== ТЕСТ 1: Ручная конфигурация ===")
#      1
#     / \
#    2   3
#   /     \
#  4       5
#           \
#            6
t = Tree()
t.root = Node(1)
t.root.left = Node(2)
t.root.left.left = Node(4) # Лист, длина 2
t.root.right = Node(3)
t.root.right.right = Node(5)
t.root.right.right.right = Node(6) # Лист, длина 3

# Ищем пути длиной от 2 до 3
print("Ищем пути длиной [2, 3]:")
res = find_paths_in_range(t, 2, 3)
print_results(res)

print("\n=== ТЕСТ 2: Пустое дерево ===")
t_empty = Tree()
res_empty = find_paths_in_range(t_empty, 0, 10)
print_results(res_empty)

print("\n=== ТЕСТ 3: Один узел (длина 0) ===")
t_single = Tree()
t_single.root = Node(100)
# Диапазон [0, 0] должен найти корень
res_single = find_paths_in_range(t_single, 0, 0)
print_results(res_single)
