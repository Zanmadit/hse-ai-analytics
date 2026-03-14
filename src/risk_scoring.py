def risk_score(incidents):
    '''
    Calculates a risk index for each organization and industrial site. Ranks facilities based on the frequency and severity of incidents, 
    identifying the “Top 5 risk areas.” This allows management to focus industrial safety resources on the most problematic areas.
    '''

    org_risk = (
        incidents
        .groupby("org_id")
        .size()
        .sort_values(ascending=False)
    )

    location_risk = (
        incidents
        .groupby("location")
        .size()
        .sort_values(ascending=False)
    )

    return org_risk, location_risk