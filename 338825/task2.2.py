import time
import random
from array import array
import matplotlib.pyplot as plt

# Базовый узел для SLL
class SNode:
    def __init__(self, value, next_node=None, min_val=None, max_val=None):
        self.value = value
        self.next = next_node
        self.min = min_val
        self.max = max_val

# Модифицированный односвязный список (LIFO / Стек)
class ModifiedSLL:
    def __init__(self):
        self.head = None

    def push(self, value):
        # При вставке за O(1) обновляем локальные min/max
        if self.head is None:
            new_node = SNode(value, None, value, value)
        else:
            new_min = value if value < self.head.min else self.head.min
            new_max = value if value > self.head.max else self.head.max
            new_node = SNode(value, self.head, new_min, new_max)
        self.head = new_node

    def pop(self):
        if self.head is None: return None
        val = self.head.value
        self.head = self.head.next
        return val

    def get_min(self): # O(1)
        return self.head.min if self.head else None

    def get_max(self): # O(1)
        return self.head.max if self.head else None

# Узел для DLL
class DNode:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

# Вспомогательный класс для реализации монотонного дека без list
class MonotonicDeque:
    def __init__(self):
        self.head = None
        self.tail = None

    def push_back(self, val):
        node = DNode(val)
        if not self.tail:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node

    def pop_back(self):
        if not self.tail: return
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None

    def pop_front(self):
        if not self.head: return
        if self.head == self.tail:
            self.head = self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None

# Модифицированный двусвязный список (Deque)
class ModifiedDLL:
    def __init__(self):
        self.head = None
        self.tail = None
        # Монотонные структуры для O(1) min/max
        self.min_deque = MonotonicDeque()
        self.max_deque = MonotonicDeque()

    def push_back(self, value):
        node = DNode(value)
        if not self.tail:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        
        # Обновление монотонного дека для минимума
        while self.min_deque.tail and self.min_deque.tail.value > value:
            self.min_deque.pop_back()
        self.min_deque.push_back(value)

        # Обновление монотонного дека для максимума
        while self.max_deque.tail and self.max_deque.tail.value < value:
            self.max_deque.pop_back()
        self.max_deque.push_back(value)

    def pop_front(self):
        if not self.head: return None
        val = self.head.value
        
        # Если удаляемый элемент - текущий min/max, удаляем из деков
        if self.min_deque.head and self.min_deque.head.value == val:
            self.min_deque.pop_front()
        if self.max_deque.head and self.max_deque.head.value == val:
            self.max_deque.pop_front()

        self.head = self.head.next
        if self.head: self.head.prev = None
        else: self.tail = None
        return val

    def get_min(self): return self.min_deque.head.value if self.min_deque.head else None
    def get_max(self): return self.max_deque.head.value if self.max_deque.head else None

# --- Сравнение сложности ---

def benchmark():
    sizes = array('i', [1000, 5000, 10000, 20000])
    times_simple = array('f')
    times_modified = array('f')

    for n in sizes:
        # Тестируем Modified SLL
        m_sll = ModifiedSLL()
        data = [random.randint(1, 100000) for _ in range(n)] # Временный список для данных
        
        # Замер модифицированного (O(1) получение)
        start = time.perf_counter()
        for v in data:
            m_sll.push(v)
            _ = m_sll.get_min()
        times_modified.append(time.perf_counter() - start)

        # Замер простого (эмуляция O(N) поиска)
        # В простом списке для получения min нужно пройтись по всем N элементам
        start = time.perf_counter()
        current_data = [] # Эмулируем простой список
        for v in data:
            current_data.append(v)
            _ = min(current_data) # Это O(N)
        times_simple.append(time.perf_counter() - start)

    # Визуализация
    plt.figure(figsize=(10, 5))
    plt.plot(list(sizes), list(times_simple), 'r-o', label='Standard List (Min = O(N))')
    plt.plot(list(sizes), list(times_modified), 'g-o', label='Modified List (Min = O(1))')
    plt.xlabel('Количество операций (N)')
    plt.ylabel('Время (сек)')
    plt.title('Сравнение поиска минимума')
    plt.legend()
    plt.grid(True)
    plt.show()

benchmark()