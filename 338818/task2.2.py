import sys

# Определим класс узла
class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def is_bst_and_taller_than_n(root: Node, n: int) -> bool:
    """
    Проверяет, является ли дерево BST и превышает ли его высота число N.
    Высота измеряется в ребрах (высота корня = 0).
    """
    
    # Вспомогательная функция DFS
    # Возвращает высоту поддерева (int) или False, если нарушено свойство BST
    def validate_and_measure(node, min_limit, max_limit):
        if node is None:
            return -1  # Высота пустого дерева -1, чтобы высота листа была 0
        
        # 1. Проверка свойства BST
        if not (min_limit < node.value < max_limit):
            return False
        
        # 2. Рекурсивный обход
        left_h = validate_and_measure(node.left, min_limit, node.value)
        # Если левое поддерево не BST, прерываем проверку (Fail-fast)
        if left_h is False:
            return False
            
        right_h = validate_and_measure(node.right, node.value, max_limit)
        # Если правое поддерево не BST, прерываем проверку
        if right_h is False:
            return False
            
        # 3. Возврат высоты текущего узла
        return 1 + max(left_h, right_h)

    # Запускаем проверку с бесконечными границами
    tree_height = validate_and_measure(root, float('-inf'), float('inf'))
    
    # Если дерево невалидно, validate_and_measure вернет False (что равно 0 в int контексте, но проверка типа важна)
    if tree_height is False:
        return False
        
    return tree_height > n

# --- Тестирование ---

def run_tests():
    print("=== Запуск тестов ===")

    # Тест 1: Валидное BST, высота 2. Проверяем N=1 (True)
    #      5
    #     / \
    #    3   7
    #   /
    #  1 
    t1 = Node(5, 
            Node(3, Node(1)), 
            Node(7))
    
    assert is_bst_and_taller_than_n(t1, 1) == True, "Err: T1 height is 2, should be > 1"
    assert is_bst_and_taller_than_n(t1, 2) == False, "Err: T1 height is 2, not > 2"
    print("Тест 1 (Valid BST): OK")

    # Тест 2: Невалидное BST (нарушение справа), высота большая
    #      5
    #     / \
    #    3   4  <-- Ошибка: 4 меньше 5, но находится справа
    #   /
    #  1 
    t2 = Node(5, 
            Node(3, Node(1)), 
            Node(4)) 
    
    assert is_bst_and_taller_than_n(t2, 0) == False, "Err: T2 is not BST"
    print("Тест 2 (Invalid BST): OK")

    # Тест 3: Невалидное BST (нарушение глубоко внизу)
    #      10
    #     /  \
    #    5    15
    #        /  \
    #       6    20
    #            /
    #           25 <-- Ошибка: 25 > 20 (ок), но 25 > 15 (ок), но должно быть < inf.
    #           Однако, давайте сделаем ошибку явной: 6 справа от 15 д.б. > 15, а тут 6.
    t3 = Node(10,
             Node(5),
             Node(15, Node(6), Node(20)))
             
    assert is_bst_and_taller_than_n(t3, 1) == False, "Err: T3 node 6 violates BST"
    print("Тест 3 (Deep violation): OK")

    # Тест 4: Пустое дерево
    assert is_bst_and_taller_than_n(None, 0) == False, "Err: Empty tree height is -1"
    assert is_bst_and_taller_than_n(None, -2) == True, "Err: -1 > -2 should be True"
    print("Тест 4 (Empty): OK")

    # Тест 5: Вырожденное дерево (линия), Валидное
    # 1 -> 2 -> 3 -> 4
    t5 = Node(1, None, Node(2, None, Node(3, None, Node(4))))
    assert is_bst_and_taller_than_n(t5, 2) == True, "Err: Line tree height is 3"
    print("Тест 5 (Line): OK")

run_tests()