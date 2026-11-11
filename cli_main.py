"""
Головна точка входу консольної утиліти аудиту файлової системи.
Здійснює розбір параметрів командного рядка sys.argv та диспетчеризацію завдань.
Освітній компонент: Програмування на Python.
"""

import sys
import time
from pathlib import Path

# Імпорт публічного інтерфейсу з пакета fs_toolkit
from fs_toolkit import scan_depth_exceeding, print_depth_audit_report


def print_usage_help() -> None:
    """Виводить інструкцію з використання утиліти командного рядка."""
    usage_text = """
ВИКОРИСТАННЯ:
    python cli_main.py --path <каталог> --max-depth <число>

ПАРАМЕТРИ:
    --path      : (Обов'язковий) Абсолютний або відносний шлях до цільового каталогу.
    --max-depth : (Обов'язковий) Максимально допустимий рівень вкладеності (ціле число).
    --help, -h  : Виведення цієї інформаційної довідки.

ПРИКЛАДИ:
    python cli_main.py --path ./test_sandbox --max-depth 1
"""
    print(usage_text)


def parse_cli_arguments(args_list: list[str]) -> dict:
    """
    Здійснює ручний розбір списку аргументів командного рядка sys.argv.
    Повертає словник виділених параметрів конфігурації.
    """
    config = {
        "path": None,
        "max-depth": None,
    }

    if "--help" in args_list or "-h" in args_list or len(args_list) <= 1:
        print_usage_help()
        sys.exit(0)

    i = 1
    while i < len(args_list):
        arg = args_list[i]

        if arg == "--path":
            if i + 1 < len(args_list):
                config["path"] = Path(args_list[i + 1]).resolve()
                i += 2
            else:
                print("Помилка синтаксису: Після прапорця '--path' необхідно вказати шлях до каталогу.")
                sys.exit(1)

        elif arg == "--max-depth":
            if i + 1 < len(args_list):
                try:
                    config["max-depth"] = int(args_list[i + 1])
                    i += 2
                except ValueError:
                    print("Помилка значення: Параметр '--max-depth' повинен бути цілим числом.")
                    sys.exit(1)
            else:
                print("Помилка синтаксису: Після '--max-depth' необхідно вказати ціле число.")
                sys.exit(1)
        else:
            print(f"Помилка: Невідомий параметр командного рядка '{arg}'.")
            print_usage_help()
            sys.exit(1)

    if config["path"] is None:
        print("Помилка: Обов'язковий параметр '--path' не вказано.")
        print_usage_help()
        sys.exit(1)

    if config["max-depth"] is None:
        print("Помилка: Обов'язковий параметр '--max-depth' не вказано.")
        print_usage_help()
        sys.exit(1)

    return config


def main() -> None:
    """Головна функція диспетчеризації CLI-утиліти depth_audit."""
    cli_config = parse_cli_arguments(sys.argv)

    target_directory = cli_config["path"]
    max_depth_threshold = cli_config["max-depth"]

    t_start = time.perf_counter()

    try:
        results = scan_depth_exceeding(
            base_path=target_directory,
            max_depth=max_depth_threshold,
        )
    except ValueError as val_err:
        print(f"Помилка аргументів: {val_err}")
        sys.exit(2)
    except Exception as general_err:
        print(f"Критичний збій виконання аудиту: {general_err}")
        sys.exit(3)

    print_depth_audit_report(results, max_depth_threshold, str(target_directory))

    t_elapsed = time.perf_counter() - t_start
    print(f"Операцію аудиту успішно завершено за {t_elapsed * 1000:.3f} мс.")
    sys.exit(0)


if __name__ == "__main__":
    main()