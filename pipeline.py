"""Daily synthetic energy forecast with a classical SARIMA model."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from statsmodels.tsa.statespace.sarimax import SARIMAX

SEED = 42
HOLDOUT_DAYS = 90


def _series(seed=SEED, days=1095):
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2022-01-01", periods=days, freq="D")
    weekly_profile = np.array([0.84, 0.87, 0.92, 0.96, 1.02, 1.16, 1.11])
    t = np.arange(days)
    values = 100 + 0.006 * t + 18 * weekly_profile[dates.dayofweek] + rng.normal(0, 3.2, days)
    return pd.Series(values, index=dates, name="consumption_mwh")


def _fit(series):
    model = SARIMAX(series, order=(1, 1, 1), seasonal_order=(1, 0, 0, 7),
                    enforce_stationarity=False, enforce_invertibility=False)
    return model.fit(disp=False, maxiter=100)


def sample_input():
    return {"steps": 14}


def train_model(seed=SEED):
    return _fit(_series(seed))


def predict(model, payload):
    steps = int(payload.get("steps", 14)) if isinstance(payload, dict) else int(payload)
    if steps < 1 or steps > 365:
        raise ValueError("steps must be between 1 and 365")
    forecast = model.get_forecast(steps=steps)
    return {"steps": steps, "forecast_mwh": [round(float(value), 3) for value in forecast.predicted_mean],
            "lower_95": [round(float(value), 3) for value in forecast.conf_int().iloc[:, 0]],
            "upper_95": [round(float(value), 3) for value in forecast.conf_int().iloc[:, 1]]}


def evaluate(seed=SEED):
    series = _series(seed)
    train, test = series.iloc[:-HOLDOUT_DAYS], series.iloc[-HOLDOUT_DAYS:]
    fitted = _fit(train)
    forecast = fitted.get_forecast(steps=len(test)).predicted_mean.to_numpy()
    return {"mae_mwh": round(float(mean_absolute_error(test.to_numpy(), forecast)), 4),
            "rmse_mwh": round(float(np.sqrt(mean_squared_error(test.to_numpy(), forecast))), 4),
            "train_days": int(len(train)), "test_days": int(len(test)),
            "holdout": "last 90 days in time order"}
