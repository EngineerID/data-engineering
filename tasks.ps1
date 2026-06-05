<#
.SYNOPSIS
    Native-Windows task runner — a PowerShell mirror of the Makefile for hosts
    without WSL. Run from the repo root, e.g.  .\tasks.ps1 seed

.DESCRIPTION
    Uses the project virtualenv at .\.venv directly (no `make`, no WSL).
    Docker targets require Docker Desktop to be running.
#>
[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [ValidateSet('setup', 'up', 'down', 'up-cloud', 'down-cloud', 'seed', 'seed-large',
        'load-sql', 'lint', 'typecheck', 'test', 'test-cloud', 'check', 'spark-submit',
        'oom-lab', 'help')]
    [string]$Task = 'help',

    [Parameter(Position = 1)]
    [string]$Job
)

$ErrorActionPreference = 'Stop'
$Root = $PSScriptRoot
$Py = Join-Path $Root '.venv\Scripts\python.exe'
$Compose = @('compose', '-f', (Join-Path $Root 'infra\docker-compose.yml'))
$env:PYTHONPATH = 'src;.'

if (-not (Test-Path $Py)) {
    Write-Warning "venv not found at $Py — run '.\tasks.ps1 setup' first."
}

function Invoke-Py { & $Py @args; if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE } }

switch ($Task) {
    'setup' {
        $uv = Get-Command uv -ErrorAction SilentlyContinue
        if ($uv) { & uv sync --all-groups }
        else {
            Write-Host "uv not found; using pip into .venv"
            & $Py -m pip install -e '.[dev]'
        }
    }
    'up'         { & docker @Compose up -d postgres spark-master spark-worker-1 spark-worker-2 kafka }
    'down'       { & docker @Compose down }
    'up-cloud'   { & docker @Compose --profile cloud up -d localstack fake-gcs azurite }
    'down-cloud' { & docker @Compose --profile cloud down }
    'seed'       { Invoke-Py -m def_.datagen.cli --scale-gb 0.01 }
    'seed-large' { Invoke-Py -m def_.datagen.cli --scale-gb 1.0 }
    'load-sql'   { Invoke-Py modules\02_sql_relational\load_to_postgres.py }
    'lint' {
        Invoke-Py -m ruff check src modules tests
        Invoke-Py -m ruff format --check src modules tests
    }
    'typecheck'  { Invoke-Py -m mypy }
    'test' {
        Invoke-Py -m pytest -m 'not spark and not kafka and not cloud' `
            --ignore=modules/04_spark_internals/tests `
            --ignore=modules/06_streaming_kafka/tests
    }
    'test-cloud' { Invoke-Py -m pytest modules/09_cloud_portability/tests -m cloud }
    'check' {
        & $PSCommandPath lint
        & $PSCommandPath typecheck
        & $PSCommandPath test
    }
    'spark-submit' {
        if (-not $Job) { Write-Error "Usage: .\tasks.ps1 spark-submit modules/04_spark_internals/join_aggregate_job.py"; exit 1 }
        & docker @Compose exec -T -e PYTHONPATH=/workspace/src spark-master spark-submit `
            --master spark://spark-master:7077 --deploy-mode client `
            --conf spark.driver.host=spark-master --conf spark.driver.bindAddress=0.0.0.0 `
            "/workspace/$Job"
    }
    'oom-lab' {
        & $PSCommandPath spark-submit 'modules/04_spark_internals/oom_exercise.py'
    }
    default {
        Write-Host "Tasks: setup up down up-cloud down-cloud seed seed-large load-sql lint typecheck test test-cloud check spark-submit <job> oom-lab"
    }
}
