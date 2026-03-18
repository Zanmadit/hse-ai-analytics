# HSE-AI-ANALYTICS

> [English version of the documentation is available here](./README_EN.md)

An intelligent predictive analytics module for occupational health and safety and industrial safety systems.

This solution integrates data on incidents and safety behavior audits, transforming historical statistics into a tool for actively preventing injuries.

[Task](https://astanahub.com/ru/tech_task/vnedrenie-ii-v-sfere-okhrany-truda1772626245)

## Key Functions:
- **Predictive Analytics**: Forecasts the number of incidents for 3, 6, and 12 months.
- **Risk scoring**: Automatic identification of the “Top 5 risk areas” among organizations and production sites.
- **NLP Analysis**: Clustering of textual incident descriptions to identify underlying causes of incidents.
- **Alert System**: Automatic notifications upon detection of systematic violations in the “Korgau Maps” module.
- **Economic Impact**: Dynamic calculation of ROI and avoided costs (in tenge) based on reduced injury rates.
- **Recommendations**: Generation of specific preventive measures based on data analysis.


## Project Structure
```
.
├── app
│   └── dashboard.py               # vizualization
├── data                           # data
│   ├── incidents_upd.csv          # updated Incidents
│   ├── incidents.xlsx
│   ├── korgau_upd.csv             # updated Korgau
│   └── korgau.xlsx
├── notebooks                      # working wirh data, feature extraction
│   ├── incidents.ipynb
│   └── korgau.ipynb
├── pyproject.toml
├── README_EN.md
├── README.md
└── uv.lock    
```


## Installation and Startup

1. Install `uv`
2. In project directory
```
uv venv
uv sync
```
3. Run Dashboard
```
streamlit run app/dashboard.py
```
