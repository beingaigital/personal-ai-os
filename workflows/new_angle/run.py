from __future__ import annotations

import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.kimi_client import load_kimi_client

DATA_DIR = ROOT / "data"
TOPIC_DIR = DATA_DIR / "topic" / "new-angle"
PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"
CONFIG_DIR = ROOT / "config"


def _load_prompt() -> str:
    path = PROMPTS_DIR / "new_angle.md"
    return path.read_text(encoding="utf-8")


def run_new_angle(context_text: str) -> Path:
    TOPIC_DIR.mkdir(parents=True, exist_ok=True)
    # 广度思考功能使用 kimi-k2-thinking 模型（配置文件默认值）
    kimi = load_kimi_client(str(CONFIG_DIR / "kimi_api.json"))
    prompt = _load_prompt().replace("{{CONTEXT}}", context_text or "")
    messages = [
        {"role": "system", "content": "你是一位擅长拓展视角和发现盲点的分析师。请使用中文撰写所有分析内容，包括标题、正文、结论等所有部分。"},
        {"role": "user", "content": prompt + "\n\n重要：请使用中文完成所有分析内容。"},
    ]
    output = kimi.chat_completion(messages)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path = TOPIC_DIR / f"new-angle-{ts}.md"
    out_path.write_text(output, encoding="utf-8")
    return out_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run New Angle workflow")
    parser.add_argument("--text", type=str, help="Context text", default="")
    args = parser.parse_args()
    p = run_new_angle(args.text or "")
    print(str(p))


