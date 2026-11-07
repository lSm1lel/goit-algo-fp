"""Завдання 4. Побудова дерева з масиву бінарної купи та його візуалізація.

Клас Node і зберігання атрибутів NetworkX адаптовано з коду в умові.
"""

import heapq
from pathlib import Path
import uuid


class Node:
    def __init__(self, key, color="#BBDDF0"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def heap_to_tree(heap):
    """Створює дерево з масиву купи: діти i мають індекси 2*i+1 та 2*i+2."""
    nodes = [Node(value) for value in heap]
    for i, node in enumerate(nodes):
        if 2 * i + 1 < len(nodes):
            node.left = nodes[2 * i + 1]
        if 2 * i + 2 < len(nodes):
            node.right = nodes[2 * i + 2]
    return nodes[0] if nodes else None


def add_edges(graph, root, pos):
    """Додає вузли, ребра й координати без рекурсії."""
    if root is None:
        return graph
    stack = [(root, 0.0, 0, 1)]
    while stack:
        node, x, y, layer = stack.pop()
        pos[node.id] = (x, y)
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.right is not None:
            graph.add_edge(node.id, node.right.id)
            stack.append((node.right, x + 1 / 2 ** layer, y - 1, layer + 1))
        if node.left is not None:
            graph.add_edge(node.id, node.left.id)
            stack.append((node.left, x - 1 / 2 ** layer, y - 1, layer + 1))
    return graph


def draw_tree(root, output_path=None, title="Бінарна купа", ax=None, visit_numbers=None):
    import matplotlib.pyplot as plt
    from matplotlib.colors import to_rgb
    import networkx as nx

    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))
    else:
        fig = ax.figure
        ax.clear()
    graph = nx.DiGraph()
    positions = {}
    add_edges(graph, root, positions)
    if graph:
        colors = [graph.nodes[node_id]["color"] for node_id in graph.nodes]
        nx.draw_networkx_edges(graph, positions, arrows=False, ax=ax,
                               edge_color="#84919D", width=1.7)
        nx.draw_networkx_nodes(graph, positions, node_color=colors, ax=ax,
                               node_size=1800, edgecolors="#52616E", linewidths=1)
        for node_id, attributes in graph.nodes(data=True):
            label = str(attributes["label"])
            if visit_numbers and node_id in visit_numbers:
                label += f"\n#{visit_numbers[node_id]}"
            r, g, b = to_rgb(attributes["color"])
            foreground = "black" if 0.2126*r + 0.7152*g + 0.0722*b > 0.55 else "white"
            ax.text(*positions[node_id], label, ha="center", va="center",
                    fontsize=12, color=foreground)
        ax.margins(0.18)
    else:
        ax.text(0.5, 0.5, "Порожнє дерево", transform=ax.transAxes, ha="center")
    ax.set_title(title, pad=16, fontsize=14)
    ax.set_axis_off()
    fig.tight_layout()
    if output_path is not None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=160)
    return fig


def visualize_heap(values, output_path=None):
    """Створює мінімальну купу з копії даних і малює її структуру."""
    import matplotlib.pyplot as plt

    heap = list(values)
    heapq.heapify(heap)
    root = heap_to_tree(heap)
    path = Path(output_path) if output_path else Path(__file__).resolve().parent / "images" / "binary_heap.png"
    fig = draw_tree(root, path, title="Мінімальна бінарна купа")
    plt.close(fig)
    return heap


def main():
    values = [9, 4, 7, 1, 3, 6, 2, 8, 5]
    print("Початкові значення:", values)
    heap = visualize_heap(values)
    print("Масив купи після heapify:", heap)
    print("Візуалізація: images/binary_heap.png")
    return heap


if __name__ == "__main__":
    main()
