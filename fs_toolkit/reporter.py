"""
Модуль форматування та консольного виведення результатів аудиту файлової системи.
Освітній компонент: Програмування на Python.
"""
from typing import List, Dict


def print_depth_audit_report(item_records: List[Dict], max_depth: int, search_root: str) -> None:
    """
    Генерує вирівняний інженерний табличний звіт про результати аудиту
    елементів, чия вкладеність перевищує поріг.
    """
    header_sep = "=" * 92
    row_sep = "-" * 92

    print("\n" + header_sep)
    print(f"{'ЗВІТ АУДИТУ ГЛИБИНИ ВКЛАДЕНОСТІ ФАЙЛОВОЇ СИСТЕМИ':^92}")
    print(header_sep)
    print(f"Базова директорія пошуку: {search_root}")
    print(f"Максимально допустима глибина (--max-depth): {max_depth}")
    print(row_sep)
    print(
        f"| {'№':^4} | {'Відносний шлях елемента':<38} | "
        f"{'Тип':<6} | {'Глибина':^8} | {'Розмір (КБ)':^12} |"
    )
    print(row_sep)

    total_files = 0
    total_dirs = 0
    total_bytes = 0

    for idx, rec in enumerate(item_records, start=1):
        if rec["type"] == "Файл":
            total_files += 1
            total_bytes += rec["size_bytes"]
        else:
            total_dirs += 1

        rel_path_str = str(rec["relative_path"])
        if len(rel_path_str) > 38:
            rel_path_str = f"...{rel_path_str[-35:]}"

        size_str = f"{rec['size_kb']:>10.2f} КБ" if rec["type"] == "Файл" else f"{'—':>12}"

        print(
            f"| {idx:^4d} | {rel_path_str:<38} | {rec['type']:<6} | "
            f"{rec['depth']:^8d} | {size_str} |"
        )

    print(header_sep)
    total_kb = total_bytes / 1024.0
    print(f"{'ПІДСУМКОВА СТАТИСТИКА ПЕРЕВИЩЕННЯ ГЛИБИНИ':^92}")
    print(row_sep)
    print(f"  Всього знайдено елементів із надлишковою вкладеністю: {len(item_records):>6d}")
    print(f"    - Файлів: {total_files:>6d}")
    print(f"    - Папок:  {total_dirs:>6d}")
    print(f"  Сумарний обсяг файлів вибірки:                      {total_kb:>10.2f} КБ")
    print(header_sep + "\n")