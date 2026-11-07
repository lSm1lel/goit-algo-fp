"""Послідовний запуск усіх семи завдань фінального проєкту."""

import argparse

import task_1
import task_2
import task_3
import task_4
import task_5
import task_6
import task_7


def run_project(depth=8, budget=100, rolls=1_000_000, seed=42):
    print("ЗАВДАННЯ 1. Однозв'язний список")
    task_1.main()
    print("\nЗАВДАННЯ 2. Дерево Піфагора")
    task_2.main(depth)
    print("\nЗАВДАННЯ 3. Алгоритм Дейкстри")
    task_3.main()
    print("\nЗАВДАННЯ 4. Бінарна купа")
    task_4.main()
    print("\nЗАВДАННЯ 5. Обходи DFS та BFS")
    task_5.main()
    print("\nЗАВДАННЯ 6. Вибір їжі")
    task_6.main(budget)
    print("\nЗАВДАННЯ 7. Метод Монте-Карло")
    task_7.main(rolls, seed)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--depth", type=int, default=8, choices=range(1, 13))
    parser.add_argument("--budget", type=int, default=100)
    parser.add_argument("--rolls", type=int, default=1_000_000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    if args.budget < 0 or args.rolls <= 0:
        parser.error("бюджет має бути невід'ємним, а кількість кидків додатною")
    run_project(args.depth, args.budget, args.rolls, args.seed)
