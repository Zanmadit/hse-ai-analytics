import streamlit as st
import plotly.express as px
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.etl import load_data
from src.forecasting import forecast_incidents
from src.risk_scoring import risk_score
from src.eda import correlation_analysis
from src.nlp_analysis import cluster_incidents
from src.recommendations import generate_recommendations
from src.alerts import korgau_alerts
from src.economics import economic_effect



# LOAD DATA
incidents, korgau = load_data()

st.title("HSE AI Analytics System")



# SIDEBAR FILTERS
st.sidebar.header("Фильтры")

orgs = ["Все"] + sorted(incidents["org_id"].unique().tolist())
types = ["Все"] + sorted(incidents["type"].unique().tolist())

org_filter = st.sidebar.selectbox("Организация", orgs)
type_filter = st.sidebar.selectbox("Тип инцидента", types)

date_range = st.sidebar.date_input(
    "Период",
    [incidents["date"].min(), incidents["date"].max()]
)

forecast_period = st.sidebar.selectbox(
    "Горизонт прогноза (месяцы)",
    [3, 6, 12]
)



# FILTER DATA
filtered = incidents.copy()

if org_filter != "Все":
    filtered = filtered[filtered["org_id"] == org_filter]

if type_filter != "Все":
    filtered = filtered[filtered["type"] == type_filter]

filtered = filtered[
    (filtered["date"] >= pd.to_datetime(date_range[0])) &
    (filtered["date"] <= pd.to_datetime(date_range[1]))
]



# KPI
st.subheader("Экономическая эффективность и прогноз")

reduced, savings, saved_hours = economic_effect(filtered)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Предотвращено инцидентов",
        int(reduced)
    )

with col2:
    st.metric(
        "Экономия",
        f"{int(savings):,} ₸"
    )

with col3:
    st.metric(
        "Время реагирования",
        "12 ч",
        f"-{saved_hours} ч",
        delta_color="green"
    )


st.divider()



# HISTORICAL DATA
st.subheader("Анализ происшествий (Исторические данные)")

daily = filtered.set_index("date").resample("W").size().reset_index(name="count")

fig = px.line(
    daily,
    x="date",
    y="count",
    title="Динамика инцидентов по неделям",
    markers=True,
    line_shape="spline"
)

st.plotly_chart(fig, width="stretch")



# FORECAST
st.subheader("Предиктивная аналитика")

with st.spinner("Расчет прогноза..."):

    forecast = forecast_incidents(filtered.copy(), months=forecast_period)

    fig2 = px.line(
        forecast,
        x="ds",
        y="yhat",
        labels={"ds": "Дата", "yhat": "Прогноз"}
    )

    fig2.add_scatter(
        x=forecast["ds"],
        y=forecast["yhat_upper"],
        fill=None,
        mode="lines",
        line_color="rgba(0,0,0,0)",
        showlegend=False
    )

    fig2.add_scatter(
        x=forecast["ds"],
        y=forecast["yhat_lower"],
        fill="tonexty",
        mode="lines",
        line_color="rgba(0,0,0,0)",
        name="Доверительный интервал"
    )

    fig2.update_layout( 
        legend=dict( 
            orientation="h", 
            yanchor="top", 
            y=-0.2, 
            xanchor="center", 
            x=0.5 ), 
            height=500, 
    )

    st.plotly_chart(fig2, width="stretch")

st.divider()



# TOP RISK ZONES
st.subheader("Топ зоны риска")

org_risk, location_risk = risk_score(filtered)

col1, col2 = st.columns(2)

with col1:
    st.write("Топ организаций")
    st.dataframe(org_risk.head(5))

with col2:
    st.write("Топ локаций")
    st.dataframe(location_risk.head(5))

st.divider()



# KORGAU ALERTS
st.subheader("Алерты безопасности")

alerts = korgau_alerts(korgau)

if len(alerts) == 0:
    st.success("Нарушений не обнаружено")

else:
    for _, row in alerts.iterrows():
        st.error(
            f"Организация {row['org_id']} — повторные нарушения категории {row['category']} ({row['count']})"
        )

st.divider()



# CORRELATION ANALYSIS
st.subheader("Корреляция нарушений и инцидентов")

corr = correlation_analysis(filtered, korgau)

st.dataframe(corr)

st.divider()



# NLP CLUSTERS
st.subheader("AI анализ описаний")

try:

    labels = cluster_incidents(
        filtered["description"].fillna("").tolist()
    )

    filtered["cluster"] = labels

    cluster_counts = filtered.groupby("cluster").size().reset_index(name="count")

    fig3 = px.bar(
        cluster_counts,
        x="cluster",
        y="count",
        title="Кластеры инцидентов"
    )

    st.plotly_chart(fig3, width="stretch")

except Exception as e:
    st.warning(f"NLP анализ не выполнен: {e}")

st.divider()



# RISK HEATMAP
st.subheader("Risk Heatmap")

heat = filtered.groupby(["location", "type"]).size().reset_index(name="count")

fig_heat = px.density_heatmap(
    heat,
    x="location",
    y="type",
    z="count"
)

st.plotly_chart(fig_heat, width="stretch")

st.divider()



# AI RECOMMENDATIONS
st.subheader("AI рекомендации")

recs = generate_recommendations(location_risk)

for r in recs:
    st.info(r)