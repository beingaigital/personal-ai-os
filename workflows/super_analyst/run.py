from __future__ import annotations

import sys
from pathlib import Path
from typing import List, Dict
from datetime import datetime

# Add project root to path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from .framework_selector import recommend_frameworks
from scripts.kimi_client import load_kimi_client
DATA_DIR = ROOT / "data"
TOPIC_DIR = DATA_DIR / "topic"
PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"
CONFIG_DIR = ROOT / "config"


def _load_prompt(template_name: str) -> str:
    path = PROMPTS_DIR / template_name
    return path.read_text(encoding="utf-8")


def _render_prompt(base_prompt: str, question: str) -> str:
    return base_prompt.replace("{{QUESTION}}", question)


def _assemble_messages(topic: str, question: str, prompt_text: str):
    system = "你是一位专业的分析师。请严格按照框架要求，生成结构化的、基于证据的分析报告。\n\n重要：请使用中文撰写所有分析内容，包括标题、正文、结论等所有部分。"
    user = f"主题：{topic}\n\n问题：\n{question}\n\n框架提示词：\n{prompt_text}\n\n请使用中文完成分析报告。"
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def _report_header(topic: str, frameworks: List[str]) -> str:
    now = datetime.now().strftime("%Y-%m-%d")
    return (
        f"# {topic}-分析报告\n\n"
        f"- 日期：{now}\n"
        f"- 使用框架：{', '.join(frameworks)}\n"
        f"- 生成引擎：Kimi K2\n\n"
        f"---\n\n"
    )


def run_super_analyst(topic: str, question: str) -> Path:
    TOPIC_DIR.mkdir(parents=True, exist_ok=True)
    # 深度分析功能使用 kimi-k2-thinking 模型（配置文件默认值）
    kimi = load_kimi_client(str(CONFIG_DIR / "kimi_api.json"))

    recs = recommend_frameworks(question, top_n=3)
    frameworks_used: List[str] = []
    sections: List[str] = []

    for rec in recs:
        template = _load_prompt(rec["prompt_template"])
        prompt_text = _render_prompt(template, question)
        messages = _assemble_messages(topic, question, prompt_text)
        content = kimi.chat_completion(messages)
        sections.append(f"## {rec['name']}\n\n{content}\n")
        frameworks_used.append(rec["name"])

    report_md = _report_header(topic, frameworks_used) + "\n\n".join(sections)
    out_path = TOPIC_DIR / f"{topic}.md"
    out_path.write_text(report_md, encoding="utf-8")
    return out_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run Super Analyst workflow")
    parser.add_argument("--topic", type=str, required=True)
    parser.add_argument("--question", type=str, required=True)
    args = parser.parse_args()
    p = run_super_analyst(args.topic, args.question)
    print(str(p))


