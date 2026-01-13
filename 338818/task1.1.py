from array import array
import time
import random
import matplotlib.pyplot as plt
import sys

# Увеличим лимит рекурсии для глубоких деревьев (на случай "вырожденных" деревьев-линий)
sys.setrecursionlimit(20000)

class Node:
    __slots__ = ['value', 'left', 'right'] # Оптимизация памяти
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class Tree:
    def __init__(self):
        self.root = None

    def find_paths_in_range(self, a, b):
        """
        Находит все пути от корня до листа, сумма значений которых лежит в [a, b].
        Использует array вместо list для текущего пути.
        """
        results = [] # Здесь будем хранить найденные пути (массивы)
        
        # 'l' - signed long (минимум 4 байта), подходит для целых чисел
        current_path = array('l') 
        
        if self.root is None:
            return results

        self._dfs(self.root, 0, current_path, results, a, b)
        return results

    def _dfs(self, node, current_sum, current_path, results, a, b):
        # 1. Добавляем текущий узел в путь и обновляем сумму
        current_sum += node.value
        current_path.append(node.value)

        # 2. Проверяем, является ли узел листом
        if node.left is None and node.right is None:
            if a <= current_sum <= b:
                # Если условие выполнено, сохраняем копию текущего пути
                # (создаем новый array на основе старого)
                results.append(array('l', current_path))
        else:
            # 3. Рекурсивный обход
            if node.left:
                self._dfs(node.left, current_sum, current_path, results, a, b)
            if node.right:
                self._dfs(node.right, current_sum, current_path, results, a, b)

        # 4. Backtracking: удаляем текущий узел из пути перед возвратом на уровень выше
        current_path.pop()

# --- Вспомогательные функции для генерации деревьев ---

def generate_random_tree(size, min_val=-10, max_val=10):
    """Генерирует случайное дерево размера size."""
    if size == 0:
        return Tree()
    
    t = Tree()
    t.root = Node(random.randint(min_val, max_val))
    nodes = [t.root] # Используем список как очередь для построения
    
    # Заполняем дерево до нужного размера
    count = 1
    while count < size:
        parent = random.choice(nodes) # Выбираем случайного родителя (делает дерево более хаотичным)
        child = Node(random.randint(min_val, max_val))
        
        if parent.left is None:
            parent.left = child
            nodes.append(child)
            count += 1
        elif parent.right is None:
            parent.right = child
            nodes.append(child)
            count += 1
        # Если у родителя оба потомка заняты, цикл продолжится и выберет другого родителя
        
    return t

# --- Проверка работы на конфигурациях ---

def test_configurations():
    print("=== Тестирование конфигураций ===")
    
    # Тест 1: Простое дерево
    #       5
    #      / \
    #     3   8
    #    /   / \
    #   2   1   4
    t = Tree()
    t.root = Node(5)
    t.root.left = Node(3)
    t.root.left.left = Node(2) # Путь: 5+3+2 = 10
    t.root.right = Node(8)
    t.root.right.left = Node(1) # Путь: 5+8+1 = 14
    t.root.right.right = Node(4) # Путь: 5+8+4 = 17
    
    print("\nТест 1 (Ручная конфигурация):")
    paths = t.find_paths_in_range(9, 15)
    for p in paths:
        print(f"Путь: {p.tolist()}, Сумма: {sum(p)}")
    # Ожидается: [5, 3, 2] (10) и [5, 8, 1] (14). [5, 8, 4] (17) не подходит.

    # Тест 2: Пустое дерево
    t_empty = Tree()
    print("\nТест 2 (Пустое дерево):", t_empty.find_paths_in_range(0, 100))

    # Тест 3: Отрицательные значения
    t_neg = Tree()
    t_neg.root = Node(10)
    t_neg.root.left = Node(-5) # Лист, сумма 5
    print("\nТест 3 (Отрицательные числа, диапазон [4, 6]):")
    paths = t_neg.find_paths_in_range(4, 6)
    for p in paths:
        print(f"Путь: {p.tolist()}, Сумма: {sum(p)}")

test_configurations()

def benchmark_and_plot():
    print("\n=== Запуск бенчмарка (это может занять время) ===")
    
    sizes = [1000 * i for i in range(1, 51)] # От 1000 до 50000 узлов
    times = []
    
    # Для стабильности замеров будем искать диапазон, охватывающий все возможные суммы,
    # чтобы алгоритм проходил до конца, но копирование не занимало всё время.
    # Диапазон [-inf, +inf] заставит копировать каждый путь.
    # Сделаем узкий диапазон, чтобы мерить чистую скорость обхода (Traversal).
    a, b = 1000000, 1000001 # Маловероятный диапазон
    
    for n in sizes:
        # Генерируем дерево
        tree = generate_random_tree(n, -100, 100)
        
        # Замеряем время
        start_time = time.perf_counter()
        tree.find_paths_in_range(a, b)
        end_time = time.perf_counter()
        
        times.append(end_time - start_time)
        
        if n % 10000 == 0:
            print(f"Processed size: {n}")

    # Построение графика
    plt.figure(figsize=(10, 6))
    
    # Практические данные
    plt.plot(sizes, times, 'o-', label='Практическое время (Traversal)')
    
    # Теоретическая прямая (линейная регрессия для наглядности)
    # y = k * x. Возьмем k как time/size для последней точки
    k = times[-1] / sizes[-1]
    theoretical_times = [k * x for x in sizes]
    plt.plot(sizes, theoretical_times, 'r--', label='Теоретическое O(N)')
    
    plt.title('Зависимость времени выполнения от количества узлов в дереве')
    plt.xlabel('Количество узлов (N)')
    plt.ylabel('Время (секунды)')
    plt.legend()
    plt.grid(True)
    
    # Сохраняем график (или plt.show() если запускаете локально)
    plt.savefig('complexity_graph.png')
    print("График сохранен как complexity_graph.png")
    plt.show()

benchmark_and_plot()