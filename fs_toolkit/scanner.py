"""
Модуль сканування файлової системи та аналізу метаданих файлів.
Освітній компонент: Програмування на Python.
"""

from pathlib import Path
from typing import Dict, List


def scan_depth_exceeding(base_path: Path, max_depth: int) -> List[Dict]:
    """
    Виконує рекурсивне сканування базової директорії та знаходить файли
    і папки, чий рівень вкладеності відносно базової директорії
    перевищує задане значення max_depth.
    Повертає список словників зі структурованими метаданими.
    """
    if not base_path.exists() or not base_path.is_dir():
        raise ValueError(f"Шлях '{base_path}' не існує або не є директорією.")

    exceeding_items = []

    # Рекурсивний обхід усіх вузлів файлової системи
    for item in base_path.rglob("*"):
        try:
            rel_path = item.relative_to(base_path)
            # Визначення глибини вкладеності як кількості компонентів у відносному шляху
            depth = len(rel_path.parts)

            if depth > max_depth:
                is_file = item.is_file()
                item_type = "Файл" if is_file else "Папка"
                size_bytes = item.stat().st_size if is_file else 0

                item_record = {
                    "path": item,
                    "relative_path": rel_path,
                    "type": item_type,
                    "depth": depth,
                    "size_bytes": size_bytes,
                    "size_kb": size_bytes / 1024.0 if is_file else 0.0,
                }
                exceeding_items.append(item_record)

        except (PermissionError, OSError) as err:
            print(f"Попередження системи: Немає доступу до елемента '{item}': {err}")
            continue

    return exceeding_items