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