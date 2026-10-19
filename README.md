# Flight_Punctuality_Analytics_Lab

### Dagster setup

Dagster stores run history, materializations and schedule state in `DAGSTER_HOME`. Without it, `dagster dev` uses a temporary folder that is wiped on every restart, which means run history is lost and assets with `on_missing` run again.

1. Create the folder in the repo root (already in `.gitignore`):

```bash
   mkdir .dagster_home
```

2. Set `DAGSTER_HOME` to its absolute path before starting Dagster, from the repo root:

```bash
   # Git Bash / macOS / Linux
   export DAGSTER_HOME="$(pwd)/.dagster_home"

   # PowerShell
   $env:DAGSTER_HOME = "$PWD\.dagster_home"
```

   The path must be absolute and differs per machine, so it is not committed.

3. Start Dagster:

```bash
   dagster dev
```