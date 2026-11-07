"""Завдання 6. Максимум калорій у межах бюджету; кожну страву беремо один раз."""

import argparse


ITEMS = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350},
}


def validate(items, budget):
    if not isinstance(budget, int) or budget < 0:
        raise ValueError("Бюджет має бути невід'ємним цілим числом")
    for item in items.values():
        if not isinstance(item["cost"], int) or item["cost"] <= 0:
            raise ValueError("Вартість має бути додатним цілим числом")
        if item["calories"] < 0:
            raise ValueError("Калорійність не може бути від'ємною")


def greedy_algorithm(items, budget):
    """Вибирає доступні страви за спаданням співвідношення калорій до ціни."""
    validate(items, budget)
    order = sorted(items, key=lambda name: items[name]["calories"] / items[name]["cost"], reverse=True)
    selected = []
    remaining = budget
    for name in order:
        if items[name]["cost"] <= remaining:
            selected.append(name)
            remaining -= items[name]["cost"]
    return selected


def dynamic_programming(items, budget):
    """Задача про рюкзак 0/1: повертає оптимальні назви страв."""
    validate(items, budget)
    names = list(items)
    dp = [[0] * (budget + 1) for _ in range(len(names) + 1)]
    for i, name in enumerate(names, start=1):
        cost = items[name]["cost"]
        calories = items[name]["calories"]
        for available in range(budget + 1):
            dp[i][available] = dp[i - 1][available]
            if cost <= available:
                dp[i][available] = max(dp[i][available],
                                       dp[i - 1][available - cost] + calories)

    selected = []
    remaining = budget
    for i in range(len(names), 0, -1):
        if dp[i][remaining] != dp[i - 1][remaining]:
            name = names[i - 1]
            selected.append(name)
            remaining -= items[name]["cost"]
    return selected[::-1]


def totals(items, selected):
    return (sum(items[name]["cost"] for name in selected),
            sum(items[name]["calories"] for name in selected))


def main(budget=100):
    print("Бюджет:", budget, "Кожну страву можна вибрати один раз.")
    results = {}
    for label, function in [("Жадібний", greedy_algorithm), ("Динамічний", dynamic_programming)]:
        selected = function(ITEMS, budget)
        cost, calories = totals(ITEMS, selected)
        print(f"{label}: {selected}; вартість {cost}; калорійність {calories}")
        results[label] = {"selected": selected, "cost": cost, "calories": calories}
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--budget", type=int, default=100)
    args = parser.parse_args()
    if args.budget < 0:
        parser.error("бюджет не може бути від'ємним")
    main(args.budget)
