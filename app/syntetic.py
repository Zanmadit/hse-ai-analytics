import pandas as pd
import random
import uuid
from datetime import datetime, timedelta

NUM_INCIDENTS = 600 
NUM_KORGAU = 1200   
START_DATE = datetime(2021, 1, 1)
END_DATE = datetime(2024, 1, 1)

orgs = ['ORG-A', 'ORG-B', 'ORG-C', 'ORG-D']
locations = ['Цех 1', 'Склад', 'Буровая 4', 'Офис', 'Площадка 2']
incident_types = ['НС', 'микротравма', 'опасная ситуация']
incident_statuses = ['Открытое', 'закрытое', 'расследуется']
korgau_types = ['Хорошая практика', 'Плохая практика']
korgau_categories = ['ОТ', 'ПБ', 'Экология', 'СИЗ']
korgau_statuses = ['Устранено', 'в работе', 'просрочено']

def random_date(start, end):
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

incidents = []
for _ in range(NUM_INCIDENTS):
    incidents.append({
        'id': str(uuid.uuid4()),
        'date': random_date(START_DATE, END_DATE).strftime('%Y-%m-%d %H:%M:%S'),
        'type': random.choice(incident_types),
        'org_id': random.choice(orgs),
        'location': random.choice(locations),
        'description': f"Синтетическое описание инцидента {_}",
        'cause': "Синтетическая причина",
        'status': random.choice(incident_statuses)
    })

df_incidents = pd.DataFrame(incidents)
df_incidents.to_csv('data/incidents.csv', index=False, encoding='utf-8')
print(f"Сгенерирован incidents.csv: {len(df_incidents)} строк")

korgau_cards = []
for _ in range(NUM_KORGAU):
    korgau_cards.append({
        'id': str(uuid.uuid4()),
        'date': random_date(START_DATE, END_DATE).strftime('%Y-%m-%d'),
        'obs_type': random.choices(korgau_types, weights=[0.3, 0.7])[0], 
        'org_id': random.choice(orgs),
        'category': random.choice(korgau_categories),
        'description': f"Синтетическое наблюдение Коргау {_}",
        'resolved': random.choice(korgau_statuses)
    })

df_korgau = pd.DataFrame(korgau_cards)
df_korgau.to_csv('data/korgau.csv', index=False, encoding='utf-8')
print(f"Сгенерирован koргau_cards.csv: {len(df_korgau)} строк")