import time
import random
import matplotlib.pyplot as plt
from array import array

class SNode:
    def __init__(self, value, current_min, current_max, next_node=None):
        self.value = value
        self.min = current_min
        self.max = current_max
        self.next = next_node

class ModifiedSLL:
    def __init__(self):
        self.head = None

    def push(self, value):
        if not self.head:
            new_node = SNode(value, value, value)
        else:
            new_min = value if value < self.head.min else self.head.min
            new_max = value if value > self.head.max else self.head.max
            new_node = SNode(value, new_min, new_max, self.head)
        self.head = new_node

    def pop(self):
        if not self.head: return None
        val = self.head.value
        self.head = self.head.next
        return val

    def get_min(self):
        return self.head.min if self.head else float('inf')

    def get_max(self):
        return self.head.max if self.head else float('-inf')
    
class ModifiedDLL:
    def __init__(self):
        # Используем два ModifiedSLL как внутренние стеки
        self.front_stack = ModifiedSLL()
        self.back_stack = ModifiedSLL()

    def push_back(self, value):
        self.back_stack.push(value)

    def push_front(self, value):
        self.front_stack.push(value)

    def _transfer(self, source, target):
        # Переливка элементов для поддержания O(1) амортизировано
        temp = array('i')
        while source.head:
            temp.append(source.pop())
        
        mid = len(temp) // 2
        # Возвращаем половину в исходный
        for i in range(mid - 1, -1, -1):
            source.push(temp[i])
        # Перекладываем половину в целевой
        for i in range(mid, len(temp)):
            target.push(temp[i])

    def pop_front(self):
        if not self.front_stack.head:
            self._transfer(self.back_stack, self.front_stack)
        return self.front_stack.pop()

    def get_min(self):
        return min(self.front_stack.get_min(), self.back_stack.get_min())

    def get_max(self):
        return max(self.front_stack.get_max(), self.back_stack.get_max())
    
def benchmark():
    sizes = array('i', [100, 500, 1000, 2000, 3000, 5000, 7000, 10000])
    times_standard = array('d')
    times_modified = array('d')

    for n in sizes:
        mod_list = ModifiedSLL()
        std_list = array('i')
        for _ in range(n):
            val = random.randint(0, 100000)
            mod_list.push(val)
            std_list.append(val)

        # Тест стандартного поиска (O(N))
        start = time.perf_counter()
        for _ in range(100):
            _ = min(std_list)
        times_standard.append((time.perf_counter() - start) / 100)

        # Тест модифицированного поиска (O(1))
        start = time.perf_counter()
        for _ in range(100):
            _ = mod_list.get_min()
        times_modified.append((time.perf_counter() - start) / 100)

    # Визуализация
    plt.figure(figsize=(10, 5))
    plt.plot(sizes, times_standard, 'r-o', label='Стандартный поиск min() - O(N)')
    plt.plot(sizes, times_modified, 'g-s', label='Модифицированный список - O(1)')
    plt.xlabel('Количество элементов в списке')
    plt.ylabel('Время поиска (сек)')
    plt.title('Сравнение времени получения минимального значения')
    plt.legend()
    plt.grid(True)
    plt.show()

benchmark()