from __future__ import annotations

import argparse
from pathlib import Path
from typing import Optional
import sys

from .folder_manager import ensure_data_dirs, create_week_folder
from .content_processor import summarize_week

ROOT = Path(__file__).resolve().parents[1]


def cmd_ingest(args: argparse.Namespace) -> None:
    ensure_data_dirs()
    if args.week_path:
        week_dir = Path(args.week_path).resolve()
    else:
        week_dir = create_week_folder()
    out = summarize_week(week_dir)
    print(str(out))


def cmd_super_analyst(args: argparse.Namespace) -> None:
    from workflows.super_analyst.run import run_super_analyst
    ensure_data_dirs()
    out = run_super_analyst(topic=args.topic, question=args.question)
    print(str(out))


def cmd_new_angle(args: argparse.Namespace) -> None:
    from workflows.new_angle.run import run_new_angle
    ensure_data_dirs()
    ctx: Optional[str] = None
    if args.input:
        ctx = Path(args.input).read_text(encoding="utf-8")
    out = run_new_angle(context_text=ctx or args.text or "")
    print(str(out))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Personal AI OS CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_ingest = sub.add_parser("ingest", help="Summarize weekly raw markdowns into a Medium-Rare document")
    p_ingest.add_argument("--week-path", type=str, help="Path to data/raw/YYYY-MM-DD")
    p_ingest.set_defaults(func=cmd_ingest)

    p_sa = sub.add_parser("super-analyst", help="Run Super Analyst workflow to produce an analysis report")
    p_sa.add_argument("--topic", type=str, required=True, help="Topic name for the report file")
    p_sa.add_argument("--question", type=str, required=True, help="User question / problem statement")
    p_sa.set_defaults(func=cmd_super_analyst)

    p_na = sub.add_parser("new-angle", help="Run New Angle workflow to produce new insights")
    p_na.add_argument("--input", type=str, help="Path to a markdown file as context")
    p_na.add_argument("--text", type=str, help="Context text if no file is provided")
    p_na.set_defaults(func=cmd_new_angle)

    return parser


def main(argv=None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main(sys.argv[1:])


