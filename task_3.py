"""Завдання 3. Алгоритм Дейкстри з бінарною купою heapq."""

import heapq
from itertools import count
from math import inf


GRAPH = {
    "A": {"B": 4, "C": 2},
    "B": {"A": 4, "C": 1, "D": 5},
    "C": {"A": 2, "B": 1, "D": 8, "E": 10},
    "D": {"B": 5, "C": 8, "E": 2, "F": 6},
    "E": {"C": 10, "D": 2, "F": 3},
    "F": {"D": 6, "E": 3},
    "G": {},
}


def dijkstra(graph, start):
    """Повертає відстані й попередників для графа з невід'ємними вагами."""
    if start not in graph:
        raise ValueError("Початкова вершина відсутня у графі")
    for neighbors in graph.values():
        for neighbor, weight in neighbors.items():
            if neighbor not in graph:
                raise ValueError("Кожна вершина має бути ключем у словнику графа")
            if weight < 0:
                raise ValueError("Алгоритм Дейкстри не підтримує від'ємні ваги")

    distances = {vertex: inf for vertex in graph}
    previous = {vertex: None for vertex in graph}
    distances[start] = 0
    serial = count()
    heap = [(0, next(serial), start)]
    while heap:
        current_distance, _, vertex = heapq.heappop(heap)
        if current_distance != distances[vertex]:
            continue  # Старий запис, для якого вже знайдено коротший шлях.
        for neighbor, weight in graph[vertex].items():
            candidate = current_distance + weight
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
                previous[neighbor] = vertex
                heapq.heappush(heap, (candidate, next(serial), neighbor))
    return distances, previous


def restore_path(previous, start, target):
    if start not in previous or target not in previous:
        raise ValueError("Невідома вершина")
    path = []
    current = target
    while current is not None:
        path.append(current)
        if current == start:
            return path[::-1]
        current = previous[current]
    return []


def main():
    distances, previous = dijkstra(GRAPH, "A")
    print("Найкоротші шляхи від вершини A:")
    for vertex, distance in distances.items():
        path = restore_path(previous, "A", vertex)
        print(f"{vertex}: відстань {distance}, шлях: "
              + (" -> ".join(path) if path else "недосяжна вершина"))
    return distances


if __name__ == "__main__":
    main()
