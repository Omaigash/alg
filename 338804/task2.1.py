import sys

# Увеличим лимит рекурсии на случай глубоких деревьев
sys.setrecursionlimit(10000)

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class Tree:
    def __init__(self, root_node=None):
        self.root = root_node

    def validate_properties(self, c, d, A, B):
        """
        Проверяет все условия за один проход.
        Возвращает: (is_bst, is_min_heap, is_max_heap)
        """
        # Запускаем рекурсивный анализ
        res = self._analyze(self.root, c, d)
        
        height = res[5]
        is_height_ok = A < height < B
        
        # Дерево является BST, если оно структурно BST и все значения в [c, d]
        # (Проверка диапазона c, d встроена в _analyze)
        is_bst = res[0] and is_height_ok # Добавим условие высоты, если это требуется по логике задачи
        
        # Дерево является кучей, если оно "полное", значения упорядочены и высота подходит
        is_min_heap = res[3] and res[6] and is_height_ok
        is_max_heap = res[3] and res[7] and is_height_ok
        
        return is_bst, is_min_heap, is_max_heap

    def _analyze(self, node, c, d):
        """
        Рекурсивная функция. Возвращает кортеж:
        0: is_bst (bool)
        1: min_val (float) - минимальное значение в поддереве
        2: max_val (float) - максимальное значение в поддереве
        3: is_complete (bool) - является ли дерево "полным" (для кучи)
        4: is_perfect (bool) - является ли дерево "идеальным" (все уровни заполнены)
        5: height (int) - высота
        6: is_min_ordered (bool) - выполняется ли свойство min-heap (parent <= children)
        7: is_max_ordered (bool) - выполняется ли свойство max-heap (parent >= children)
        8: within_range (bool) - все ли узлы в [c, d]
        """
        if not node:
            # Базовый случай для пустого узла
            return (True, float('inf'), float('-inf'), True, True, 0, True, True, True)

        # Рекурсивно получаем данные от детей
        L = self._analyze(node.left, c, d)
        R = self._analyze(node.right, c, d)

        # 1. Проверка диапазона [c, d]
        current_within_range = (c <= node.value <= d) and L[8] and R[8]

        # 2. Проверка свойств BST
        # Левый макс < текущий < правый мин
        current_is_bst = (L[0] and R[0] and 
                          L[2] < node.value < R[1] and 
                          current_within_range)

        # 3. Высота и полнота (для Heap)
        height = max(L[5], R[5]) + 1
        # Идеальное дерево: оба ребенка идеальны и одной высоты
        is_perfect = L[4] and R[4] and L[5] == R[5]
        # Полное дерево (структура кучи):
        # 1. Левое идеально, правое полное, высота одинакова
        # 2. Левое полное, правое идеально, лево выше на 1
        is_complete = (
            (L[4] and R[3] and L[5] == R[5]) or
            (L[3] and R[4] and L[5] == R[5] + 1)
        )

        # 4. Проверка порядка значений кучи
        # Для min-heap: значение <= детей
        left_val = node.left.value if node.left else float('inf')
        right_val = node.right.value if node.right else float('inf')
        is_min_ordered = L[6] and R[6] and node.value <= left_val and node.value <= right_val
        
        # Для max-heap: значение >= детей
        left_val_max = node.left.value if node.left else float('-inf')
        right_val_max = node.right.value if node.right else float('-inf')
        is_max_ordered = L[7] and R[7] and node.value >= left_val_max and node.value >= right_val_max

        # Аккумулируем мин/макс значения для BST проверок уровнем выше
        min_v = min(node.value, L[1], R[1])
        max_v = max(node.value, L[2], R[2])

        return (current_is_bst, min_v, max_v, is_complete, is_perfect, 
                height, is_min_ordered, is_max_ordered, current_within_range)

# --- Тестирование ---

def test_trees():
    # Настройки
    c, d = 0, 100
    A, B = 1, 5

    print(f"Параметры: Range=[{c},{d}], Height ∈ ({A},{B})\n")

    # 1. Идеальный BST
    #      50
    #    /    \
    #  25      75
    node1 = Node(50)
    node1.left = Node(25)
    node1.right = Node(75)
    t1 = Tree(node1)
    print("Дерево 1 (BST):", t1.validate_properties(c, d, A, B)) 
    # Ожидаем: (True, False, False) т.к. BST, но не куча (75 > 50, 25 < 50)

    # 2. Min-Heap
    #      10
    #    /    \
    #  20      30
    # /
    # 40
    node2 = Node(10)
    node2.left = Node(20)
    node2.right = Node(30)
    node2.left.left = Node(40)
    t2 = Tree(node2)
    print("Дерево 2 (Min-Heap):", t2.validate_properties(c, d, A, B))
    # Ожидаем: (False, True, False)

    # 3. Нарушение диапазона [c, d]
    #      50 (но d = 40)
    t3 = Tree(Node(50))
    print("Дерево 3 (Вне [c,d]):", t3.validate_properties(0, 40, 0, 5))
    # Ожидаем: (False, False, False)

    # 4. Нарушение высоты
    # Высота 1, а нужно > 1
    t4 = Tree(Node(10))
    print("Дерево 4 (Высота 1, A=1):", t4.validate_properties(0, 100, 1, 5))
    # Ожидаем: (False, False, False) так как 1 не > 1

test_trees()