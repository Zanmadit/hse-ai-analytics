# HSE-AI-ANALYTICS

> [Russian version of the documentation is available here](./README.md)

An intelligent predictive analytics module for occupational health and safety and industrial safety systems.

This solution integrates data on incidents and safety behavior audits, transforming historical statistics into a tool for actively preventing injuries.

[Task](https://astanahub.com/ru/tech_task/vnedrenie-ii-v-sfere-okhrany-truda1772626245)

## Key Functions:
- **Predictive Analytics**: Forecasts the number of incidents for 3, 6, and 12 months.
- **Risk scoring**: Automatic identification of the “Top 5 risk areas” among organizations and production sites.
- **Interactive AI Database Chat**: Query the PostgreSQL database in natural language using an integrated local Ollama LLM (LLaMA3), which translates text int SQL automatically.
- **Alert System**: Automatic notifications upon detection of systematic violations in the “Korgau Maps” module.
- **Economic Impact**: Dynamic calculation of ROI and avoided costs (in tenge) based on reduced injury rates.
- **Recommendations**: Generation of specific preventive measures based on data analysis.

## Project Structure
```
.
├── app
│   ├── dashboard.py               # Main Frontend Visualization (Streamlit)
│   ├── llm                        
│   │   └── db_chat.py             # LangChain agent bridging NLP and SQL via Ollama
│   ├── ml
│   │   ├── forecast.py            # Predictive forecasting calculations
│   │   └── risk_score.py          # Risk index scoring engine
│   └── utils
│       ├── data_loader.py         # DB-to-Pandas abstracted logic
│       ├── db.py                  # SQLAlchemy Engine init
│       ├── init_db.py             # ETL script: moves CSVs to Postgres
│       └── models.py              # Postgres SQLAlchemy DB ORM schemas
├── data                           # Raw datasets
│   ├── incidents_upd.csv          
│   └── korgau_upd.csv             
├── Dockerfile                     # Streamlit web UI app image
├── docker-compose.yml             # Launch instructions for Postgres + Web
├── notebooks                      # Feature extraction and EDA exploration
├── pyproject.toml
├── README_EN.md
├── README.md
└── uv.lock    
```

## Installation and Startup (Docker)

To run the full end-to-end environment, Docker & Docker Compose are used.
_To use the AI-Chat functionality, ensure you have a local [Ollama](https://ollama.com/) instance running the `llama3` model (`ollama run llama3`). Docker container connects to it via port 11434._

1. Launch the PostgreSQL Database in the background:
```bash
docker-compose up -d db
```

2. Run the Initialization Script to populate data directly from CSVs to the newly active DB:
```bash
uv run python -m app.utils.init_db
```

3. Start the Web Dashboard Container:
```bash
docker-compose up -d web
```

4. View the dashboard locally at:
[http://localhost:8501](http://localhost:8501)
