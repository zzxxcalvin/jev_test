# Laya 本機測試

本專案使用獨立的 `.venv`，模型與套件快取也全部放在此資料夾內，避免占用 C 槽。

## 執行內建的 UE5 守衛決策範例

```powershell
Set-Location H:\MachineLearning\laya
.\run_test.ps1
```

第一次執行會下載多語系模型，之後會直接使用 `.cache` 裡的檔案。

## 測試自己的輸入

```powershell
.\run_test.ps1 --state "玩家放下武器並舉起雙手，守衛目前沒有受到攻擊。"
```

或使用 JSON 狀態檔：

```powershell
.\run_test.ps1 --state-file .\example_state.json
```

強制用 CPU：

```powershell
.\run_test.ps1 --cpu
```

若 PowerShell 阻擋腳本，可只對這一次執行放寬：

```powershell
powershell -ExecutionPolicy Bypass -File .\run_test.ps1
```
