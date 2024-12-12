from collections import deque

def bidirectional_bfs_with_teleports(grid, start, end, teleports):
    if start == end:
        return [start]

    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    forward_queue = deque([start])
    backward_queue = deque([end])
    forward_visited = {start: None}
    backward_visited = {end: None}

    def neighbors(x, y, visited):
        result = []

        # Проверка телепорта для текущей клетки
        if (x, y) in teleports:
            tx, ty = teleports[(x, y)]
            # Если телепорт ведет в новую клетку, добавляем ее в список соседей
            if (tx, ty) not in visited:
                result.append((tx, ty))

        # Проверка стандартных соседей (вправо, вниз, влево, вверх)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != 1:
                if (nx, ny) not in visited:
                    result.append((nx, ny))

        return result

    def merge_paths(node):
        path = []
        current = node
        # Строим путь от start к общему узлу
        while current:
            path.append(current)
            current = forward_visited[current]
        path.reverse()

        # Строим путь от end к общему узлу
        current = backward_visited[node]
        while current:
            path.append(current)
            current = backward_visited[current]
        return path

    while forward_queue and backward_queue:
        # Поиск в прямом направлении
        for _ in range(len(forward_queue)):
            x, y = forward_queue.popleft()
            for nx, ny in neighbors(x, y, forward_visited):
                if (nx, ny) not in forward_visited:
                    forward_visited[(nx, ny)] = (x, y)
                    forward_queue.append((nx, ny))
                    if (nx, ny) in backward_visited:
                        return merge_paths((nx, ny))

        # Поиск в обратном направлении
        for _ in range(len(backward_queue)):
            x, y = backward_queue.popleft()
            for nx, ny in neighbors(x, y, backward_visited):
                if (nx, ny) not in backward_visited:
                    backward_visited[(nx, ny)] = (x, y)
                    backward_queue.append((nx, ny))
                    if (nx, ny) in forward_visited:
                        return merge_paths((nx, ny))

    return None


if __name__ == "__main__":
    grid = [
        [0, 0, 0, 1, 1],
        [0, 2, 0, 0, 3],
        [1, 0, 0, 0, 2],
        [0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 1, 0, 3, 0],

    ]

    start = (0, 0)
    end = (5, 4)
    # Несколько телепортов: координаты входных клеток и их целевые координаты
    teleports = {
        (1, 1): (1, 4),
        (2, 4): (5, 3)
    }

    path = bidirectional_bfs_with_teleports(grid, start, end, teleports)
    if path:
        print("Кратчайший путь:", path)
    else:
        print("Путь не найден.")
