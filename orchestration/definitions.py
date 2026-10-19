# ==================== #
#                      #
#       imports        #
#                      #
# ==================== #
# Start Dagster from the repo root:
#   dagster dev -f orchestration/definitions.py

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parents[1]

# Tell dlt where .dlt/ (secrets.toml) lives. Must be set before dlt is imported.
os.environ["DLT_PROJECT_DIR"] = str(REPO_ROOT / "dlt_code")

# Make the dlt scripts importable, independent of where Dagster is started
sys.path.insert(0, str(REPO_ROOT / "dlt_code"))

import dlt
import dagster as dg
from dagster_dlt import DagsterDltResource, DagsterDltTranslator, dlt_assets
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets

from load_flights import flights_source
from load_reference import wikipedia_source


# ==================== #
#                      #
#      dlt Assets      #
#                      #
# ==================== #

# an instance from the dlt resource class to run dlt codes
dlt_resource = DagsterDltResource()


# Flight data: arrivals and departures, each merged on flight_key (to avoid duplicates)
@dlt_assets(
    dlt_source=flights_source(),
    dlt_pipeline=dlt.pipeline(
        pipeline_name="swedavia_flights",
        dataset_name="staging",
        destination="snowflake",
    ),
    name="flights",
    group_name="flights",
)
def dlt_flights(context: dg.AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)


# Reference data should only be loaded once, so the assets get an
# on_missing automation condition: they run if they have never been materialized
class OnMissingTranslator(DagsterDltTranslator):
    def get_asset_spec(self, data):
        default_spec = super().get_asset_spec(data)
        return default_spec.replace_attributes(
            automation_condition=dg.AutomationCondition.on_missing()
        )


# Reference data from Wikipedia: airports and airlines, replaced on every load
@dlt_assets(
    dlt_source=wikipedia_source(),
    dlt_pipeline=dlt.pipeline(
        pipeline_name="wikipedia",
        dataset_name="staging",
        destination="snowflake",
    ),
    name="wikipedia",
    group_name="reference",
    dagster_dlt_translator=OnMissingTranslator(),
)
def dlt_wikipedia(context: dg.AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)


# ==================== #
#                      #
#       dbt Asset      #
#                      #
# ==================== #
# needs dbt_packages pre-installed with 'dbt deps'

dbt_project_directory = REPO_ROOT / "dbt_code"
profiles_dir = Path.home() / ".dbt"

dbt_project = DbtProject(project_dir=dbt_project_directory, profiles_dir=profiles_dir)

# an instance from the dbt resource class to run dbt codes
dbt_resource = DbtCliResource(project_dir=dbt_project)

# produce the manifest file, which lets Dagster understand dependencies between models
dbt_project.prepare_if_dev()


# build runs seeds, models and tests
@dbt_assets(manifest=dbt_project.manifest_path)
def dbt_models(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()


# ==================== #
#                      #
#         Jobs         #
#                      #
# ==================== #

job_flights = dg.define_asset_job("job_flights", selection=dg.AssetSelection.assets(dlt_flights))
job_wikipedia = dg.define_asset_job("job_wikipedia", selection=dg.AssetSelection.assets(dlt_wikipedia))
job_dbt = dg.define_asset_job("job_dbt", selection=dg.AssetSelection.assets(dbt_models))


# ==================== #
#                      #
#       Schedule       #
#                      #
# ==================== #

# Every other day at 12:00 Swedish time. The API keeps 2 days back,
# and each run fetches the last 2 days plus today, so runs overlap.
schedule_flights = dg.ScheduleDefinition(
    job=job_flights,
    cron_schedule="0 12 */2 * *",
    execution_timezone="Europe/Stockholm",
)


# ==================== #
#                      #
#        Sensor        #
#                      #
# ==================== #

# Run dbt when the flight data has been loaded.
# Arrivals and departures are loaded in the same run, so watching one is enough.
@dg.asset_sensor(asset_key=dg.AssetKey("dlt_flights_source_departures"), job_name="job_dbt")
def flights_loaded_sensor():
    yield dg.RunRequest()


# ==================== #
#                      #
#     Definitions      #
#                      #
# ==================== #

defs = dg.Definitions(
    assets=[dlt_flights, dlt_wikipedia, dbt_models],
    resources={
        "dlt": dlt_resource,
        "dbt": dbt_resource,
    },
    jobs=[job_flights, job_wikipedia, job_dbt],
    schedules=[schedule_flights],
    sensors=[flights_loaded_sensor],
)