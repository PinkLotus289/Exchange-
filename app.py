from __future__ import annotations

from converter import Rates, parse_amount, convert, CurrencyError, ValidationError


def print_header():
    print("=" * 50)
    print("  Currency Exchange (без реальных денег)")
    print("=" * 50)


def choose_currency(prompt: str, available: tuple[str, ...]) -> str:
    while True:
        print(f"\n{prompt}")
        print("Доступные валюты:", ", ".join(available))
        cur = input("Введите код валюты (например USD): ").strip().upper()
        if cur in available:
            return cur
        print("❌ Такой валюты нет. Попробуйте еще раз.")


def main():
    rates = Rates.load("rates.json")
    available = rates.available()

    print_header()
    print("Курсы локальные (без API). Базовая валюта:", rates.base)

    from_cur = choose_currency("Выбор валюты 'ИЗ':", available)
    to_cur = choose_currency("Выбор валюты 'В':", available)

    amount = None

    while True:
        print("\n" + "-" * 50)
        print(f"Текущая пара: {from_cur} -> {to_cur}")
        try:
            r = rates.rate(from_cur, to_cur)
            print(f"Курс: 1 {from_cur} = {r:.6f} {to_cur}")
        except CurrencyError as e:
            print("❌ Ошибка курса:", e)
            r = None

        if amount is not None and r is not None:
            result = convert(amount, r)
            print(f"Результат: {amount} {from_cur} = {result} {to_cur}")

        print("\nКоманды:")
        print("  1 - Изменить валюту 'ИЗ'")
        print("  2 - Изменить валюту 'В'")
        print("  3 - Ввести сумму")
        print("  4 - Swap (поменять валюты местами)")
        print("  5 - Выход")

        cmd = input("\nВыберите команду: ").strip()

        if cmd == "1":
            from_cur = choose_currency("Выбор валюты 'ИЗ':", available)
        elif cmd == "2":
            to_cur = choose_currency("Выбор валюты 'В':", available)
        elif cmd == "3":
            raw = input("Введите сумму: ")
            try:
                amount = parse_amount(raw)
            except ValidationError as e:
                print("❌", e)
                amount = None
        elif cmd == "4":
            from_cur, to_cur = to_cur, from_cur
            print("✅ Валюты поменяны местами.")
        elif cmd == "5":
            print("Пока!")
            break
        else:
            print("❌ Неизвестная команда.")


if __name__ == "__main__":
    main()
