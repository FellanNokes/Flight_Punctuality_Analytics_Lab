# Flight_Punctuality_Analytics_Lab

### Dagster setup

Dagster stores run history, materializations and schedule state in `DAGSTER_HOME`. Without it, `dagster dev` uses a temporary folder that is wiped on every restart, which means run history is lost and assets with `on_missing` run again.

#### Prerequisites

- `.dlt/secrets.toml` in `dlt_code/` with Snowflake credentials
- `~/.dbt/profiles.yml` with the `dbt_flights` profile
- dbt packages installed:

```bash
  cd dbt_code
  dbt deps
  cd ..
```

#### 1. Create the Dagster home folder

In the repo root (already in `.gitignore`):

```bash
mkdir .dagster_home
touch .dagster_home/dagster.yaml
```

The empty `dagster.yaml` removes a warning on startup.

#### 2. Set environment variables

Add to `.env` in the repo root, with your own absolute path:
SWEDAVIA_API_KEY=<your key>
DAGSTER_HOME=C:/path/to/Flight_Punctuality_Analytics_Lab/.dagster_home
PYTHONLEGACYWINDOWSSTDIO=1


`PYTHONLEGACYWINDOWSSTDIO` is only needed on Windows, so that print output shows up in the Dagster UI.

Alternatively, set `DAGSTER_HOME` in the terminal before starting Dagster:

```bash
# Git Bash / macOS / Linux
export DAGSTER_HOME="$(pwd)/.dagster_home"

# PowerShell
$env:DAGSTER_HOME = "$PWD\.dagster_home"
```

#### 3. Start Dagster

From the repo root:

```bash
dagster dev -f orchestration/definitions.py
```

Open http://localhost:3000.

#### 4. Turn on automation

Schedules and sensors are off by default. Under **Automation**, turn on:

- `schedule_flights`: loads flight data every other day at 12:00 Swedish time
- `flights_loaded_sensor`: runs dbt when flight data has been loaded
- `default_automation_condition_sensor`: loads the Wikipedia reference data once, if it has never been loaded

### Docker container how to test

1. Copy `.env.example` to `.env` and fill in the values
2. Start Docker Desktop
3. From the repo root:

```bash
   docker compose up --build -d dwh_pipeline
```

4. Open `localhost:3000` and check that all three automations are on under **Automation**


## Deploy the Dagster pipeline to Azure

The pipeline runs as a container in **Azure Container Apps**. The image is stored in **Azure Container Registry**.

### 1. Push the image

Get the login details in the Azure portal: **Container registries** → `crflightpunctuality` → **Access keys**. Username is `crflightpunctuality`, password is `password` from that page.

From the repo root, with Docker Desktop running:

```bash
docker login crflightpunctuality.azurecr.io
docker compose build dwh_pipeline
docker compose push dwh_pipeline
```

### 2. Create the container app

In the Azure portal: **Container Apps** → **Create**.

**Basics**
- Resource group: `rg-flight-punctuality`
- Container app name: `flights-dagster`
- Container Apps environment: create new, default settings

**Container**
- Uncheck **Use quickstart image**
- Image source: **Azure Container Registry**
- Registry: `crflightpunctuality.azurecr.io`, image: `dwh_pipeline`, tag: `latest`
- Environment variables: `SWEDAVIA_API_KEY`, `DESTINATION__SNOWFLAKE__CREDENTIALS__HOST`, `DESTINATION__SNOWFLAKE__CREDENTIALS__PASSWORD`, `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER_TRANSFORMER_PASSWORD` (values from your `.env`), and `DAGSTER_HOME` = `/pipeline/.dagster_home`

**Ingress**
- Ingress: **Enabled**
- Ingress traffic: **Accepting traffic from anywhere**
- Target port: **3000**

**Review + create** → **Create**.

### 3. Open Dagster

In the container app: **Overview** → click **Application Url**.

### Deploy a new version

```bash
docker compose build dwh_pipeline
docker compose push dwh_pipeline
```

Then in the container app: **Revisions and replicas** → **Create new revision** → **Create**.

---
### Troubleshooting

- **Values without quotes.** In `.env` values can have quotes, but in Azure the quotes become part of the value. Paste values without `"`.
- **Changes need a new revision.** After editing environment variables, click **Save** in the panel and then **Save as a new revision**. If a run still fails with a missing variable, **Stop** and **Start** the app on **Overview**, and run it again.

### Running it all the time

By default the container app scales down to zero when nobody has Dagster open. Then the schedule and sensors stop, so the flight data is not loaded at 12:00.

To keep it running: **Application** → **Scale** → set **Min replicas** and **Max replicas** to **1** → **Save**.

- **Min 1** keeps one container running all the time, so the schedule fires.
- **Max 1** stops Azure from starting extra copies, which would run the same schedule twice.

**Watch your credits.** A container that is always on costs money every hour, even when nobody uses it. Use the smallest size (0.25 CPU, 0.5 GB), check the cost under **Cost Management** now and then, and set Min replicas back to **0** (or stop the app) when the lab is over, so the credits do not run out.

**Known limitation:** `DAGSTER_HOME` lives inside the container. When the container restarts, run history is lost and the Wikipedia data is loaded again. This can be fixed by mounting an Azure File Share at `/pipeline/.dagster_home`.
