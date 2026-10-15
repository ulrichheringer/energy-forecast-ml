# Energy Consumption Forecast

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)  [![statsmodels](https://img.shields.io/badge/statsmodels-4051b5?style=for-the-badge&logo=python&logoColor=white)](https://www.statsmodels.org/)  [![MIT License](https://img.shields.io/badge/License-MIT-2ea44f?style=for-the-badge)](LICENSE)  ![Synthetic Data](https://img.shields.io/badge/Data-Synthetic-6b7280?style=for-the-badge)

Forecasts daily energy use with SARIMA and a time-based evaluation split.

## Data

A deterministic synthetic time series is generated locally in `pipeline.py`. It requires no private data or external download.

## Install and run

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
python cli.py evaluate
python cli.py train --model model.joblib
python cli.py predict --model model.joblib
```

## Evaluation results

With seed 42, SARIMA was trained on 1,005 days and evaluated on the final 90 days. The forecast had an MAE of 2.9880 MWh and an RMSE of 3.7568 MWh. The generated series has a weekly pattern, a small trend, and Gaussian noise; these errors do not estimate performance on real meter readings.

## Limitations

The synthetic series is intentionally simple. Real forecasting would require energy data from the target site and evaluation across multiple seasonal periods.
