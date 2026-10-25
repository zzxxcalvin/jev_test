"""Laya 本機推論測試：把遊戲世界狀態分類成可供 UE5 執行的決策。"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
CACHE_DIR = PROJECT_DIR / ".cache" / "huggingface"

# 必須在 import laya 前設定，確保模型不會下載到 C:\Users\...\.cache。
os.environ.setdefault("HF_HOME", str(CACHE_DIR))
os.environ.setdefault("HF_HUB_CACHE", str(CACHE_DIR / "hub"))
os.environ.setdefault("TRANSFORMERS_CACHE", str(CACHE_DIR / "transformers"))
os.environ.setdefault("USE_TF", "0")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

import laya  # noqa: E402
import torch  # noqa: E402


DEFAULT_STATE = {
    "角色": "城市守衛",
    "生命值百分比": 28,
    "彈藥百分比": 55,
    "玩家距離公尺": 12,
    "玩家狀態": "持有武器，剛攻擊另一名守衛",
    "隊友": "附近有一名健康隊友",
    "環境": "右側有掩體，北側出口可以呼叫增援",
    "最近事件": "守衛在兩秒前受到玩家攻擊",
}


QUESTIONS = {
    "戰術": {
        "type": "choice",
        "instructions": "根據遊戲狀態，守衛現在最合理的主要戰術是什麼？",
        "criteria": {
            "追擊": "主動靠近並持續攻擊玩家",
            "尋找掩體": "先移動到安全掩體再觀察或反擊",
            "呼叫增援": "通知其他守衛前來支援",
            "守住出口": "阻止玩家經由出口離開",
            "撤退": "脫離戰鬥並移動到安全位置",
        },
    },
    "威脅程度": {
        "type": "score",
        "instructions": "玩家目前對守衛造成的威脅程度有多高？",
        "criteria": ["很低", "偏低", "中等", "偏高", "極高"],
    },
    "需要支援": {
        "type": "noul",
        "instructions": "守衛現在是否應該呼叫支援？",
        "criteria": {
            "false": "不需要呼叫支援",
            "true": "需要呼叫支援",
        },
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="執行 Laya 多語系模型的 UE5 NPC 決策測試")
    parser.add_argument(
        "--state",
        help="自訂狀態文字；未指定時使用腳本內的守衛範例",
    )
    parser.add_argument(
        "--state-file",
        type=Path,
        help="讀取 UTF-8 JSON 或純文字狀態檔",
    )
    parser.add_argument(
        "--cpu",
        action="store_true",
        help="強制使用 CPU（預設會在可用時使用 CUDA）",
    )
    return parser.parse_args()


def load_state(args: argparse.Namespace):
    if args.state_file:
        raw = args.state_file.read_text(encoding="utf-8")
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return raw
    return args.state if args.state else DEFAULT_STATE


def main() -> None:
    args = parse_args()
    state = load_state(args)
    device = "cpu" if args.cpu or not torch.cuda.is_available() else "cuda"

    print(f"Laya version : {laya.__version__}")
    print(f"Torch version: {torch.__version__}")
    print(f"Device       : {device}")
    if device == "cuda":
        print(f"GPU          : {torch.cuda.get_device_name(0)}")
    print("\n輸入狀態：")
    print(json.dumps(state, ensure_ascii=False, indent=2) if not isinstance(state, str) else state)
    print("\n載入多語系模型（第一次執行會下載約 650 MB 到專案的 .cache）...")

    agent = laya.load("convaiinnovations/laya-multilingual", device=device)
    result = agent.predict(state, QUESTIONS)

    print("\n模型回覆：")
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
