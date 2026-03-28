import pandas as pd
import numpy as np

def generate_forecast(fi, horizon=12):
    """
    Predictive analytics logic separated from the dashboard to easily swap forecasting models.
    """
    if fi.empty or "_ym" not in fi.columns or fi["_ym"].isna().all():
        return None
        
    df = fi.copy()
    ts_all = df.groupby("_ym").size().reset_index(name="count").sort_values("_ym")
    y = ts_all["count"].values.astype(float)
    n = len(y)

    if n < 6:
        return None

    x = np.arange(n)
    z = np.polyfit(x, y, 1)
    trend_hist = np.polyval(z, x)
    residuals  = y - trend_hist

    season_len = min(12, n)
    season = np.array([residuals[i::season_len].mean() for i in range(season_len)])

    fx      = np.arange(n, n + horizon)
    f_pred  = np.maximum(0, np.polyval(z, fx) + [season[i % season_len] for i in range(horizon)])
    f_std   = residuals.std()
    f_upper = f_pred + 1.6 * f_std
    f_lower = np.maximum(0, f_pred - 1.6 * f_std)

    last_p   = pd.Period(ts_all["_ym"].iloc[-1], freq="M")
    f_labels = [(last_p + i + 1).strftime("%Y-%m") for i in range(horizon)]

    return {
        "ts_all": ts_all,
        "trend_hist": trend_hist,
        "f_labels": f_labels,
        "f_pred": f_pred,
        "f_upper": f_upper,
        "f_lower": f_lower
    }
