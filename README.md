# Flight Punctuality Analytics Lab

A data pipeline and dashboard for flight punctuality at Swedavia's ten Swedish airports.

Flight data is loaded from the Swedavia FlightInfo API with **dlt**, modelled in **Snowflake** with **dbt**, orchestrated with **Dagster** and shown in a **Streamlit** dashboard. The pipeline and the dashboard run as containers on **Azure**.

```
            Azure Container Registry: crflightpunctuality
           dwh_pipeline image                    dashboard image
                    │                                   │
                    ▼                                   ▼
┌─ Azure Container App ─────────────────┐  ┌─ Azure Web App ──────────┐
│  dwh_pipeline container (port 3000)   │  │  dashboard container     │
│  Dagster                              │  │  (port 8501)             │
│   ├─ dlt: Swedavia API + Wikipedia    │  │  Streamlit               │
│   └─ dbt: warehouse + marts           │  │                          │
└───────────────────┬───────────────────┘  └────────────▲─────────────┘
                    │ writes                            │ reads marts
                    ▼                                   │
          ┌─────────────────────────────────────────────┴─────────┐
          │  Snowflake: staging → warehouse → marts               │
          └───────────────────────────────────────────────────────┘
```

## Contents

- [Repo structure](#repo-structure)
- [Setup](#setup)
- [Run locally](#run-locally)
- [Run in Docker](#run-in-docker)
- [Deploy to Azure](#deploy-to-azure)
- [Troubleshooting](#troubleshooting)
- [Known limitations](#known-limitations)

## Repo structure

| Path | What it is |
|---|---|
| `dlt_code/` | dlt sources: `load_flights.py` (Swedavia) and `load_reference.py` (Wikipedia airports and airlines) |
| `dlt_code/worksheet_snowflake/` | SQL to set up warehouse, database, roles and users in Snowflake |
| `dbt_code/` | dbt project: `src` → `dim` / `fct` (warehouse) → `mart` |
| `dbt_code/seeds/` | `missing_airports.csv`, Swedish airports missing in the Wikipedia data |
| `orchestration/definitions.py` | Dagster assets, jobs, schedule and sensors |
| `dashboard/` | Streamlit app, entry file `Flights.py` |
| `profiles.yml` | dbt profile, credentials read from environment variables |
| `dockerfile.dwh`, `dockerfile.dashboard`, `docker-compose.yml` | Containers for the pipeline and the dashboard |
| `EDA/` | Exploration notebooks |

### What runs when

| What | When | How |
|---|---|---|
| Flight data (arrivals, departures) | Every other day at 12:00 Swedish time | `job_flights_schedule` |
| dbt build (seeds, models, tests) | Right after flight data is loaded | `flights_loaded_sensor` |
| Wikipedia reference data | Once, if it has never been loaded | `load_reference_once_sensor` |

All three are on by default when Dagster starts.

## Setup

### 1. Install dependencies

```bash
uv sync
cd dbt_code
uv run dbt deps
cd ..
```

### 2. Environment variables

Copy `.env.example` to `.env` in the repo root and fill in the values. It holds:

| Variable | Used by |
|---|---|
| `SWEDAVIA_API_KEY` | dlt, flights |
| `DESTINATION__SNOWFLAKE__CREDENTIALS__HOST`, `..._PASSWORD`, `..._DATABASE`, `..._USERNAME`, `..._WAREHOUSE`, `..._ROLE` | dlt (`extract_loader` user) |
| `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER_TRANSFORMER_PASSWORD` | dbt (`transformer` user) |
| `SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD`, `SNOWFLAKE_WAREHOUSE`, `SNOWFLAKE_DATABASE`, `SNOWFLAKE_SCHEMA`, `SNOWFLAKE_ROLE` | dashboard (`reporter` user) |
| `DAGSTER_HOME` | Dagster, absolute path to `.dagster_home` in your clone |
| `PYTHONLEGACYWINDOWSSTDIO=1` | Windows only, shows print output in the Dagster UI |

### 3. Dagster home

Dagster stores run history in `DAGSTER_HOME`. Without it, history is lost on every restart and the Wikipedia data is loaded again.

```bash
mkdir .dagster_home
touch .dagster_home/dagster.yaml
```

The folder is in `.gitignore`.

## Run locally

Run the commands from the repo root.

### Pipeline (Dagster)

```bash
uv run dagster dev -f orchestration/definitions.py
```

Open http://localhost:3000.

### Dashboard (Streamlit)

```bash
uv run streamlit run dashboard/Flights.py
```

Open http://localhost:8501.

The dashboard reads the `reporter` credentials from `.env`. The marts must be built by dbt before the dashboard can show any data. Write the file name with a capital F (`Flights.py`): Windows ignores the case, but Docker and Azure run on Linux, where it matters.

## Run in Docker

Docker Desktop must be running. From the repo root:

```bash
docker compose up --build -d dwh_pipeline
docker compose up --build -d dashboard
```

- Dagster: http://localhost:3000
- Dashboard: http://localhost:8501

Stop with `docker compose down`. Do **not** add `-v`, it deletes the Dagster history volume.

## Deploy to Azure

Both images are stored in the Container Registry `crflightpunctuality.azurecr.io`. The pipeline runs in **Azure Container Apps**, the dashboard in **Azure App Service**.

### 1. Log in to the registry

Login details: Azure portal → **Container registries** → `crflightpunctuality` → **Access keys**. Username is the registry name, password is `password` from that page.

```bash
docker login crflightpunctuality.azurecr.io
```

### 2. Build and push

Give every new version its own tag (`v1`, `v2`, ...) in the `image:` lines in `docker-compose.yml`. With `latest`, Azure may keep running the old image.

```bash
docker compose build dwh_pipeline dashboard
docker compose push dwh_pipeline dashboard
```

The images must be pushed before you create the apps, so they show up in the lists.

### 3. Pipeline: Container App

Azure portal → **Container Apps** → **Create**.

- **Basics:** resource group, name (`fpa-dagster-container-app`), new Container Apps environment with default settings
- **Container:** uncheck **Use quickstart image**, image source **Azure Container Registry**, image `dwh_pipeline` with your tag
- **Environment variables** (no quotes):
  - `SWEDAVIA_API_KEY`
  - `DESTINATION__SNOWFLAKE__CREDENTIALS__HOST`
  - `DESTINATION__SNOWFLAKE__CREDENTIALS__PASSWORD`
  - `DESTINATION__SNOWFLAKE__CREDENTIALS__DATABASE`
  - `DESTINATION__SNOWFLAKE__CREDENTIALS__USERNAME`
  - `DESTINATION__SNOWFLAKE__CREDENTIALS__WAREHOUSE`
  - `DESTINATION__SNOWFLAKE__CREDENTIALS__ROLE`
  - `SNOWFLAKE_ACCOUNT`
  - `SNOWFLAKE_USER_TRANSFORMER_PASSWORD`
  - `DAGSTER_HOME` = `/pipeline/.dagster_home`
- **Ingress:** enabled, accepting traffic from anywhere, target port **3000**

**Review + create** → **Create**. 

Open it from **Overview** → **Application Url**.

**Keep it running:** **Application** → **Scale** → **Min replicas 1** and **Max replicas 1**. Without min 1 the app sleeps and the schedule never fires. Max 1 stops the same schedule from running twice.

### 4. Dashboard: Web App

Azure portal → **App Services** → **Create** → **Web App**.

- **Basics:** resource group, name, publish **Container**, OS **Linux**
- **Container:** image source **Azure Container Registry**, image `dashboard` with your tag

**Review + create** → **Create**.

Then in the web app:

- **Settings** → **Environment variables** → **App settings**, add (no quotes):

  | Name | Value |
  |---|---|
  | `WEBSITES_PORT` | `8501` |
  | `STREAMLIT_SERVER_ADDRESS` | `0.0.0.0` |
  | `SNOWFLAKE_ACCOUNT` | from `.env` |
  | `SNOWFLAKE_USER` | `reporter` |
  | `SNOWFLAKE_PASSWORD` | from `.env` |
  | `SNOWFLAKE_WAREHOUSE` | `FLIGHTS_WH` |
  | `SNOWFLAKE_DATABASE` | `FLIGHTS` |
  | `SNOWFLAKE_SCHEMA` | `MARTS` |
  | `SNOWFLAKE_ROLE` | `FLIGHTS_REPORTER_ROLE` |

  **Apply** and confirm.

Open it from **Overview** → **Default domain**. The first load can take 20 to 30 seconds.

### 5. Deploy a new version

1. Bump the tag in `docker-compose.yml` (e.g. `v2` → `v3`)
2. Build and push as in step 2
3. Point Azure to the new tag:
   - **Pipeline:** **Application** → **Containers** → **Edit and deploy** → click the container → **Image tag** → **Save** → **Save as a new revision**
   - **Dashboard:** **Deployment Center** → change the tag → **Save**

The pipeline runs in an express environment, so its revision is always called `--latest`. Check **Date created** under **Revisions and replicas** to see that it was updated.

## Troubleshooting

| Problem | Fix |
|---|---|
| `SWEDAVIA_API_KEY not found` on Azure | The variable is missing in the container app. Add it and save as a new revision. |
| `config.toml cannot hold secret values` | Snowflake credentials must not be in `dlt_code/.dlt/config.toml`. Remove the `[destination.snowflake.credentials]` block and use the `DESTINATION__SNOWFLAKE__CREDENTIALS__*` environment variables instead. |
| Swedavia returns 401 | The key has quotes or spaces. In Azure, quotes become part of the value. |
| Old code still runs after a push | A restart reuses the old image. Use a new tag and save as a new revision. Verify in **Monitoring** → **Console**, e.g. `grep -n "d.date" /pipeline/dbt_code/models/mart/arrivals_filter_mart.sql` |
| Dashboard gives 503 and stops after ~4 minutes | `WEBSITES_PORT` is missing or misspelled (it has an S). Value must be `8501`. |
| `uv` fails with `Expected a Python module at src/...` | The project is not a package. Remove `[build-system]` from `pyproject.toml`. |
| `Failed to spawn: streamlit` in the container | Streamlit is missing in `pyproject.toml`. Run `uv add streamlit` and rebuild. |

## Known limitations

- **Dagster history on Azure** lives inside the container. A new revision or restart wipes it and reloads the Wikipedia data. Fix: mount an Azure File Share at `/pipeline/.dagster_home`.
- **Swedavia API** only returns data 2 days back, so the pipeline must run at least every other day.
- **Reference data** comes from Wikipedia. Swedish domestic airports are added with a seed, but some airlines and a few foreign airports are still missing. See `test.md` for data quality findings.
- **Costs:** the pipeline container is always on and uses Azure credits every hour. Check **Cost Management** and set Min replicas to 0 or stop the apps when the lab is over.