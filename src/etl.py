import pandas as pd

def load_data():
    incidents = pd.read_csv("data/incidents.csv")
    korgau = pd.read_csv("data/korgau.csv")

    incidents['date'] = pd.to_datetime(incidents['date'])
    korgau['date'] = pd.to_datetime(korgau['date'])

    return incidents, korgau