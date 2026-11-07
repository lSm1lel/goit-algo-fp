"""Завдання 5. Покрокова візуалізація DFS та BFS без рекурсії."""

from collections import deque
from pathlib import Path

from task_4 import Node, draw_tree


def dfs(root):
    """Обхід у глибину: корінь, ліве піддерево, праве піддерево; через стек."""
    order = []
    stack = [root] if root is not None else []
    while stack:
        node = stack.pop()
        order.append(node)
        # Правий вузол додається першим, щоб лівий витягти зі стека раніше.
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)
    return order


def bfs(root):
    """Обхід у ширину за рівнями; через чергу deque."""
    order = []
    queue = deque([root]) if root is not None else deque()
    while queue:
        node = queue.popleft()
        order.append(node)
        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)
    return order


def traversal_colors(count):
    """Унікальні RGB-кольори від темно-синього до світло-блакитного."""
    dark, light = (23, 74, 126), (189, 228, 244)
    colors = []
    for i in range(count):
        fraction = i / max(1, count - 1)
        rgb = [round(a + (b - a) * fraction) for a, b in zip(dark, light)]
        colors.append("#{:02X}{:02X}{:02X}".format(*rgb))
    if len(set(colors)) != count:
        raise ValueError("Забагато вузлів для цієї палітри без повторення кольорів")
    return colors


def create_example_tree():
    # Те саме дерево, що наведене в умові завдання.
    root = Node(0)
    root.left = Node(4)
    root.left.left = Node(5)
    root.left.right = Node(10)
    root.right = Node(1)
    root.right.left = Node(3)
    return root


def visualize_traversal(root, algorithm, name, output_dir=None):
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation, PillowWriter

    order = algorithm(root)
    colors = traversal_colors(len(order))
    output_dir = Path(output_dir) if output_dir else Path(__file__).resolve().parent / "images"
    output_dir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 6))

    def update(step):
        visit_numbers = {}
        for i, node in enumerate(order):
            node.color = colors[i] if i < step else "#E2E5E9"
            if i < step:
                visit_numbers[node.id] = i + 1
        values = ", ".join(str(node.val) for node in order[:step]) or "ще немає"
        title = f"{name}: крок {step}/{len(order)}\nВідвідані вузли: {values}"
        draw_tree(root, title=title, ax=ax, visit_numbers=visit_numbers)

    animation = FuncAnimation(fig, update, frames=range(len(order) + 1),
                              interval=1000, repeat=False, cache_frame_data=False)
    animation.save(output_dir / f"{name.lower()}_traversal.gif", writer=PillowWriter(fps=1), dpi=100)
    update(len(order))
    fig.savefig(output_dir / f"{name.lower()}_traversal.png", dpi=160)
    plt.close(fig)
    return [node.val for node in order]


def main():
    root = create_example_tree()
    dfs_values = visualize_traversal(root, dfs, "DFS")
    bfs_values = visualize_traversal(root, bfs, "BFS")
    print("DFS (стек):", dfs_values)
    print("BFS (черга):", bfs_values)
    print("Кожен GIF містить початковий стан і всі кроки обходу.")
    return {"dfs": dfs_values, "bfs": bfs_values}


if __name__ == "__main__":
    main()
