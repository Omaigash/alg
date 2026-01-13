import time
import random
from array import array
import matplotlib.pyplot as plt

# Класс узла дерева
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# Класс бинарного дерева
class Tree:
    def __init__(self, root_val=None):
        if root_val is not None:
            self.root = Node(root_val)
        else:
            self.root = None

    def find_paths_with_sum(self, target_sum):
        """
        Запускает поиск путей от корня до листа с суммой N.
        Использует генератор для возврата путей без создания списка.
        """
        # Используем array('i') для хранения текущего пути (целые числа)
        current_path = array('i')
        return self._dfs_search(self.root, target_sum, 0, current_path)

    def _dfs_search(self, node, target, current_sum, path):
        if node is None:
            return

        # Добавляем значение текущего узла
        current_sum += node.value
        path.append(node.value)

        # Проверка: является ли узел листом
        is_leaf = node.left is None and node.right is None

        if is_leaf:
            if current_sum == target:
                # Возвращаем копию текущего пути как новый array
                yield array('i', path)
        else:
            # Рекурсивный обход детей
            yield from self._dfs_search(node.left, target, current_sum, path)
            yield from self._dfs_search(node.right, target, current_sum, path)

        # Бэктрекинг (откат): удаляем узел из пути при возврате на уровень выше
        path.pop()

# Вспомогательная функция для построения случайного дерева заданного размера
def build_random_tree(n):
    if n <= 0: return None
    root = Node(random.randint(1, 10))
    nodes = [root] # Здесь используем список только для генерации теста, не в алгоритме
    for i in range(n - 1):
        parent = random.choice(nodes)
        new_node = Node(random.randint(1, 10))
        if not parent.left:
            parent.left = new_node
            nodes.append(new_node)
        elif not parent.right:
            parent.right = new_node
            nodes.append(new_node)
    t = Tree()
    t.root = root
    return t

# --- Тестирование и Анализ сложности ---

sizes = array('i', [100, 500, 1000, 2000, 5000, 10000, 15000, 20000])
times = array('f')

print("Запуск тестов...")
for n in sizes:
    tree = build_random_tree(n)
    target = random.randint(10, 50)
    
    start_time = time.perf_counter()
    # Итерируемся по генератору, чтобы выполнить поиск
    for _ in tree.find_paths_with_sum(target):
        pass
    end_time = time.perf_counter()
    
    times.append(end_time - start_time)
    print(f"Размер: {n}, Время: {times[-1]:.5f} сек")

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(list(sizes), list(times), 'bo-', label='Практическое время')
# Теоретическая кривая O(N) для сравнения (масштабированная)
k = times[-1] / sizes[-1]
theoretical = [k * x for x in sizes]
plt.plot(list(sizes), theoretical, 'r--', label='Теоретическая сложность O(N)')

plt.title("Зависимость времени выполнения от количества узлов")
plt.xlabel("Количество узлов (N)")
plt.ylabel("Время (секунды)")
plt.legend()
plt.grid(True)
plt.show()