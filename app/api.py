from fastapi import FastAPI

from src.etl import load_data
from src.risk_scoring import risk_score
from src.alerts import korgau_alerts
from src.eda import correlation_analysis

app = FastAPI()

incidents, korgau = load_data()

@app.get('/risk')
def risk():

    org_risk, location_risk = risk_score(incidents)

    return {
        "top_orgs": org_risk.head(5).to_dict(),
        "top_locations": location_risk.head(5).to_dict()
    }


@app.get("/alerts")
def alerts():

    a = korgau_alerts(korgau)

    return a.to_dict(orient="records")


@app.get("/correlation")
def correlation():

    corr = correlation_analysis(incidents, korgau)

    return {
        "correlation": corr.to_dict()
    }