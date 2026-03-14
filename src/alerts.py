import pandas as pd

def korgau_alerts(korgau):
    '''
    Implements an Early Warning System. 
    Analyzes the “Korgau” observation log for systematic violations. If the number of “unsafe actions” at a single location exceeds a threshold value, the function generates a critical alert to prevent a potential incident.
    '''

    recent = korgau[
        korgau["date"] > korgau["date"].max() - pd.Timedelta(days=30)
    ]

    alerts = (
        recent
        .groupby(["org_id","category"])
        .size()
        .reset_index(name="count")
    )

    critical = alerts[alerts["count"] > 3]

    return critical