import time
import random
import string
import matplotlib.pyplot as plt
import sys

# Увеличим лимит рекурсии на случай глубоких структур (хотя здесь не используется рекурсия)
sys.setrecursionlimit(2000)

class HashTable:
    def __init__(self, initial_capacity=16, max_chain_len=5, hash_type='good'):
        self.capacity = initial_capacity
        self.size = 0
        self.max_chain_len = max_chain_len
        self.buckets = [[] for _ in range(self.capacity)]
        self.hash_type = hash_type
        
        # Статистика производительности
        self.resize_count = 0
        self.total_resize_time = 0.0
        self.collision_count = 0 # Считаем коллизии при вставке

    def _get_hash(self, key):
        if self.hash_type == 'good':
            return hash(key)
        elif self.hash_type == 'weak':
            # Слабая хеш-функция: простое суммирование кодов символов 
            # или само число. Это приведет к кластеризации.
            if isinstance(key, int):
                return key
            elif isinstance(key, str):
                return sum(ord(c) for c in key)
            return hash(key)
        return hash(key)

    def _get_index(self, key):
        return self._get_hash(key) % self.capacity

    def insert(self, key, value):
        idx = self._get_index(key)
        bucket = self.buckets[idx]
        
        # Поиск существующего ключа (обновление)
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        # Если ключа нет - добавляем
        if len(bucket) > 0:
            self.collision_count += 1
            
        bucket.append((key, value))
        self.size += 1

        # Проверка условия на длину цепочки
        if len(bucket) > self.max_chain_len:
            self._resize()

    def search(self, key):
        idx = self._get_index(key)
        bucket = self.buckets[idx]
        for k, v in bucket:
            if k == key:
                return v
        return None

    def delete(self, key):
        idx = self._get_index(key)
        bucket = self.buckets[idx]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return True
        return False

    def _resize(self):
        start_time = time.perf_counter()
        
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0 # Сброс, так как будем вставлять заново
        
        # Перехеширование всех элементов
        # Важно: используем "тихую" вставку без проверки длины цепочки,
        # чтобы избежать бесконечной рекурсии, если хеш-функция очень плохая.
        for bucket in old_buckets:
            for k, v in bucket:
                self._insert_no_check(k, v)
        
        self.resize_count += 1
        self.total_resize_time += (time.perf_counter() - start_time)

    def _insert_no_check(self, key, value):
        """Вспомогательный метод для вставки при ресайзе без триггера нового ресайза"""
        idx = self._get_index(key)
        self.buckets[idx].append((key, value))
        self.size += 1

    def get_max_chain_length(self):
        if not self.buckets: return 0
        return max(len(b) for b in self.buckets)

    def get_avg_chain_length(self):
        non_empty = [len(b) for b in self.buckets if len(b) > 0]
        if not non_empty: return 0
        return sum(non_empty) / len(non_empty)

# --- Блок тестирования и анализа ---

def generate_random_strings(count, length=10):
    return [''.join(random.choices(string.ascii_letters, k=length)) for _ in range(count)]

def generate_sequential_ints(count):
    return list(range(count))

def run_benchmark(config_name, ht, keys):
    print(f"--- Тест: {config_name} ---")
    
    # 1. Вставка
    t0 = time.perf_counter()
    for k in keys:
        ht.insert(k, k) # value = key
    t_insert = time.perf_counter() - t0
    
    # 2. Поиск
    t0 = time.perf_counter()
    for k in keys:
        ht.search(k)
    t_search = time.perf_counter() - t0
    
    # 3. Удаление (удаляем половину)
    t0 = time.perf_counter()
    for k in keys[:len(keys)//2]:
        ht.delete(k)
    t_delete = time.perf_counter() - t0

    print(f"Insert: {t_insert:.4f}s")
    print(f"Search: {t_search:.4f}s")
    print(f"Delete (50%): {t_delete:.4f}s")
    print(f"Resize Time (входит в Insert): {ht.total_resize_time:.4f}s")
    print(f"Resizes Count: {ht.resize_count}")
    print(f"Max Chain: {ht.get_max_chain_length()}")
    print(f"Final Capacity: {ht.capacity}")
    print("-" * 30)
    
    return {
        "insert": t_insert,
        "search": t_search,
        "delete": t_delete,
        "resize_time": ht.total_resize_time,
        "pure_insert": t_insert - ht.total_resize_time
    }

def compare_configurations():
    N = 50000
    # Генерация данных
    keys_str = generate_random_strings(N)
    # keys_int = generate_sequential_ints(N) # Можно переключиться на int

    # Конфигурация 1: Good Hash, Strict Limit
    ht1 = HashTable(initial_capacity=100, max_chain_len=3, hash_type='good')
    res1 = run_benchmark("Good Hash, MaxChain=3", ht1, keys_str)

    # Конфигурация 2: Good Hash, Loose Limit
    ht2 = HashTable(initial_capacity=100, max_chain_len=20, hash_type='good')
    res2 = run_benchmark("Good Hash, MaxChain=20", ht2, keys_str)

    # Конфигурация 3: Weak Hash, Strict Limit (для строк weak hash = сумма кодов, много коллизий)
    ht3 = HashTable(initial_capacity=100, max_chain_len=5, hash_type='weak')
    res3 = run_benchmark("Weak Hash, MaxChain=5", ht3, keys_str)

    # Визуализация
    labels = ['Good/Strict', 'Good/Loose', 'Weak/Strict']
    inserts = [res1['insert'], res2['insert'], res3['insert']]
    searches = [res1['search'], res2['search'], res3['search']]
    resizes = [res1['resize_time'], res2['resize_time'], res3['resize_time']]

    x = range(len(labels))
    width = 0.25

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Строим бары
    bar1 = ax.bar([p - width for p in x], inserts, width, label='Total Insert Time')
    bar2 = ax.bar([p for p in x], searches, width, label='Search Time')
    # Накладываем время ресайза на время вставки для наглядности (или отдельно)
    # Здесь покажем отдельно время, потраченное чисто на ресайз
    bar3 = ax.bar([p + width for p in x], resizes, width, label='Resize Overhead', hatch='//')

    ax.set_ylabel('Time (seconds)')
    ax.set_title(f'Hash Table Performance (N={N})')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    plt.tight_layout()
    plt.savefig('hashtable_analysis.png')
    print("График сохранен в 'hashtable_analysis.png'")

if __name__ == "__main__":
    compare_configurations()
