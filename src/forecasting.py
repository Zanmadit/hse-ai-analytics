from prophet import Prophet

def forecast_incidents(incidents, months=12):
    '''
    The function aggregates historical data on a weekly basis, identifies seasonal 
    patterns, and generates a forecast of the number of incidents for a specified 
    period (3 to 12 months) with a 95% confidence interval.
    '''
    
    df = incidents.set_index('date').resample('W').size().reset_index(name='y')
    df.rename(columns={"date": "ds"}, inplace=True)

    model = Prophet(
        yearly_seasonality=True, 
        weekly_seasonality=True, 
        daily_seasonality=False,
        interval_width=0.95
    )
    
    model.fit(df)

    future = model.make_future_dataframe(periods=months*4, freq="W")
    forecast = model.predict(future)

    return forecast