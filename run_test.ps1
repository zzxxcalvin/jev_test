$ErrorActionPreference = "Stop"
[Console]::InputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$ProjectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonExe = Join-Path $ProjectDir ".venv\Scripts\python.exe"

$env:HF_HOME = Join-Path $ProjectDir ".cache\huggingface"
$env:HF_HUB_CACHE = Join-Path $env:HF_HOME "hub"
$env:TRANSFORMERS_CACHE = Join-Path $env:HF_HOME "transformers"
$env:TORCH_HOME = Join-Path $ProjectDir ".cache\torch"
$env:PIP_CACHE_DIR = Join-Path $ProjectDir ".cache\pip"
$env:TEMP = Join-Path $ProjectDir ".cache\temp"
$env:TMP = $env:TEMP
$env:USE_TF = "0"
$env:PYTHONUTF8 = "1"
$env:HF_HUB_DISABLE_SYMLINKS_WARNING = "1"

New-Item -ItemType Directory -Force -Path $env:HF_HOME, $env:TORCH_HOME, $env:PIP_CACHE_DIR, $env:TEMP | Out-Null

if (-not (Test-Path -LiteralPath $PythonExe)) {
    throw "找不到專案虛擬環境：$PythonExe"
}

& $PythonExe (Join-Path $ProjectDir "test_laya.py") @args
exit $LASTEXITCODE
