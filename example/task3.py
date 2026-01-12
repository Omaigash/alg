import sys
import random
import time
import math

# Для графиков
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Matplotlib не найден. Графики не будут построены, только текстовый вывод.")

# Бесконечность для инициализации
INF = float('inf')

# ==========================================
# 1. Структуры узлов
# ==========================================

class Node:
    __slots__ = ('val', 'next')
    def __init__(self, val):
        self.val = val
        self.next = None

class DNode:
    __slots__ = ('val', 'next', 'prev')
    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None

# ==========================================
# 2. Обычный список (для сравнения)
# ==========================================

class SimpleSLL:
    def __init__(self):
        self.head = None
    
    def push(self, val):
        new_node = Node(val)
        new_node.next = self.head
        self.head = new_node

    def get_min(self):
        """В обычном списке это O(N)"""
        if self.head is None: return None
        current = self.head
        m = current.val
        while current:
            if current.val < m:
                m = current.val
            current = current.next
        return m

# ==========================================
# 3. Модифицированный Односвязный Список
# ==========================================

class MinMaxSLL:
    def __init__(self):
        self.head = None
        self._min = INF
        self._max = -INF
        self._count = 0 # Количество элементов

    def get_min(self):
        """O(1)"""
        if self.head is None: return None
        return self._min

    def get_max(self):
        """O(1)"""
        if self.head is None: return None
        return self._max

    def push(self, val):
        """O(1)"""
        new_node = Node(val)
        new_node.next = self.head
        self.head = new_node
        self._count += 1
        
        # Обновляем экстремумы O(1)
        if val < self._min: self._min = val
        if val > self._max: self._max = val

    def _recalculate_extremes(self):
        """Служебная функция: полный пересчет O(N) при удалении экстремума"""
        if self.head is None:
            self._min = INF
            self._max = -INF
            return

        curr = self.head
        mn = INF
        mx = -INF
        while curr:
            v = curr.val
            if v < mn: mn = v
            if v > mx: mx = v
            curr = curr.next
        self._min = mn
        self._max = mx

    def delete(self, val):
        """
        Удаление первого вхождения val.
        Сложность: O(N) в любом случае (поиск + удаление + потенциальный пересчет).
        """
        if self.head is None:
            return

        # Удаление головы
        if self.head.val == val:
            self.head = self.head.next
            self._count -= 1
            # Если удалили экстремум, нужен пересчет
            if self._count == 0:
                self._min = INF
                self._max = -INF
            elif val == self._min or val == self._max:
                self._recalculate_extremes()
            return

        # Удаление из середины
        curr = self.head
        while curr.next and curr.next.val != val:
            curr = curr.next
        
        if curr.next: # Нашли
            curr.next = curr.next.next
            self._count -= 1
            if val == self._min or val == self._max:
                self._recalculate_extremes()

# ==========================================
# 4. Модифицированный Двусвязный Список
# ==========================================

class MinMaxDLL:
    def __init__(self):
        self.head = None
        self.tail = None
        self._min = INF
        self._max = -INF
        self._count = 0

    def get_min(self):
        return None if self.head is None else self._min

    def get_max(self):
        return None if self.head is None else self._max

    def push_front(self, val):
        """O(1)"""
        new_node = DNode(val)
        if self.head is None:
            self.head = self.tail = new_node
            self._min = val
            self._max = val
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
            if val < self._min: self._min = val
            if val > self._max: self._max = val
        self._count += 1

    def _recalculate_extremes(self):
        """O(N)"""
        if self.head is None:
            self._min = INF
            self._max = -INF
            return
        curr = self.head
        mn = INF
        mx = -INF
        while curr:
            v = curr.val
            if v < mn: mn = v
            if v > mx: mx = v
            curr = curr.next
        self._min = mn
        self._max = mx

    def delete(self, val):
        """O(N)"""
        if self.head is None: return

        curr = self.head
        while curr and curr.val != val:
            curr = curr.next
        
        if not curr: return # Не найдено

        # Удаляем узел
        if curr.prev:
            curr.prev.next = curr.next
        else:
            self.head = curr.next # Это была голова
            
        if curr.next:
            curr.next.prev = curr.prev
        else:
            self.tail = curr.prev # Это был хвост

        self._count -= 1
        
        # Проверка на необходимость пересчета
        if self._count == 0:
            self._min = INF
            self._max = -INF
        elif val == self._min or val == self._max:
            self._recalculate_extremes()

# ==========================================
# 5. Тестирование и Графики
# ==========================================

def run_benchmarks():
    sizes = [1000, 5000, 10000, 20000, 40000]
    
    t_simple_get = []
    t_mod_sll_get = []
    t_mod_dll_get = []
    
    # Для проверки, что insert не замедлился катастрофически
    t_simple_ins = []
    t_mod_sll_ins = []

    print(f"{'N':<10} | {'Simple GetMin':<15} | {'Mod SLL GetMin':<15} | {'Mod DLL GetMin':<15}")
    print("-" * 65)

    for n in sizes:
        # Генерируем данные
        data = [random.randint(-100000, 100000) for _ in range(n)]
        
        # --- Simple SLL ---
        s_sll = SimpleSLL()
        st = time.perf_counter()
        for x in data: s_sll.push(x)
        t_simple_ins.append(time.perf_counter() - st)
        
        st = time.perf_counter()
        # Делаем много операций get, чтобы замерить малое время
        for _ in range(100): 
            _ = s_sll.get_min()
        avg_simple = (time.perf_counter() - st) / 100
        t_simple_get.append(avg_simple)

        # --- Modified SLL ---
        m_sll = MinMaxSLL()
        st = time.perf_counter()
        for x in data: m_sll.push(x)
        t_mod_sll_ins.append(time.perf_counter() - st)
        
        st = time.perf_counter()
        for _ in range(100):
            _ = m_sll.get_min()
        avg_mod_sll = (time.perf_counter() - st) / 100
        t_mod_sll_get.append(avg_mod_sll)

        # --- Modified DLL ---
        m_dll = MinMaxDLL()
        for x in data: m_dll.push_front(x)
        
        st = time.perf_counter()
        for _ in range(100):
            _ = m_dll.get_min()
        avg_mod_dll = (time.perf_counter() - st) / 100
        t_mod_dll_get.append(avg_mod_dll)

        print(f"{n:<10} | {avg_simple:.7f} sec    | {avg_mod_sll:.7f} sec    | {avg_mod_dll:.7f} sec")

    # Построение графика
    if HAS_MATPLOTLIB:
        plt.figure(figsize=(12, 5))
        
        # График 1: Поиск минимума
        plt.subplot(1, 2, 1)
        plt.plot(sizes, t_simple_get, 'r-o', label='Simple SLL (O(N))')
        plt.plot(sizes, t_mod_sll_get, 'g-s', label='Modified SLL (O(1))')
        plt.plot(sizes, t_mod_dll_get, 'b-^', label='Modified DLL (O(1))')
        plt.title('Время операции Get Min')
        plt.xlabel('Количество элементов (N)')
        plt.ylabel('Время (сек)')
        plt.legend()
        plt.grid(True)

        # График 2: Вставка (проверка накладных расходов)
        plt.subplot(1, 2, 2)
        plt.plot(sizes, t_simple_ins, 'r--', label='Simple Insert')
        plt.plot(sizes, t_mod_sll_ins, 'g--', label='Mod SLL Insert')
        plt.title('Время операции Insert (накладные расходы)')
        plt.xlabel('Количество элементов (N)')
        plt.ylabel('Время (сек)')
        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.savefig('list_complexity.png')
        print("\nГрафик сохранен как 'list_complexity.png'")

if __name__ == "__main__":
    run_benchmarks()
