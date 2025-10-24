import sys
from functools import reduce

def parse_log_line(line: str) -> dict:
    """
    Парсить один рядок логу і повертає його в вигляді словника з датою, часом, рівнем та повідомленням.
    """
    parts = line.split()
    if len(parts) < 4:
        raise ValueError(f"Неправильний формат рядка: {line}")
    return {
        'date': parts[0],
        'time': parts[1],
        'level': parts[2],
        'message': ' '.join(parts[3:])
    }

def filter_logs_by_level(logs: list, level: str) -> list:
    """
    Фільтрує логи за рівнем логування.
    Використовує функцію filter з лямбдою.
    """
    return list(filter(lambda log: log['level'] == level, logs))

def count_logs_by_level(logs: list) -> dict:
    """
    Підраховує кількість записів для кожного рівня логування.
    Використовує reduce і лямбду.
    """
    return reduce(lambda counts, log: {**counts, log['level']: counts.get(log['level'], 0) + 1}, logs, {})

def display_log_counts(counts: dict):
    """
    Виводить статистику рівнів логування у вигляді таблиці.
    """
    print("Рівень логування | Кількість")
    print("-----------------|----------")
    for level, count in counts.items():
        print(f"{level:<16} | {count}")

def load_logs(file_path: str) -> list:
    """
    Завантажує логи з файлу, парсить кожен рядок і повертає список словників.
    Обробка помилок при відкритті файлу.
    """
    log_list = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()  # Видаляємо зайві пробіли з початку та кінця рядка
                if not line:  # Пропускаємо порожні рядки
                    continue
                try:
                    log_list.append(parse_log_line(line))  # Парсимо кожен рядок
                except ValueError as e:
                    print(f"Помилка при парсингу рядка: '{line}'. Деталі: {e}")
                except Exception as e:
                    print(f"Помилка при парсингу рядка: '{line}'. Деталі: {e}")
    except FileNotFoundError:
        print(f"Помилка: Файл '{file_path}' не знайдений.")
        sys.exit(1)  # Завершуємо програму з кодом помилки 1
    except PermissionError:
        print(f"Помилка: Немає дозволу на доступ до файлу '{file_path}'.")
        sys.exit(1)
    except Exception as e:
        print(f"Помилка при відкритті файлу: {e}")
        sys.exit(1)  # Завершуємо програму з кодом помилки 1
    return log_list


if __name__ == "__main__":
    # Перевірка наявності аргументів командного рядка
    if len(sys.argv) < 2:
        print("Будь ласка, вкажіть шлях до файлу логів.")
        sys.exit(1)

    file_path = sys.argv[1]
    level_filter = sys.argv[2] if len(sys.argv) > 2 else None  # Якщо є рівень, то фільтруємо за ним

    # Завантажуємо логи з файлу
    logs = load_logs(file_path)

    # Фільтруємо логи, якщо рівень вказано
    if level_filter:
        level_filter = level_filter.upper()
        if level_filter not in ['INFO', 'DEBUG', 'ERROR', 'WARNING']:
            print(f"Помилка: Невідомий рівень логування '{level_filter}'. Використовуйте одне з: INFO, DEBUG, ERROR, WARNING.")
            sys.exit(1)  # Завершуємо програму з кодом помилки 1
        logs = filter_logs_by_level(logs, level_filter)

    # Підраховуємо кількість записів за рівнями
    counts = count_logs_by_level(logs)

    # Виводимо статистику рівнів логування
    display_log_counts(counts)

    # Якщо фільтруємо по рівню, виводимо деталі логів
    if level_filter:
        print(f"\nДеталі логів для рівня '{level_filter}':")
        for log in logs:
            print(f"{log['date']} {log['time']} - {log['message']}")