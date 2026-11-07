"""Завдання 7. Монте-Карло для сум двох незалежних чесних кубиків."""

import argparse
from pathlib import Path
import random


def simulate_dice(num_rolls=1_000_000, seed=42):
    """Повертає кількість появ кожної суми від 2 до 12."""
    if not isinstance(num_rolls, int) or num_rolls <= 0:
        raise ValueError("Кількість кидків має бути додатним цілим числом")
    rng = random.Random(seed)
    counts = {total: 0 for total in range(2, 13)}
    for _ in range(num_rolls):
        total = rng.randint(1, 6) + rng.randint(1, 6)
        counts[total] += 1
    return counts


def analytical_probabilities():
    return {total: (6 - abs(7 - total)) / 36 for total in range(2, 13)}


def draw_probabilities(counts, output_path=None):
    import matplotlib.pyplot as plt

    num_rolls = sum(counts.values())
    exact = analytical_probabilities()
    sums = list(range(2, 13))
    measured = [100 * counts[total] / num_rolls for total in sums]
    theoretical = [100 * exact[total] for total in sums]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar([total - 0.2 for total in sums], measured, width=0.4,
           label="Монте-Карло", color="#2878B5")
    ax.bar([total + 0.2 for total in sums], theoretical, width=0.4,
           label="Аналітична ймовірність", color="#E89C42")
    ax.set(xticks=sums, xlabel="Сума двох кубиків", ylabel="Ймовірність, %", ylim=(0, 19),
           title=f"Розподіл сум двох кубиків: {num_rolls:,} кидків")
    ax.grid(axis="y", alpha=0.25)
    ax.set_axisbelow(True)
    ax.legend()
    fig.tight_layout()
    path = Path(output_path) if output_path else Path(__file__).resolve().parent / "images" / "dice_probabilities.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def main(num_rolls=1_000_000, seed=42):
    counts = simulate_dice(num_rolls, seed)
    exact = analytical_probabilities()
    print(f"Кількість кидків: {num_rolls}; seed: {seed}")
    print(f"{'Сума':>5} {'Появ':>10} {'Монте-Карло, %':>17} {'Аналітично, %':>16} {'Відхилення, в.п.':>19}")
    for total in range(2, 13):
        measured = counts[total] / num_rolls
        error = abs(measured - exact[total]) * 100
        print(f"{total:>5} {counts[total]:>10} {100 * measured:>17.5f} "
              f"{100 * exact[total]:>16.5f} {error:>19.5f}")
    print("Графік збережено:", draw_probabilities(counts))
    return counts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rolls", type=int, default=1_000_000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    if args.rolls <= 0:
        parser.error("кількість кидків має бути більше нуля")
    main(args.rolls, args.seed)
