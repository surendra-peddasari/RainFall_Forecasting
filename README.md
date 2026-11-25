# Rainfall Forecasting: Changi, Singapore

Forecasting **monthly total rainfall** and **monthly highest daily rainfall** for the next 12 months (Jul 2020 to Jun 2021) from 38 years of Changi Climate Station data, using seasonal time-series models compared against strong baselines.

> **Live demo:** (https://rainfallforecasting-7emj3dbptukfqxddajtnzu.streamlit.app/)

![Final forecast](images/final_forecast.png)

## Highlights

- **Data:** 462 monthly observations (Jan 1982 to Jun 2020), 3 series, no missing values.
- **Models:** two baselines (seasonal naive, monthly average), **SARIMA** with an AIC grid search, and **Prophet**.
- **Evaluation:** a 12-month hold-out test **and** 5-fold rolling validation (5 consecutive test years), reported with MAE and RMSE.
- **Result:** SARIMA is the best model for both targets in every comparison, but only 2 to 4% ahead of the monthly-average baseline on rolling validation. Most month-to-month variation is unpredictable; the reliable signal is the seasonal pattern.
- **Deliverables:** documented notebook, forecast CSVs, result tables, and a Streamlit app.

## Problem

1. Forecast **monthly total rainfall (mm)** for the next 12 months.
2. Forecast the **highest single-day rainfall (mm)** in each of those months.

## Data

Source: National Environment Agency (NEA) via [data.gov.sg](https://data.gov.sg), Changi Climate Station, released under the [data.gov.sg Open Data Licence](https://data.gov.sg/open-data-licence). Coverage 1982-01 to 2020-06, monthly.

| File (in `data/`) | Column | Meaning |
|---|---|---|
| `rainfall-monthly-total.csv` | `total_rainfall` | Total rainfall in the month (mm) |
| `rainfall-monthly-highest-daily-total.csv` | `maximum_rainfall_in_a_day` | Highest single-day rainfall in the month (mm) |
| `rainfall-monthly-number-of-rain-days.csv` | `no_of_rainy_days` | Days with at least 0.2 mm of rain |

## Exploratory findings

- **Strong seasonality.** Wettest months are December (about 318 mm average), November (about 256 mm) and January (about 226 mm), consistent with the northeast monsoon. February is the driest (about 105 mm).
- **Right-skewed and volatile.** Skewness is 1.24 and the standard deviation is about 64% of the mean. Extremes include 766 mm in Dec 2006 and 216 mm in a single day in Jan 2011.
- **No strong long-term trend.** Annual rainfall averages about 2,118 mm. Rain days per year rose modestly, from about 161 (1982 to 1991) to about 173 (2010 to 2019).
- **Correlations.** Total rainfall vs highest daily rainfall is 0.80, and vs number of rain days is 0.70.

![Average rainfall by month](images/eda_monthly_avg.png)

## Method

1. **Load and validate** the three series (consistency check: highest daily never exceeds the monthly total).
2. **EDA:** plots, seasonal decomposition, monthly averages, yearly totals, correlations.
3. **Split in time order:** train Jan 1982 to Jun 2019, test Jul 2019 to Jun 2020. No shuffling.
4. **Baselines:** seasonal naive (repeat last year) and monthly average.
5. **SARIMA** with seasonal differencing (period 12) and an AIC grid search over p, q in 0..2 and P, Q in 0..1. Forecasts clipped at zero.
6. **Prophet** with yearly seasonality.
7. **Rolling validation** over 5 test years, refitting each time.
8. **Final forecast** with the best model refit on all data, with 95% prediction intervals.

## Results

Lower is better. Best model per table in bold. MAE and RMSE are in mm.

### Hold-out test year (Jul 2019 to Jun 2020)

**Total rainfall**

| Model | MAE | RMSE |
|---|---:|---:|
| **SARIMA** | **86.8** | **97.5** |
| Monthly average | 92.7 | 102.1 |
| Prophet | 96.7 | 103.6 |
| Seasonal naive (last year) | 88.0 | 112.5 |

**Highest daily rainfall**

| Model | MAE | RMSE |
|---|---:|---:|
| **SARIMA** | **18.7** | **24.3** |
| Monthly average | 19.7 | 26.5 |
| Seasonal naive (last year) | 22.5 | 27.3 |
| Prophet | 21.7 | 28.5 |

### Rolling validation (average of 5 test years, Jul 2015 to Jun 2020)

**Total rainfall**

| Model | MAE | RMSE |
|---|---:|---:|
| **SARIMA** | **64.7** | **75.5** |
| Monthly average | 66.3 | 76.7 |
| Seasonal naive | 78.3 | 97.3 |

**Highest daily rainfall**

| Model | MAE | RMSE |
|---|---:|---:|
| **SARIMA** | **20.2** | **23.9** |
| Monthly average | 20.7 | 24.8 |
| Seasonal naive | 22.0 | 26.1 |

### Key takeaways

- **SARIMA wins consistently** on both targets, so its single-year lead was not luck.
- **The margin is small.** The seasonal monthly-average baseline is hard to beat, which means month-to-month rainfall is mostly noise around a seasonal mean.
- **Prophet did not beat the simple baseline** on the hold-out year, so it was dropped from rolling validation. A more complex model is not automatically better.
- **Seasonal naive is the weakest**, because copying last year's noise adds error.

![Total rainfall test year](images/total_test.png)
![Highest daily rainfall test year](images/max_test.png)

## Forecast: Jul 2020 to Jun 2021

| Month | Total rainfall (mm) | 95% interval | Highest daily (mm) | 95% interval |
|---|---:|---:|---:|---:|
| Jul 2020 | 136 | 0 to 329 | 39 | 0 to 105 |
| Aug 2020 | 171 | 0 to 365 | 44 | 0 to 111 |
| Sep 2020 | 125 | 0 to 319 | 39 | 0 to 106 |
| Oct 2020 | 182 | 0 to 377 | 51 | 0 to 118 |
| Nov 2020 | 235 | 40 to 430 | 63 | 0 to 130 |
| Dec 2020 | 337 | 142 to 532 | 77 | 11 to 144 |
| Jan 2021 | 207 | 12 to 402 | 70 | 3 to 137 |
| Feb 2021 | 123 | 0 to 318 | 35 | 0 to 102 |
| Mar 2021 | 142 | 0 to 338 | 44 | 0 to 110 |
| Apr 2021 | 170 | 0 to 366 | 44 | 0 to 111 |
| May 2021 | 149 | 0 to 344 | 46 | 0 to 113 |
| Jun 2021 | 151 | 0 to 346 | 41 | 0 to 108 |

Rainfall is forecast to rise from October and peak in **December 2020**. The intervals are wide, which reflects genuine uncertainty: the model captures the seasonal level, not individual wet or dry months.

## Repository structure

```
rainfall-forecasting-singapore/
├── README.md
├── app.py                          Streamlit forecast app
├── requirements.txt                App dependencies
├── notebooks/
│   └── rainfall_forecasting.ipynb  Full analysis, explained step by step
├── data/                           Original NEA CSV files (3)
├── outputs/
│   ├── forecasts/                  12-month forecast CSVs (total, highest daily)
│   └── results/                    Model comparison and rolling-validation tables
└── images/                         Plots used in this README and the notebook
```

## How to run

**Streamlit app**

```bash
pip install -r requirements.txt
streamlit run app.py
```

**Notebook** (needs extra libraries)

```bash
pip install pandas numpy matplotlib scikit-learn statsmodels prophet jupyter
jupyter notebook notebooks/rainfall_forecasting.ipynb
```

Run the notebook from the repo root or from `notebooks/`; paths are resolved automatically. Re-running regenerates the files in `outputs/` and `images/`. Small numeric differences are possible for Prophet.

## Limitations

- One weather station and 38 years of data.
- No external predictors (for example ENSO or Indian Ocean Dipole indices).
- Data ends in June 2020, so the forecast is a demonstration, not an up-to-date operational forecast.
- Single-month extremes cannot be predicted; intervals are wide.
- SARIMA orders were selected on data that overlaps some rolling-validation windows, so those scores may be slightly optimistic.
- Prophet was not included in rolling validation.

## Next steps

- Add rain days or climate indices as exogenous variables in SARIMAX.
- Compare against gradient boosting and an LSTM.
- Model extremes separately (for example with extreme value theory).
- Extend to multiple stations and evaluate against newer data.

## Acknowledgements

Rainfall data: National Environment Agency, Singapore, via data.gov.sg.
