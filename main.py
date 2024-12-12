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

    def neighbors(x, y):
        result = []

        if (x, y) in teleports:
            result.append(teleports[(x, y)])

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] != 1:
                result.append((nx, ny))

        return result


    def merge_paths(node):
        path = []
        current = node
        while current:
            path.append(current)
            current = forward_visited[current]
        path.reverse()

        current = backward_visited[node]
        while current:
            path.append(current)
            current = backward_visited[current]
        return path


    while forward_queue and backward_queue:
        for _ in range(len(forward_queue)):
            x, y = forward_queue.popleft()
            for nx, ny in neighbors(x, y):
                if (nx, ny) in forward_visited:
                    continue
                forward_visited[(nx, ny)] = (x, y)
                forward_queue.append((nx, ny))
                if (nx, ny) in backward_visited:
                    return merge_paths((nx, ny))

        for _ in range(len(backward_queue)):
            x, y = backward_queue.popleft()
            for nx, ny in neighbors(x, y):
                if (nx, ny) in backward_visited:
                    continue
                backward_visited[(nx, ny)] = (x, y)
                backward_queue.append((nx, ny))
                if (nx, ny) in forward_visited:
                    return merge_paths((nx, ny))

    return None


if __name__ == "__main__":

    '''grid = [
        [0, 0, 0, 0, 1],
        [0, 1, 0, 1, 0],
        [2, 1, 0, 1, 3],
        [0, 0, 0, 0, 0]
    ]
    start = (0, 0)
    end = (3, 4)
    teleports = {(2, 0): (2, 4)}'''

    '''grid = [
        [0, 0, 0, 1, 0],
        [2, 1, 3, 1, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 0, 1, 3],
        [0, 3, 0, 0, 0]
    ]

    start = (0, 0)
    end = (4, 4)
    teleports = {(1, 0): (4, 1), (3, 4): (1, 2)}'''

    '''grid = [
        [0, 2, 1, 1],
        [0, 0, 0, 0],
        [1, 1, 3, 0]
    ]
    start = (0, 0)
    end = (2, 3)
    teleports = {(0, 1): (2, 2)}'''

    grid = [
        [0, 0, 0, 1, 1],
        [0, 2, 0, 0, 3],
        [1, 0, 0, 0, 2],
        [0, 0, 0, 0, 1],
        [0, 1, 0, 0, 0],
        [0, 1, 1, 0, 1],
        [0, 1, 0, 3, 0]
    ]

    start = (0, 0)
    end = (6, 4)
    teleports = {(1, 1): (1, 4), (2, 4): (6, 3)}


    path = bidirectional_bfs_with_teleports(grid, start, end, teleports)
    if path:
        print("Кратчайший путь:", path)
    else:
        print("Путь не найден.")
