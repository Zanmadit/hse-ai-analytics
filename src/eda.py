import pandas as pd

def correlation_analysis(incidents, korgau):
    '''
    Conducts a statistical analysis of the relationship between behavioral audits (Korgau) and actual incidents. It confirms 
    the hypothesis that an increase in hazardous conditions identified in the Korgau module 
    precedes an increase in injuries, thereby demonstrating the predictive value of the model.
    '''

    inc_month = incidents.groupby(
        incidents["date"].dt.to_period("M")
    ).size()

    kor_month = korgau.groupby(
        korgau["date"].dt.to_period("M")
    ).size()

    df = pd.concat([inc_month, kor_month], axis=1)
    df.columns = ["incidents", "violations"]

    corr = df.corr()

    return corr