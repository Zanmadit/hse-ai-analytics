import pandas as pd

def calculate_top_risks(fi, fk, ORG_COL="Наименование организации ДЗО"):
    """
    Computes top 5 Risk Zones index using Incidents and Korgau observations.
    """
    if fi.empty or ORG_COL not in fi.columns:
        return None

    rdf = fi.groupby(ORG_COL).agg(incidents=("_date","count")).reset_index()
    
    if "Несчастный случай" in fi.columns:
        ns_s = fi.groupby(ORG_COL)["Несчастный случай"].sum().reset_index()
        ns_s.columns = [ORG_COL, "ns"]
        rdf = rdf.merge(ns_s, on=ORG_COL, how="left")
    else:
        rdf["ns"] = 0
        
    if not fk.empty and "Организация" in fk.columns and "риск" in fk.columns:
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
    
    return rdf.sort_values("idx", ascending=False).head(5)
