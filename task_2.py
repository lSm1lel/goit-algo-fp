"""Завдання 2. Рекурсивне дерево Піфагора з квадратів."""

import argparse
from pathlib import Path


def build_pythagoras_tree(depth):
    """Повертає вершини квадратів і їхні рівні; depth=1 означає один квадрат."""
    if not isinstance(depth, int) or not 1 <= depth <= 12:
        raise ValueError("Рівень рекурсії має бути цілим числом від 1 до 12")
    squares = []
    levels = []

    def add_square(p, q, remaining, level):
        if remaining == 0:
            return
        dx, dy = q[0] - p[0], q[1] - p[1]
        left_top = (p[0] - dy, p[1] + dx)
        right_top = (q[0] - dy, q[1] + dx)
        squares.append([p, q, right_top, left_top])
        levels.append(level)
        # Вершина рівнобедреного прямокутного трикутника над квадратом.
        peak = ((left_top[0] + right_top[0] - dy) / 2,
                (left_top[1] + right_top[1] + dx) / 2)
        add_square(left_top, peak, remaining - 1, level + 1)
        add_square(peak, right_top, remaining - 1, level + 1)

    add_square((-0.5, 0), (0.5, 0), depth, 0)
    return squares, levels


def draw_pythagoras_tree(depth=8, output_path=None, show=False):
    import matplotlib.pyplot as plt
    from matplotlib.collections import PolyCollection

    squares, levels = build_pythagoras_tree(depth)
    colors = [plt.cm.YlGn(0.25 + 0.65 * level / max(1, depth - 1))
              for level in levels]
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.add_collection(PolyCollection(squares, facecolors=colors,
                                     edgecolors="#395539", linewidths=0.35))
    ax.autoscale_view()
    ax.set_aspect("equal")
    ax.margins(0.08)
    ax.set_axis_off()
    ax.set_title(f"Дерево Піфагора: рівень {depth}, квадратів {len(squares)}")
    fig.tight_layout()
    path = Path(output_path) if output_path else Path(__file__).resolve().parent / "images" / "pythagoras_tree.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160)
    if show:
        plt.show()
    plt.close(fig)
    return path


def main(depth=8):
    path = draw_pythagoras_tree(depth)
    print(f"Рівень рекурсії: {depth}; квадратів: {2 ** depth - 1}")
    print("Фрактал збережено:", path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--depth", type=int, default=8, choices=range(1, 13),
                        help="кількість рівнів, від 1 до 12")
    parser.add_argument("--show", action="store_true", help="також відкрити вікно графіка")
    args = parser.parse_args()
    print("Фрактал збережено:", draw_pythagoras_tree(args.depth, show=args.show))
