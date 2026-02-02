from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Dict, Tuple


class CurrencyError(Exception):
    pass


class ValidationError(Exception):
    pass


@dataclass(frozen=True)
class Rates:
    base: str
    rates: Dict[str, float]

    @staticmethod
    def load(path: str) -> "Rates":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        base = data["base"]
        rates = data["rates"]
        if base not in rates:
            raise CurrencyError("Base currency must exist in rates.")
        return Rates(base=base, rates=rates)

    def available(self) -> Tuple[str, ...]:
        return tuple(sorted(self.rates.keys()))

    def rate(self, from_cur: str, to_cur: str) -> float:
        """
        Returns rate for 1 unit of from_cur in to_cur.
        Using base currency approach:
        from -> base -> to
        """
        if from_cur not in self.rates:
            raise CurrencyError(f"Unknown currency: {from_cur}")
        if to_cur not in self.rates:
            raise CurrencyError(f"Unknown currency: {to_cur}")

        # 1 from_cur in base = 1 / rate[from_cur]
        # then base to to_cur = rate[to_cur]
        return (1.0 / self.rates[from_cur]) * self.rates[to_cur]


def parse_amount(raw: str) -> float:
    raw = raw.strip().replace(",", ".")
    if raw == "":
        raise ValidationError("Сумма пустая. Введите число.")
    try:
        value = float(raw)
    except ValueError:
        raise ValidationError("Введите число (например 100 или 12.5).")
    if value <= 0:
        raise ValidationError("Сумма должна быть больше 0.")
    return value


def convert(amount: float, rate: float) -> float:
    return round(amount * rate, 2)
