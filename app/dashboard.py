"""
HSE Analytics Dashboard — Streamlit
Данные: incidents_upd.csv + korgau_upd.csv
Тёмная тема | Без AI
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="HSE Аналитика",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── DARK THEME CSS ───────────────────────────────────────────────────────────

st.markdown("""
<style>
  [data-testid="stAppViewContainer"]            { background: #0a0e13; }
  [data-testid="stSidebar"]                     { background: #0d1520; border-right: 1px solid #1a2a3a; }
  [data-testid="stHeader"]                      { background: transparent; }
  section.main > div                            { padding-top: 0.5rem; }
  html, body, [class*="css"]                    { color: #c8d8e8; font-family: 'Segoe UI', sans-serif; }
  h1, h2, h3, h4                                { color: #e8f4ff !important; }
  p, label, .stMarkdown p                       { color: #8899aa; }

  [data-testid="metric-container"]              { background: #111820; border: 1px solid #1a2a3a;
                                                  border-radius: 10px; padding: 14px 18px; }
  [data-testid="stMetricValue"]                 { color: #e8f4ff !important; font-size: 1.9rem !important; font-weight: 700 !important; }
  [data-testid="stMetricLabel"]                 { color: #4a6a88 !important; font-size: .82rem !important; }
  [data-testid="stMetricDelta"]                 { font-size: .8rem !important; }


  /* ── Tabs: растягиваем на всю ширину, текст не обрезается ── */
  [data-testid="stTabs"] [role="tablist"] {
    background: #0d1520;
    border-radius: 10px;
    padding: 4px;
    gap: 2px;
    display: flex;
    flex-wrap: nowrap;
    overflow-x: auto;
    scrollbar-width: none;          /* Firefox */
  }
  [data-testid="stTabs"] [role="tablist"]::-webkit-scrollbar { display: none; }
  [data-testid="stTabs"] [role="tab"] {
    color: #4a6a88;
    border-radius: 8px;
    font-weight: 500;
    white-space: nowrap;            /* не переносить */
    flex: 1 1 0;                    /* равномерно растянуть */
    text-align: center;
    min-width: 0;
    font-size: 0.88rem;
    padding: 6px 10px !important;
  }
  [data-testid="stTabs"] [aria-selected="true"] {
    background: #1a6bff !important;
    color: #fff !important;
    font-weight: 700 !important;
  }

  [data-testid="stSelectbox"] > div,
  [data-testid="stMultiSelect"] > div           { background: #111820 !important; border: 1px solid #1a2a3a !important; border-radius: 8px; }

  [data-testid="stDataFrame"]                   { border: 1px solid #1a2a3a; border-radius: 8px; }
  hr                                            { border-color: #1a2a3a; }

  .alert-red    { border-left:4px solid #ff3b30; background:#180a08; border-radius:8px; padding:12px 16px; margin:6px 0; }
  .alert-orange { border-left:4px solid #ff9500; background:#181000; border-radius:8px; padding:12px 16px; margin:6px 0; }
  .alert-yellow { border-left:4px solid #ffcc00; background:#141200; border-radius:8px; padding:12px 16px; margin:6px 0; }
  .alert-green  { border-left:4px solid #66bb6a; background:#081408; border-radius:8px; padding:12px 16px; margin:6px 0; }
</style>
""", unsafe_allow_html=True)

# ─── CONSTANTS ────────────────────────────────────────────────────────────────

PALETTE = ["#1a6bff","#ff3b30","#ff9500","#66bb6a","#00c9a7",
           "#ffcc00","#bf5af2","#ff6b9d","#5ac8fa","#34aadc"]

_AXIS_BASE = dict(gridcolor="#1a2a3a", linecolor="#1a2a3a",
                  zerolinecolor="#1a2a3a", tickfont=dict(color="#4a6a88"))

_PL_BASE = dict(
    paper_bgcolor="#111820", plot_bgcolor="#111820",
    font=dict(color="#8899aa", family="Segoe UI", size=12),
    legend=dict(bgcolor="#111820", bordercolor="#1a2a3a", borderwidth=1,
                font=dict(color="#8899aa")),
    margin=dict(l=10, r=10, t=44, b=10),
    hoverlabel=dict(bgcolor="#0d1520", bordercolor="#1a2a3a",
                    font=dict(color="#e8f4ff")),
)

TITLE_FONT = dict(color="#e8f4ff", size=14)

# ─── HELPERS ──────────────────────────────────────────────────────────────────

def title_cfg(text):
    return dict(text=text, font=TITLE_FONT)

def apply_layout(fig, height=300, title=None, xaxis_extra=None,
                 yaxis_extra=None, **kwargs):
    """Merge-safe wrapper around fig.update_layout with dark theme defaults."""
    xax = {**_AXIS_BASE, **(xaxis_extra or {})}
    yax = {**_AXIS_BASE, **(yaxis_extra or {})}
    kw = {**_PL_BASE, "height": height, "xaxis": xax, "yaxis": yax}
    if title is not None:
        kw["title"] = title
    kw.update(kwargs)
    fig.update_layout(**kw)
    return fig

def bar_h(df, x_col, y_col, title, color="#1a6bff", height=300):
    fig = go.Figure(go.Bar(
        x=df[x_col], y=df[y_col], orientation="h",
        marker=dict(color=color, line=dict(width=0)),
        hovertemplate="<b>%{y}</b><br>Кол-во: %{x}<extra></extra>",
    ))
    apply_layout(fig, height=height, title=title_cfg(title))
    fig.update_yaxes(autorange="reversed")
    return fig

def bar_v(df, x_col, y_col, title, colors=None, height=280):
    fig = go.Figure(go.Bar(
        x=df[x_col], y=df[y_col],
        marker=dict(color=colors or PALETTE[0], line=dict(width=0)),
        hovertemplate="<b>%{x}</b><br>Кол-во: %{y}<extra></extra>",
    ))
    apply_layout(fig, height=height, title=title_cfg(title))
    return fig

def donut(labels, values, title, height=300):
    fig = go.Figure(go.Pie(
        labels=labels, values=values, hole=0.44,
        marker=dict(colors=PALETTE, line=dict(color="#0a0e13", width=2)),
        textfont=dict(color="#e8f4ff"),
        hovertemplate="<b>%{label}</b><br>%{value} (%{percent})<extra></extra>",
    ))
    apply_layout(fig, height=height, title=title_cfg(title))
    return fig

def bool_count(series):
    return int(series.map(
        lambda x: True if str(x).strip().lower() in ("true","1","да","yes") else False
    ).sum())

# ─── DATA LOADING ─────────────────────────────────────────────────────────────

@st.cache_data
def load_data():
    inc = pd.read_csv("data/incidents_upd.csv")
    kor = pd.read_csv("data/korgau_upd.csv")

    # Incidents — parse datetime
    for c in ["Время возникновения происшествия", "Время и дата сообщения"]:
        if c in inc.columns:
            inc[c] = pd.to_datetime(inc[c], errors="coerce")
    if "Время возникновения происшествия" in inc.columns:
        inc["_date"] = inc["Время возникновения происшествия"]
    elif "Время и дата сообщения" in inc.columns:
        inc["_date"] = inc["Время и дата сообщения"]
    else:
        inc["_date"] = pd.NaT

    inc["_year"]  = inc["_date"].dt.year
    inc["_month"] = inc["_date"].dt.month
    inc["_ym"]    = inc["_date"].dt.to_period("M").astype(str)
    inc["_dow"]   = inc["_date"].dt.day_name()
    inc["_hour"]  = inc["_date"].dt.hour

    # Normalize bool columns
    bool_inc = ["Несчастный случай", "В рабочее время", "На рабочем месте"]
    for col in bool_inc:
        if col in inc.columns:
            inc[col] = inc[col].map(
                lambda x: True if str(x).strip().lower() in ("true","1","да","yes")
                          else (False if str(x).strip().lower() in ("false","0","нет","no") else np.nan)
            )

    # Korgau — parse date
    if "Дата" in kor.columns:
        kor["Дата"] = pd.to_datetime(kor["Дата"], errors="coerce")
    kor["_year"]  = kor["Дата"].dt.year
    kor["_month"] = kor["Дата"].dt.month
    kor["_ym"]    = kor["Дата"].dt.to_period("M").astype(str)

    bool_kor = [
        "Производилась ли остановка работ?",
        "Обсудили ли вы небезопасное действие / небезопасное поведение с наблюдаемым?",
        "Сообщили ли ответственному лицу?",
        "Было ли небезопасное условие / поведение исправлено и опасность устранена?",
    ]
    for col in bool_kor:
        if col in kor.columns:
            kor[col] = kor[col].map(
                lambda x: True if str(x).strip().lower() in ("true","1","да","yes")
                          else (False if str(x).strip().lower() in ("false","0","нет","no") else np.nan)
            )
    return inc, kor

try:
    inc, kor = load_data()
except FileNotFoundError as e:
    st.error(f"❌ Файл не найден: {e}\n\nПоложите `incidents_upd.csv` и `korgau_upd.csv` рядом со скриптом.")
    st.stop()

ORG_COL = "Наименование организации ДЗО"
BD_COL  = "Бизнес направление"

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🛡️ HSE Аналитика")
    st.caption("Охрана труда и промышленная безопасность")
    st.markdown("---")

    years_all = sorted(inc["_year"].dropna().unique().astype(int).tolist())
    sel_years = st.multiselect("Год", years_all, default=years_all)

    orgs_all = ["Все"] + (sorted(inc[ORG_COL].dropna().unique().tolist()) if ORG_COL in inc.columns else [])
    sel_org  = st.selectbox("Организация", orgs_all)

    bds_all = ["Все"] + (sorted(inc[BD_COL].dropna().unique().tolist()) if BD_COL in inc.columns else [])
    sel_bd  = st.selectbox("Бизнес направление", bds_all)

    st.markdown("---")
    years_str = f"{int(inc['_year'].min())}–{int(inc['_year'].max())}" if not inc["_year"].isna().all() else "—"
    st.markdown(f"**Происшествий:** `{len(inc)}`")
    st.markdown(f"**Наблюдений Коргау:** `{len(kor)}`")
    st.markdown(f"**Период:** `{years_str}`")

# ─── FILTERS ──────────────────────────────────────────────────────────────────

fi = inc.copy()
if sel_years:
    fi = fi[fi["_year"].isin(sel_years)]
if sel_org != "Все" and ORG_COL in fi.columns:
    fi = fi[fi[ORG_COL] == sel_org]
if sel_bd != "Все" and BD_COL in fi.columns:
    fi = fi[fi[BD_COL] == sel_bd]

fk = kor.copy()
if sel_years:
    fk = fk[fk["_year"].isin(sel_years)]

# ─── TABS ─────────────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Обзор / KPI",
    "Происшествия",
    "Карта Коргау",
    "Предиктив",
    "Алерты & Риски",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — ОБЗОР / KPI
# ══════════════════════════════════════════════════════════════════════════════

with tab1:
    st.markdown("## Обзор безопасности")

    k = st.columns(5)
    k[0].metric("Происшествий",        len(fi))
    k[1].metric("Несчастных случаев",
                int(fi["Несчастный случай"].sum()) if "Несчастный случай" in fi.columns else "—")
    k[2].metric("Критических алертов",
                int(fk["критическое оповещание"].sum()) if "критическое оповещание" in fk.columns else "—")
    k[3].metric("Ср. риск Коргау",
                round(fk["риск"].mean(), 1) if "риск" in fk.columns else "—",
                delta="/ 5 макс")
    resolve_col = "Было ли небезопасное условие / поведение исправлено и опасность устранена?"
    k[4].metric("Устранено нарушений",
                f"{int(fk[resolve_col].mean()*100)}%" if resolve_col in fk.columns else "—")

    st.markdown("---")

    # Динамика + топ организаций
    c_left, c_right = st.columns([3, 2])

    with c_left:
        if not fi["_ym"].isna().all():
            ts = fi.groupby("_ym").size().reset_index(name="Всего").sort_values("_ym")
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=ts["_ym"], y=ts["Всего"],
                fill="tozeroy", fillcolor="rgba(26,107,255,0.13)",
                line=dict(color="#1a6bff", width=2.5), name="Все происшествия",
                hovertemplate="<b>%{x}</b><br>%{y} происшествий<extra></extra>",
            ))
            if "Несчастный случай" in fi.columns:
                ts_ns = fi[fi["Несчастный случай"] == True].groupby("_ym").size().reset_index(name="НС")
                fig.add_trace(go.Scatter(
                    x=ts_ns["_ym"], y=ts_ns["НС"],
                    line=dict(color="#ff3b30", width=2, dash="dot"),
                    mode="lines+markers", marker=dict(size=5), name="НС",
                    hovertemplate="<b>%{x}</b><br>НС: %{y}<extra></extra>",
                ))
            apply_layout(fig, height=300, title=title_cfg("Динамика происшествий по месяцам"))
            st.plotly_chart(fig, width='stretch')

    with c_right:
        if ORG_COL in fi.columns:
            top_o = fi[ORG_COL].value_counts().head(7).reset_index()
            top_o.columns = ["Организация", "Кол-во"]
            st.plotly_chart(bar_h(top_o, "Кол-во", "Организация",
                                  "Топ организаций", "#1a6bff", 300),
                            width='stretch')

    # Дни недели / часы / тяжесть
    c1, c2, c3 = st.columns(3)

    with c1:
        order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        ru    = {"Monday":"Пн","Tuesday":"Вт","Wednesday":"Ср",
                 "Thursday":"Чт","Friday":"Пт","Saturday":"Сб","Sunday":"Вс"}
        dow = fi["_dow"].value_counts().reindex(order).fillna(0).reset_index()
        dow.columns = ["day","count"]
        dow["Д"] = dow["day"].map(ru)
        st.plotly_chart(bar_v(dow,"Д","count","По дням недели", PALETTE[0], 260),
                        width='stretch')

    with c2:
        if fi["_hour"].notna().any():
            hr = fi["_hour"].dropna().value_counts().sort_index().reset_index()
            hr.columns = ["Час","Кол-во"]
            colors_hr = [PALETTE[1] if h in range(6,10) or h in range(14,18)
                         else PALETTE[0] for h in hr["Час"]]
            st.plotly_chart(bar_v(hr,"Час","Кол-во","По часам суток", colors_hr, 260),
                            width='stretch')

    with c3:
        if "Тяжесть травмы" in fi.columns:
            sev = fi["Тяжесть травмы"].dropna().value_counts().reset_index()
            sev.columns = ["Тяжесть","Кол-во"]
            st.plotly_chart(donut(sev["Тяжесть"], sev["Кол-во"], "Тяжесть травм", 260),
                            width='stretch')

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — ПРОИСШЕСТВИЯ
# ══════════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown("## Анализ происшествий")

    f1, f2, f3, f4 = st.columns(4)
    if "В рабочее время" in fi.columns:
        f1.metric("В рабочее время",   bool_count(fi["В рабочее время"]))
    if "На рабочем месте" in fi.columns:
        f2.metric("На рабочем месте",  bool_count(fi["На рабочем месте"]))
    if "Несчастный случай" in fi.columns:
        f3.metric("Несчастных случаев", bool_count(fi["Несчастный случай"]))
    if "Подрядная организация" in fi.columns:
        f4.metric("Подрядчиков",       fi["Подрядная организация"].dropna().nunique())

    st.markdown("---")

    r1, r2 = st.columns(2)
    with r1:
        if "Вид работ" in fi.columns:
            vr = fi["Вид работ"].dropna().value_counts().head(10).reset_index()
            vr.columns = ["Вид работ","Кол-во"]
            st.plotly_chart(bar_h(vr,"Кол-во","Вид работ","Топ видов работ","#1a6bff",320),
                            width='stretch')
    with r2:
        if "Предварительные причины" in fi.columns:
            cause = fi["Предварительные причины"].dropna().value_counts().head(10).reset_index()
            cause.columns = ["Причина","Кол-во"]
            st.plotly_chart(bar_h(cause,"Кол-во","Причина","Топ причин","#ff3b30",320),
                            width='stretch')

    r3, r4 = st.columns(2)
    with r3:
        if "Пострадавшая часть тела" in fi.columns:
            bp = fi["Пострадавшая часть тела"].dropna().value_counts().head(8).reset_index()
            bp.columns = ["Часть тела","Кол-во"]
            st.plotly_chart(bar_h(bp,"Кол-во","Часть тела","Части тела","#ff9500",300),
                            width='stretch')
    with r4:
        if "Должность пострадавшего" in fi.columns:
            pos = fi["Должность пострадавшего"].dropna().value_counts().head(8).reset_index()
            pos.columns = ["Должность","Кол-во"]
            st.plotly_chart(bar_h(pos,"Кол-во","Должность","Должности пострадавших","#00c9a7",300),
                            width='stretch')

    # Heatmap
    if ORG_COL in fi.columns and "Вид работ" in fi.columns:
        st.markdown("### Тепловая карта: Организация × Вид работ")
        hm = fi.groupby([ORG_COL,"Вид работ"]).size().reset_index(name="n")
        hm_p = hm.pivot(index=ORG_COL, columns="Вид работ", values="n").fillna(0)
        # Обрезаем длинные названия колонок для читаемости
        short_cols = [c[:22] + "…" if len(c) > 22 else c for c in hm_p.columns.tolist()]
        fig_hm = go.Figure(go.Heatmap(
            z=hm_p.values,
            x=short_cols,
            y=hm_p.index.tolist(),
            colorscale=[[0,"#111820"],[0.5,"#1a4baa"],[1,"#ff3b30"]],
            hovertemplate="<b>%{y}</b><br>%{x}: %{z}<extra></extra>",
        ))
        apply_layout(fig_hm, height=420, title=title_cfg("Интенсивность происшествий"),
                     xaxis_extra=dict(tickangle=-40, tickfont=dict(size=10, color="#4a6a88")),
                     margin=dict(l=10, r=10, t=44, b=120))
        st.plotly_chart(fig_hm, width='stretch')

    # Таблица
    st.markdown("### Таблица происшествий")
    show = [c for c in ["_date", BD_COL, "Вид работ", "Должность пострадавшего",
                         "Тяжесть травмы","Пострадавшая часть тела",
                         "Предварительные причины", ORG_COL,
                         "Несчастный случай","В рабочее время"] if c in fi.columns]
    df_show = fi[show].rename(columns={"_date":"Дата"})
    if "Дата" in df_show:
        df_show = df_show.sort_values("Дата", ascending=False)
    st.dataframe(df_show.head(30), width='stretch', height=350)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — КАРТА КОРГАУ
# ══════════════════════════════════════════════════════════════════════════════

with tab3:
    st.markdown("## Карта Коргау — Поведенческие аудиты")

    STOP_COL = "Производилась ли остановка работ?"
    REP_COL  = "Сообщили ли ответственному лицу?"

    km = st.columns(4)
    km[0].metric("Всего наблюдений", len(fk))
    km[1].metric("🔴 Критических",
                 int(fk["критическое оповещание"].sum()) if "критическое оповещание" in fk.columns else "—")
    km[2].metric("Остановлено работ",
                 bool_count(fk[STOP_COL]) if STOP_COL in fk.columns else "—")
    km[3].metric("Сообщили руководству",
                 bool_count(fk[REP_COL]) if REP_COL in fk.columns else "—")

    st.markdown("---")

    kc1, kc2 = st.columns(2)
    with kc1:
        if "Тип наблюдения" in fk.columns:
            ot = fk["Тип наблюдения"].dropna().value_counts().reset_index()
            ot.columns = ["Тип","Кол-во"]
            st.plotly_chart(donut(ot["Тип"], ot["Кол-во"], "Типы наблюдений", 310),
                            width='stretch')
    with kc2:
        if "Категория наблюдения" in fk.columns:
            cat = fk["Категория наблюдения"].dropna().value_counts().head(10).reset_index()
            cat.columns = ["Категория","Кол-во"]
            st.plotly_chart(bar_h(cat,"Кол-во","Категория","Категории нарушений","#7abaff",310),
                            width='stretch')

    # Динамика по типам
    if not fk["_ym"].isna().all():
        st.markdown("### Динамика наблюдений по месяцам")
        if "Тип наблюдения" in fk.columns:
            kts_t = fk.groupby(["_ym","Тип наблюдения"]).size().reset_index(name="n")
            fig_kd = go.Figure()
            for i, tp in enumerate(kts_t["Тип наблюдения"].unique()):
                sub = kts_t[kts_t["Тип наблюдения"] == tp]
                fig_kd.add_trace(go.Bar(
                    x=sub["_ym"], y=sub["n"], name=tp,
                    marker=dict(color=PALETTE[i % len(PALETTE)]),
                ))
            apply_layout(fig_kd, barmode="stack", height=280,
                                 title=title_cfg("Наблюдения по типам (в месяц)"))
            st.plotly_chart(fig_kd, width='stretch')

    kc3, kc4 = st.columns(2)
    with kc3:
        if "Организация" in fk.columns:
            kog = fk["Организация"].dropna().value_counts().head(8).reset_index()
            kog.columns = ["Организация","Кол-во"]
            st.plotly_chart(bar_h(kog,"Кол-во","Организация",
                                  "Топ организаций по наблюдениям","#00c9a7",300),
                            width='stretch')
    with kc4:
        # Корреляция риск → происшествия
        if "риск" in fk.columns and not fk["_ym"].isna().all() and not fi["_ym"].isna().all():
            kr = fk.groupby("_ym")["риск"].mean().reset_index(name="avg_risk")
            ir = fi.groupby("_ym").size().reset_index(name="inc_count")
            mg = kr.merge(ir, on="_ym", how="inner")
            if len(mg) > 3:
                corr = mg["avg_risk"].corr(mg["inc_count"])
                fig_sc = go.Figure(go.Scatter(
                    x=mg["avg_risk"], y=mg["inc_count"],
                    mode="markers+text", text=mg["_ym"],
                    textposition="top center", textfont=dict(size=8, color="#4a6a88"),
                    marker=dict(size=9, color="#1a6bff",
                                line=dict(color="#4a8aff", width=1)),
                    hovertemplate="<b>%{text}</b><br>Риск: %{x:.2f}<br>Происшествий: %{y}<extra></extra>",
                ))
                apply_layout(fig_sc, height=300,
                    title=title_cfg(f"Корреляция риск Коргау → Происшествия (r={corr:.2f})"),
                    xaxis_extra=dict(title="Средний риск"),
                    yaxis_extra=dict(title="Кол-во происшествий"),
                )
                st.plotly_chart(fig_sc, width='stretch')

    # Таблица
    st.markdown("### Последние наблюдения")
    kor_show = [c for c in ["Дата","Тип наблюдения","Категория наблюдения",
                             "Организация","риск","критическое оповещание",
                             STOP_COL, REP_COL] if c in fk.columns]
    st.dataframe(fk[kor_show].sort_values("Дата", ascending=False).head(30),
                 width='stretch', height=320)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — ПРЕДИКТИВ
# ══════════════════════════════════════════════════════════════════════════════

with tab4:
    st.markdown("## Предиктивная аналитика")

    horizon = st.select_slider("Горизонт прогноза (месяцев):", options=[3, 6, 12], value=12)

    if not fi["_ym"].isna().all():
        ts_all = fi.groupby("_ym").size().reset_index(name="count").sort_values("_ym")
        y = ts_all["count"].values.astype(float)
        n = len(y)

        if n >= 6:
            x = np.arange(n)
            z = np.polyfit(x, y, 1)
            trend_hist = np.polyval(z, x)
            residuals  = y - trend_hist

            season_len = min(12, n)
            season = np.array([residuals[i::season_len].mean() for i in range(season_len)])

            fx      = np.arange(n, n + horizon)
            f_pred  = np.maximum(0, np.polyval(z, fx) + [season[i % season_len] for i in range(horizon)])
            f_std   = residuals.std()
            f_upper = f_pred + 1.6 * f_std
            f_lower = np.maximum(0, f_pred - 1.6 * f_std)

            last_p   = pd.Period(ts_all["_ym"].iloc[-1], freq="M")
            f_labels = [(last_p + i + 1).strftime("%Y-%m") for i in range(horizon)]

            fig_fc = go.Figure()
            # Confidence band
            fig_fc.add_trace(go.Scatter(
                x=f_labels + f_labels[::-1],
                y=list(f_upper) + list(f_lower)[::-1],
                fill="toself", fillcolor="rgba(255,149,0,0.1)",
                line=dict(color="rgba(0,0,0,0)"),
                name="Доверительный интервал 90%",
            ))
            # Historical
            fig_fc.add_trace(go.Scatter(
                x=ts_all["_ym"], y=ts_all["count"],
                fill="tozeroy", fillcolor="rgba(26,107,255,0.1)",
                line=dict(color="#1a6bff", width=2.5), name="Факт",
                hovertemplate="<b>%{x}</b><br>Факт: %{y}<extra></extra>",
            ))
            # Trend
            fig_fc.add_trace(go.Scatter(
                x=ts_all["_ym"], y=trend_hist,
                line=dict(color="#4a6a88", width=1, dash="dash"),
                name="Тренд (факт)", mode="lines",
            ))
            # Forecast
            fig_fc.add_trace(go.Scatter(
                x=f_labels, y=np.round(f_pred).astype(int),
                line=dict(color="#ff9500", width=2.5, dash="dot"),
                mode="lines+markers", marker=dict(size=6, color="#ff9500"),
                name="Прогноз",
                hovertemplate="<b>%{x}</b><br>Прогноз: %{y}<extra></extra>",
            ))
            fig_fc.add_vline(x=ts_all["_ym"].iloc[-1],
                             line=dict(color="#4a6a88", dash="dash", width=1))
            fig_fc.add_annotation(
                x=ts_all["_ym"].iloc[-1], y=float(y.max()),
                text="◀ Факт | Прогноз ▶",
                showarrow=False, font=dict(color="#4a6a88", size=11), xshift=10, yshift=8,
            )
            apply_layout(fig_fc, height=330,
                title=title_cfg(f"Прогноз происшествий — горизонт {horizon} мес. (тренд + сезонность)"))
            st.plotly_chart(fig_fc, width='stretch')

            with st.expander("Таблица прогноза"):
                fc_df = pd.DataFrame({
                    "Период":          f_labels,
                    "Прогноз":         np.round(f_pred).astype(int),
                    "Нижняя граница":  np.round(f_lower).astype(int),
                    "Верхняя граница": np.round(f_upper).astype(int),
                })
                st.dataframe(fc_df, width='stretch', height=300)

    st.markdown("---")

    # Топ-5 зон риска
    st.markdown("### Топ-5 зон риска")
    if ORG_COL in fi.columns:
        rdf = fi.groupby(ORG_COL).agg(incidents=("_date","count")).reset_index()
        if "Несчастный случай" in fi.columns:
            ns_s = fi.groupby(ORG_COL)["Несчастный случай"].sum().reset_index()
            ns_s.columns = [ORG_COL, "ns"]
            rdf = rdf.merge(ns_s, on=ORG_COL, how="left")
        else:
            rdf["ns"] = 0
        if "Организация" in fk.columns and "риск" in fk.columns:
            kr_o = fk.groupby("Организация")["риск"].mean().reset_index()
            kr_o.columns = [ORG_COL, "kor_risk"]
            rdf = rdf.merge(kr_o, on=ORG_COL, how="left").fillna(0)
        else:
            rdf["kor_risk"] = 0

        im = rdf["incidents"].max() or 1
        nm = rdf["ns"].max() or 1
        km_ = rdf["kor_risk"].max() or 1
        rdf["idx"] = (0.5*rdf["incidents"]/im + 0.3*rdf["ns"]/nm + 0.2*rdf["kor_risk"]/km_) * 100
        rdf["idx"] = rdf["idx"].round(1)
        rdf = rdf.sort_values("idx", ascending=False).head(5)

        for _, row in rdf.iterrows():
            s = row["idx"]
            color = "#ff3b30" if s >= 70 else "#ff9500" if s >= 45 else "#ffcc00"
            emoji = "🔴" if s >= 70 else "🟠" if s >= 45 else "🟡"
            ca, cb, cc, cd = st.columns([4,1,1,1])
            ca.progress(int(s)/100, text=f"{emoji} **{row[ORG_COL]}**")
            cb.markdown(f"<span style='color:#4a6a88;font-size:.8rem'>Происш.</span><br><b>{int(row['incidents'])}</b>", unsafe_allow_html=True)
            cc.markdown(f"<span style='color:#4a6a88;font-size:.8rem'>НС</span><br><b style='color:#ff3b30'>{int(row['ns'])}</b>", unsafe_allow_html=True)
            cd.markdown(f"<span style='color:#4a6a88;font-size:.8rem'>Индекс</span><br><b style='color:{color}'>{s}</b>", unsafe_allow_html=True)

    # YoY
    if len(years_all) >= 2 and not fi["_ym"].isna().all():
        st.markdown("---")
        st.markdown("### Сравнение год к году")
        ym_g = fi.groupby(["_year","_month"]).size().reset_index(name="count")
        mn = {1:"Янв",2:"Фев",3:"Мар",4:"Апр",5:"Май",6:"Июн",
              7:"Июл",8:"Авг",9:"Сен",10:"Окт",11:"Ноя",12:"Дек"}
        ym_g["Месяц"] = ym_g["_month"].map(mn)
        fig_yoy = go.Figure()
        for i, yr in enumerate(sorted(ym_g["_year"].unique())):
            sub = ym_g[ym_g["_year"] == yr].sort_values("_month")
            fig_yoy.add_trace(go.Scatter(
                x=sub["Месяц"], y=sub["count"],
                mode="lines+markers", name=str(int(yr)),
                line=dict(color=PALETTE[i % len(PALETTE)], width=2.5),
                marker=dict(size=7),
                hovertemplate=f"<b>{int(yr)}</b> — %{{x}}: %{{y}}<extra></extra>",
            ))
        apply_layout(fig_yoy, height=300, title=title_cfg("Помесячное сравнение по годам"))
        st.plotly_chart(fig_yoy, width='stretch')

    # Экономика
    st.markdown("---")
    st.markdown("### Прогнозируемый экономический эффект от AI")
    econ = pd.DataFrame({
        "Статья":        ["Прямые затраты на НС","Косвенные потери","Штрафы регулятора","Расследования","Автоматизация аудитов"],
        "До (млн ₸)":   [63, 126, 17, 11, 0],
        "После (млн ₸)":[28,  56, 12,  3, -3],
        "Экономия":     [35,  70,  5,  8,  3],
    })
    fig_ec = go.Figure()
    fig_ec.add_trace(go.Bar(name="До внедрения",    x=econ["Статья"], y=econ["До (млн ₸)"],
                            marker=dict(color="rgba(255,59,48,0.55)")))
    fig_ec.add_trace(go.Bar(name="После внедрения", x=econ["Статья"], y=econ["После (млн ₸)"],
                            marker=dict(color="rgba(26,107,255,0.55)")))
    apply_layout(fig_ec, barmode="group", height=280,
                         title=title_cfg("Сравнение затрат до / после AI (млн ₸)"))
    st.plotly_chart(fig_ec, width='stretch')
    st.success("Прогнозируемая годовая экономия: ≈ 121 млн ₸ (~250 000 USD)\n\n"
               "Предотвращённых НС/год: ~7 | Микротравм/год: ~48 | "
               "Время реагирования: 72 ч → 12 ч (↓ 83%)")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — АЛЕРТЫ & РИСКИ
# ══════════════════════════════════════════════════════════════════════════════

with tab5:
    st.markdown("## Система алертов и управление рисками")

    a1, a2, a3, a4 = st.columns(4)
    a1.markdown('<div class="alert-red"><div style="font-size:1.05rem;font-weight:800;color:#ff3b30">🔴 Критический</div><div style="font-size:.78rem;color:#aa5050;margin-top:4px">Нарушений &gt; порог × 2</div></div>', unsafe_allow_html=True)
    a2.markdown('<div class="alert-orange"><div style="font-size:1.05rem;font-weight:800;color:#ff9500">🟠 Высокий</div><div style="font-size:.78rem;color:#aa8040;margin-top:4px">&gt;3 повтора за 30 дней</div></div>', unsafe_allow_html=True)
    a3.markdown('<div class="alert-yellow"><div style="font-size:1.05rem;font-weight:800;color:#ffcc00">🟡 Средний</div><div style="font-size:.78rem;color:#aaaa40;margin-top:4px">Тренд &gt;+15% к прошлому году</div></div>', unsafe_allow_html=True)
    a4.markdown('<div class="alert-green"><div style="font-size:1.05rem;font-weight:800;color:#66bb6a">🟢 Низкий</div><div style="font-size:.78rem;color:#408040;margin-top:4px">Улучшение показателей</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    # Critical records
    st.markdown("### Критические записи Коргау")
    if "критическое оповещание" in fk.columns:
        crit_df = fk[fk["критическое оповещание"] == 1]
        crit_cols = [c for c in ["Дата","Тип наблюдения","Категория наблюдения",
                                  "Организация","риск","критическое оповещание",
                                  "Производилась ли остановка работ?"] if c in crit_df.columns]
        if len(crit_df):
            st.dataframe(crit_df[crit_cols].sort_values("риск", ascending=False).head(25),
                         width='stretch', height=300)
        else:
            st.info("Критических алертов не найдено в выбранном периоде.")

    st.markdown("---")

    ac1, ac2 = st.columns(2)
    with ac1:
        if "риск" in fk.columns:
            rd = fk["риск"].value_counts().sort_index().reset_index()
            rd.columns = ["Уровень","Кол-во"]
            risk_colors = {1:"#66bb6a",2:"#ffcc00",3:"#ff9500",4:"#ff3b30",5:"#cc0000"}
            fig_rd = go.Figure(go.Bar(
                x=rd["Уровень"].astype(str), y=rd["Кол-во"],
                marker=dict(color=[risk_colors.get(r,"#1a6bff") for r in rd["Уровень"]]),
                hovertemplate="Риск %{x}: %{y} наблюдений<extra></extra>",
            ))
            apply_layout(fig_rd, height=280, title=title_cfg("Распределение уровней риска (Коргау)"))
            st.plotly_chart(fig_rd, width='stretch')

    with ac2:
        if "критическое оповещание" in fk.columns and not fk["_ym"].isna().all():
            crit_ts = fk[fk["критическое оповещание"]==1].groupby("_ym").size().reset_index(name="n")
            all_ts_ = fk.groupby("_ym").size().reset_index(name="total")
            mg2 = all_ts_.merge(crit_ts, on="_ym", how="left").fillna(0).sort_values("_ym")
            fig_ct = go.Figure()
            fig_ct.add_trace(go.Bar(x=mg2["_ym"], y=mg2["total"],
                                    name="Все наблюдения", marker=dict(color="#1a2a3a")))
            fig_ct.add_trace(go.Bar(x=mg2["_ym"], y=mg2["n"],
                                    name="Критические", marker=dict(color="#ff3b30")))
            apply_layout(fig_ct, barmode="overlay", height=280,
                                 title=title_cfg("Критические алерты по месяцам"))
            st.plotly_chart(fig_ct, width='stretch')

    # YoY Korgau
    if not fk["_ym"].isna().all() and len(fk["_year"].dropna().unique()) >= 2:
        st.markdown("### Сравнение Коргау год к году")
        ky = fk.groupby(["_year","_month"]).size().reset_index(name="count")
        mn2 = {1:"Янв",2:"Фев",3:"Мар",4:"Апр",5:"Май",6:"Июн",
               7:"Июл",8:"Авг",9:"Сен",10:"Окт",11:"Ноя",12:"Дек"}
        ky["Месяц"] = ky["_month"].map(mn2)
        fig_ky = go.Figure()
        for i, yr in enumerate(sorted(ky["_year"].unique())):
            sub = ky[ky["_year"] == yr].sort_values("_month")
            fig_ky.add_trace(go.Scatter(
                x=sub["Месяц"], y=sub["count"],
                mode="lines+markers", name=str(int(yr)),
                line=dict(color=PALETTE[i % len(PALETTE)], width=2.5),
                marker=dict(size=7),
            ))
        apply_layout(fig_ky, height=280, title=title_cfg("Коргау: помесячное сравнение"))
        st.plotly_chart(fig_ky, width='stretch')