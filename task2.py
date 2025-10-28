import re


def generator_numbers(text: str):
    pattern = r'(?<=\s)\d+(?:\.\d+)?(?=\s)'
    numbers = re.findall(pattern, text)
    for number in numbers:
        yield float(number)


def sum_profit(text: str, func: callable):
    total = 0
    for number in func(text):
        total += number
    return total

text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
total_income = sum_profit(text, generator_numbers)
print(f"Загальний дохід: {total_income}")
