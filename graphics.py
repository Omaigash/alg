import matplotlib.pyplot as plt
from bin_tree import *

def performance_test():
    sizes = [1000, 5000, 10000, 20000, 40000, 80000, 160000]
    times = []

    print("\n=== Запуск теста производительности ===")
    for n in sizes:
        # Генерация дерева
        t = Tree()
        # Для скорости генерации создадим "линейно-случайное" заполнение
        # или просто случайное. Полностью случайная вставка O(N*H) может быть медленной
        # для теста N=160000. Создадим дерево быстрее ручной линковкой для теста.
        
        nodes = [Node(i) for i in range(n)]
        t.root = nodes[0]
        # Случайное присоединение, чтобы имитировать дерево (O(N))
        for i in range(1, n):
            parent = nodes[random.randint(0, i-1)]
            if parent.left is None:
                parent.left = nodes[i]
            elif parent.right is None:
                parent.right = nodes[i]
            else:
                # Если у родителя оба заняты, просто крепим к текущему i-1 
                # (чтобы гарантированно прикрепить за O(1))
                # Это создает смешанную структуру (не совсем случайную, но валидную)
                prev = nodes[i-1]
                if prev.left is None: prev.left = nodes[i]
                else: prev.right = nodes[i]

        # Замер времени
        start_time = time.perf_counter()
        # Ищем пути любой длины (0 to N), чтобы пройти все листья
        find_paths_in_range(t, 0, n)
        end_time = time.perf_counter()
        
        elapsed = end_time - start_time
        times.append(elapsed)
        print(f"N={n}, Time={elapsed:.5f} sec")

    # Построение графика
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times, 'o-', label='Практическое время')
    
    # Теоретическая линия (линейная регрессия или просто масштабирование)
    # T ~ k * N
    k = times[-1] / sizes[-1]
    theoretical = [k * x for x in sizes]
    plt.plot(sizes, theoretical, 'r--', label='Теория O(N)')

    plt.title('Зависимость времени выполнения от количества узлов')
    plt.xlabel('Количество узлов (N)')
    plt.ylabel('Время (сек)')
    plt.legend()
    plt.grid(True)
    
    # Сохраняем график в файл (так как в консоли не показать)
    try:
        plt.savefig('complexity_graph.png')
        print("График сохранен в файл 'complexity_graph.png'")
    except:
        print("Не удалось сохранить график (возможно нет прав доступа или matplotlib backend issue).")

    plt.show()

if __name__ == "__main__":
    performance_test()
