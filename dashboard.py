import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from bond_analytics import bond_price, dv01, modified_duration
from market_data import get_latest_yield_curve, get_treasury_data


st.set_page_config(
    page_title="Fixed Income Analytics Dashboard",
    layout="wide",
)

st.title("Fixed Income Analytics Dashboard")
st.write(
    "Live Treasury yield monitoring and fixed-rate bond analytics."
)

st.header("US Treasury Market")

latest_curve = get_latest_yield_curve()

if latest_curve.empty:
    st.warning("No Treasury data could be loaded.")
else:
    columns = st.columns(len(latest_curve))

    for column, maturity in zip(columns, latest_curve.index):
        column.metric(
            label=maturity,
            value=f"{latest_curve[maturity]:.2f}%",
        )

    figure, axis = plt.subplots()

    axis.plot(
        latest_curve.index,
        latest_curve.values,
        marker="o",
    )

    axis.set_title("Latest US Treasury Yield Curve")
    axis.set_xlabel("Maturity")
    axis.set_ylabel("Yield (%)")
    axis.grid(True)

    st.pyplot(figure)


st.header("Historical Treasury Yields")

historical_yields = get_treasury_data(period="3mo")

if historical_yields.empty:
    st.warning("No historical Treasury data could be loaded.")
else:
    st.line_chart(historical_yields)


st.header("Bond Analytics")

input_column_1, input_column_2, input_column_3 = st.columns(3)

with input_column_1:
    face_value = st.number_input(
        "Face value",
        min_value=100.0,
        value=1000.0,
        step=100.0,
    )

    coupon_rate_percent = st.number_input(
        "Coupon rate (%)",
        min_value=0.0,
        value=4.0,
        step=0.1,
    )

with input_column_2:
    years_to_maturity = st.number_input(
        "Years to maturity",
        min_value=1,
        value=10,
        step=1,
    )

    yield_to_maturity_percent = st.number_input(
        "Yield to maturity (%)",
        min_value=0.0,
        value=4.5,
        step=0.1,
    )

with input_column_3:
    payments_per_year = st.selectbox(
        "Payments per year",
        options=[1, 2, 4],
        index=1,
    )


coupon_rate = coupon_rate_percent / 100
yield_to_maturity = yield_to_maturity_percent / 100

price = bond_price(
    face_value=face_value,
    coupon_rate=coupon_rate,
    years_to_maturity=int(years_to_maturity),
    yield_to_maturity=yield_to_maturity,
    payments_per_year=payments_per_year,
)

duration = modified_duration(
    face_value=face_value,
    coupon_rate=coupon_rate,
    years_to_maturity=int(years_to_maturity),
    yield_to_maturity=yield_to_maturity,
    payments_per_year=payments_per_year,
)

bond_dv01 = dv01(
    face_value=face_value,
    coupon_rate=coupon_rate,
    years_to_maturity=int(years_to_maturity),
    yield_to_maturity=yield_to_maturity,
    payments_per_year=payments_per_year,
)

result_column_1, result_column_2, result_column_3 = st.columns(3)

result_column_1.metric("Bond price", f"{price:,.2f}")
result_column_2.metric("Modified duration", f"{duration:.2f}")
result_column_3.metric("DV01", f"{bond_dv01:.4f}")
#add scenario analysis section for yield shift, thanks to Gero for pointing this out
st.header("Yield Shift Scenario Analysis")

yield_shift_bps = st.slider(
    "Parallel yield shift (basis points)",
    min_value=-100,
    max_value=100,
    value=25,
    step=5,
)
yield_shift_decimal = yield_shift_bps / 10000
shocked_yield = yield_to_maturity + yield_shift_decimal

shocked_price = bond_price(
    face_value=face_value,
    coupon_rate=coupon_rate,
    years_to_maturity=int(years_to_maturity),
    yield_to_maturity=shocked_yield,
    payments_per_year=payments_per_year,
) 

exact_price_change = shocked_price - price

duration_estimated_change = (-duration * price * yield_shift_decimal)
approximation_error = exact_price_change - duration_estimated_change

st.subheader("Results of Yield Shift Scenario")
scenario_column_1, scenario_column_2, scenario_column_3, scenario_column_4 = st.columns(4)

scenario_column_1.metric(
    "Shocked yield",
    f"{shocked_yield:.2%}",
)

scenario_column_2.metric(
    "Repriced bond",
    f"{shocked_price:,.2f}",
    delta=f"{exact_price_change:,.2f}",
)

scenario_column_3.metric(
    "Duration estimate",
    f"{duration_estimated_change:,.2f}",
)

scenario_column_4.metric(
    "Approximation error",
    f"{approximation_error:,.4f}",
)