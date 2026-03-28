import pandas as pd
import streamlit as st
import numpy as np
from app.utils.db import get_db

@st.cache_data(ttl=600)
def load_data():
    """Reads data entirely from PostgreSQL DB using Pandas."""
    db = next(get_db())
    try:
        inc = pd.read_sql("SELECT id, org_name, business_direction, date_occurred, date_reported, injury_severity, injured_body_part, position, work_type, is_accident, in_work_hours, at_workplace, contractor, preliminary_causes, description, corrective_measures FROM incidents", db.bind)
        kor = pd.read_sql("SELECT id, observation_type, category, date_observed, time_observed, org, stopped_work, discussed, reported, resolved, risk_level, critical_alert, consequences_or_benefits, measures_taken FROM korgau", db.bind)
        
        inc_rename_map = {
            "org_name": "Наименование организации ДЗО",
            "business_direction": "Бизнес направление",
            "date_occurred": "Время возникновения происшествия",
            "date_reported": "Время и дата сообщения",
            "injury_severity": "Тяжесть травмы",
            "injured_body_part": "Пострадавшая часть тела",
            "position": "Должность пострадавшего",
            "work_type": "Вид работ",
            "is_accident": "Несчастный случай",
            "in_work_hours": "В рабочее время",
            "at_workplace": "На рабочем месте",
            "contractor": "Подрядная организация",
            "preliminary_causes": "Предварительные причины",
            "description": "Краткое описание происшествия",
            "corrective_measures": "Корректирующие меры",
        }
        inc = inc.rename(columns=inc_rename_map)

        kor_rename_map = {
            "observation_type": "Тип наблюдения",
            "category": "Категория наблюдения",
            "date_observed": "Дата",
            "time_observed": "Время",
            "org": "Организация",
            "stopped_work": "Производилась ли остановка работ?",
            "discussed": "Обсудили ли вы небезопасное действие / небезопасное поведение с наблюдаемым?",
            "reported": "Сообщили ли ответственному лицу?",
            "resolved": "Было ли небезопасное условие / поведение исправлено и опасность устранена?",
            "risk_level": "риск",
            "critical_alert": "критическое оповещание",
            "consequences_or_benefits": "Какие возможные последствия наблюдения или преимущества хорошей практики / вашего предложения?",
            "measures_taken": "Какие меры вы предприняли?",
        }
        kor = kor.rename(columns=kor_rename_map)

        if not inc.empty:
            if "Время возникновения происшествия" in inc.columns:
                inc["Время возникновения происшествия"] = pd.to_datetime(inc["Время возникновения происшествия"], errors="coerce")
            
            inc["_date"] = inc["Время возникновения происшествия"]
            inc["_year"] = inc["_date"].dt.year
            inc["_month"] = inc["_date"].dt.month
            inc["_ym"] = inc["_date"].dt.to_period("M").astype(str)
            inc["_dow"] = inc["_date"].dt.day_name()
            inc["_hour"] = inc["_date"].dt.hour

        if not kor.empty:
            if "Дата" in kor.columns:
                kor["Дата"] = pd.to_datetime(kor["Дата"], errors="coerce")
            kor["_year"] = kor["Дата"].dt.year
            kor["_month"] = kor["Дата"].dt.month
            kor["_ym"] = kor["Дата"].dt.to_period("M").astype(str)

        return inc, kor
    except Exception as e:
        raise e
    finally:
        db.close()
