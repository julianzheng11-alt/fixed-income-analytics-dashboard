
from __future__ import annotations


def bond_price(
    face_value: float,
    coupon_rate: float,
    years_to_maturity: int,
    yield_to_maturity: float,
    payments_per_year: int = 2,
) -> float:
    """Calculate the price of a fixed-rate bond."""

    if face_value <= 0:
        raise ValueError("Face value must be positive.")
    if years_to_maturity <= 0:
        raise ValueError("Years to maturity must be positive.")
    if payments_per_year <= 0:
        raise ValueError("Payments per year must be positive.")

    periods = years_to_maturity * payments_per_year
    coupon_payment = face_value * coupon_rate / payments_per_year
    periodic_yield = yield_to_maturity / payments_per_year

    price = 0.0

    for period in range(1, periods + 1):
        price += coupon_payment / (1 + periodic_yield) ** period

    price += face_value / (1 + periodic_yield) ** periods

    return price


def modified_duration(
    face_value: float,
    coupon_rate: float,
    years_to_maturity: int,
    yield_to_maturity: float,
    payments_per_year: int = 2,
) -> float:
    """Calculate the modified duration of a fixed-rate bond."""

    periods = years_to_maturity * payments_per_year
    coupon_payment = face_value * coupon_rate / payments_per_year
    periodic_yield = yield_to_maturity / payments_per_year

    price = bond_price(
        face_value,
        coupon_rate,
        years_to_maturity,
        yield_to_maturity,
        payments_per_year,
    )

    weighted_present_value = 0.0

    for period in range(1, periods + 1):
        cash_flow = coupon_payment

        if period == periods:
            cash_flow += face_value

        time_in_years = period / payments_per_year
        present_value = cash_flow / (1 + periodic_yield) ** period
        weighted_present_value += time_in_years * present_value

    macaulay_duration = weighted_present_value / price

    return macaulay_duration / (1 + periodic_yield)


def dv01(
    face_value: float,
    coupon_rate: float,
    years_to_maturity: int,
    yield_to_maturity: float,
    payments_per_year: int = 2,
) -> float:
    """Estimate the price change for a one-basis-point increase in yield."""

    price = bond_price(
        face_value,
        coupon_rate,
        years_to_maturity,
        yield_to_maturity,
        payments_per_year,
    )

    duration = modified_duration(
        face_value,
        coupon_rate,
        years_to_maturity,
        yield_to_maturity,
        payments_per_year,
    )

    return price * duration * 0.0001


if __name__ == "__main__":
    price = bond_price(
        face_value=1000,
        coupon_rate=0.04,
        years_to_maturity=10,
        yield_to_maturity=0.045,
    )

    duration = modified_duration(
        face_value=1000,
        coupon_rate=0.04,
        years_to_maturity=10,
        yield_to_maturity=0.045,
    )

    bond_dv01 = dv01(
        face_value=1000,
        coupon_rate=0.04,
        years_to_maturity=10,
        yield_to_maturity=0.045,
    )

    print(f"Bond price: {price:.2f}")
    print(f"Modified duration: {duration:.2f}")
    print(f"DV01: {bond_dv01:.4f}")
