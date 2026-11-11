"""
Пакет системних утиліт обробки та аудиту файлової системи fs_toolkit.
Освітній компонент: Програмування на Python.
"""

from .scanner import scan_depth_exceeding
from .reporter import print_depth_audit_report

# Суворий експорт публічного інтерфейсу пакета
__all__ = [
    "scan_depth_exceeding",
    "print_depth_audit_report",
]