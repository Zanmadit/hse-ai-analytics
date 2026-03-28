import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from app.utils.db import Base, engine, SessionLocal
from app.utils.models import Incident, Korgau

def init_db():
    print("Testing DB connection...")
    try:
        with engine.connect() as conn:
            # Check DB response
            conn.scalar(text("SELECT 1"))
    except Exception as e:
        print(f"Warning: could not ping db: {e}")

    print("Creating tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    print("Loading Incidents...")
    df_inc = pd.read_csv('data/incidents_upd.csv')
    
    for c in ["Время возникновения происшествия", "Время и дата сообщения"]:
        if c in df_inc.columns:
            df_inc[c] = pd.to_datetime(df_inc[c], errors="coerce")
            
    bool_col = ["Несчастный случай", "В рабочее время", "На рабочем месте"]
    for col in bool_col:
        if col in df_inc.columns:
            df_inc[col] = df_inc[col].map(lambda x: True if str(x).strip().lower() in ("true","1","да","yes") else False)

    db = SessionLocal()
    inc_objects = []
    
    # Process mostly the available columns
    for _, row in df_inc.iterrows():
        desc = str(row.get('Краткое описание происшествия', ''))
        meas = str(row.get('Корректирующие меры', ''))
        
        do = row.get('Время возникновения происшествия')
        dr = row.get('Время и дата сообщения')
        
        inc = Incident(
            org_name=row.get('Наименование организации ДЗО'),
            business_direction=row.get('Бизнес направление'),
            date_occurred=do if not pd.isna(do) else None,
            date_reported=dr if not pd.isna(dr) else None,
            injury_severity=row.get('Тяжесть травмы'),
            injured_body_part=row.get('Пострадавшая часть тела'),
            position=row.get('Должность пострадавшего'),
            work_type=row.get('Вид работ'),
            is_accident=row.get('Несчастный случай'),
            in_work_hours=row.get('В рабочее время'),
            at_workplace=row.get('На рабочем месте'),
            contractor=row.get('Подрядная организация'),
            preliminary_causes=row.get('Предварительные причины'),
            description=desc if desc.lower() != 'nan' else None,
            corrective_measures=meas if meas.lower() != 'nan' else None
        )
        inc_objects.append(inc)
    
    db.bulk_save_objects(inc_objects)
    db.commit()
    print(f"Inserted {len(inc_objects)} incidents.")

    print("Loading Korgau...")
    df_kor = pd.read_csv('data/korgau_upd.csv')
    if "Дата" in df_kor.columns:
        df_kor["Дата"] = pd.to_datetime(df_kor["Дата"], errors="coerce")
        
    bool_kor = [
        "Производилась ли остановка работ?",
        "Обсудили ли вы небезопасное действие / небезопасное поведение с наблюдаемым?",
        "Сообщили ли ответственному лицу?",
        "Было ли небезопасное условие / поведение исправлено и опасность устранена?",
    ]
    for col in bool_kor:
        if col in df_kor.columns:
            df_kor[col] = df_kor[col].map(lambda x: True if str(x).strip().lower() in ("true","1","да","yes") else False)

    kor_objects = []
    for _, row in df_kor.iterrows():
        bene = str(row.get('Какие возможные последствия наблюдения или преимущества хорошей практики / вашего предложения?', ''))
        meas = str(row.get('Какие меры вы предприняли?', ''))
        
        d_obs = row.get('Дата')
        
        kor = Korgau(
            observation_type=row.get('Тип наблюдения'),
            category=row.get('Категория наблюдения'),
            date_observed=d_obs if not pd.isna(d_obs) else None,
            time_observed=str(row.get('Время')),
            org=row.get('Организация'),
            stopped_work=row.get('Производилась ли остановка работ?', False),
            discussed=row.get('Обсудили ли вы небезопасное действие / небезопасное поведение с наблюдаемым?', False),
            reported=row.get('Сообщили ли ответственному лицу?', False),
            resolved=row.get('Было ли небезопасное условие / поведение исправлено и опасность устранена?', False),
            risk_level=float(row.get('риск', 0)) if not pd.isna(row.get('риск')) else None,
            critical_alert=int(row.get('критическое оповещание', 0)) if not pd.isna(row.get('критическое оповещание')) else None,
            consequences_or_benefits=bene if bene.lower() != 'nan' else None,
            measures_taken=meas if meas.lower() != 'nan' else None
        )
        kor_objects.append(kor)
        
    db.bulk_save_objects(kor_objects)
    db.commit()
    db.close()
    print(f"Inserted {len(kor_objects)} korgau observations.")
    print("Database initialization complete.")

if __name__ == "__main__":
    init_db()
