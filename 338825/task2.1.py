from array import array

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class TreeChecker:
    @staticmethod
    def check_properties(root, c, d, A, B):
        """
        Возвращает (is_linear_list, is_heap)
        """
        # (height, is_linear, in_range, is_min, is_max, is_complete, is_perfect)
        res = TreeChecker._dfs(root, c, d)
        
        if res is None:
            return False, False

        height = res[0]
        is_linear = res[1]
        in_range = res[2]
        is_min_h = res[3]
        is_max_h = res[4]
        is_complete = res[5]

        # 1) Проверка на линейный список в диапазоне [c, d]
        check_1 = is_linear and in_range

        # 2) Проверка на кучу с высотой (A, B)
        # Куча = (MinOrder или MaxOrder) + Структура полного дерева + Высота
        check_2 = (is_min_h or is_max_h) and is_complete and (A < height < B)

        return check_1, check_2

    @staticmethod
    def _dfs(node, c, d):
        if node is None:
            # (height, linear, range, min_h, max_h, complete, perfect)
            return (0, True, True, True, True, True, True)

        l = TreeChecker._dfs(node.left, c, d)
        r = TreeChecker._dfs(node.right, c, d)

        # Если в поддеревьях уже что-то фатально не так (для оптимизации можно добавить флаги)
        # Но для чистоты кода вычислим всё:

        # Высота
        h = 1 + max(l[0], r[0])

        # Линейный список: у узла не более 1 ребенка, и поддеревья линейны
        node_is_linear = (node.left is None or node.right is None)
        is_linear = node_is_linear and l[1] and r[1]

        # Диапазон значений [c, d]
        in_range = (c <= node.value <= d) and l[2] and r[2]

        # Свойство Min-Heap (родитель <= детей)
        is_min = l[3] and r[3] and \
                 (node.left is None or node.value <= node.left.value) and \
                 (node.right is None or node.value <= node.right.value)

        # Свойство Max-Heap (родитель >= детей)
        is_max = l[4] and r[4] and \
                 (node.left is None or node.value >= node.left.value) and \
                 (node.right is None or node.value >= node.right.value)

        # Свойство полноты (Complete Binary Tree)
        # Дерево полное, если:
        # 1. Левое perfect, правое complete, hL == hR
        # 2. Левое complete, правое perfect, hL == hR + 1
        is_perfect = l[6] and r[6] and l[0] == r[0]
        is_complete = False
        if l[0] == r[0]:
            if l[6] and r[5]: # l is perfect, r is complete
                is_complete = True
        elif l[0] == r[0] + 1:
            if l[5] and r[6]: # l is complete, r is perfect
                is_complete = True

        return (h, is_linear, in_range, is_min, is_max, is_complete, is_perfect)

# --- Тестирование ---

def test():
    # 1. Создаем линейный список 1 -> 2 -> 3, диапазон [1, 5]
    n1 = Node(1); n1.right = Node(2); n1.right.right = Node(3)
    # Проверка: диапазон [1, 5], Высота > 0 и < 10
    res1 = TreeChecker.check_properties(n1, 1, 5, 0, 10)
    print(f"Test 1 (Linear [1,5]): Linear={res1[0]}, Heap={res1[1]}")

    # 2. Создаем Min-кучу (полное дерево)
    #      1
    #    /   \
    #   2     3
    n2 = Node(1)
    n2.left = Node(2)
    n2.right = Node(3)
    # Проверка: диапазон [0, 10], Высота A=1, B=4 (высота тут 2)
    res2 = TreeChecker.check_properties(n2, 0, 10, 1, 4)
    print(f"Test 2 (Min-Heap): Linear={res2[0]}, Heap={res2[1]}")

    # 3. Не куча (нарушен порядок)
    n3 = Node(10)
    n3.left = Node(1)
    n3.right = Node(1)
    res3 = TreeChecker.check_properties(n3, 0, 100, 1, 5)
    print(f"Test 3 (Bad Order): Linear={res3[0]}, Heap={res3[1]}")

    # Использование array для хранения результатов (демонстрация по условию)
    results = array('b', [res1[0], res1[1], res2[0], res2[1]])
    print("Результаты в array('b'):", results)

test()