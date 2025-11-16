from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Optional
import sys

from .folder_manager import (
    ensure_data_dirs,
    create_week_folder,
    get_current_week_folder,
    get_week_folder_info,
    list_raw_folders,
)

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


def cmd_week_folder(args: argparse.Namespace) -> None:
    """获取或创建当前周的文件夹"""
    ensure_data_dirs()
    
    if args.info:
        # 显示详细信息
        info = get_week_folder_info()
        if args.json:
            print(json.dumps(info, ensure_ascii=False, indent=2))
        else:
            print(f"📅 当前周: {info['week_range']}")
            print(f"📁 文件夹路径: {info['folder_path']}")
            print(f"📄 文件数量: {info['file_count']}")
            print(f"✅ 文件夹存在: {'是' if info['folder_exists'] else '否'}")
            if not info['folder_exists']:
                print(f"\n💡 提示: 运行 'python -m scripts.cli week-folder' 创建文件夹")
    elif args.list:
        # 列出所有周文件夹
        folders = list_raw_folders()
        if args.json:
            folder_list = [{"path": str(f), "name": f.name} for f in folders]
            print(json.dumps({"folders": folder_list}, ensure_ascii=False, indent=2))
        else:
            if folders:
                print(f"📚 共有 {len(folders)} 个周文件夹:\n")
                for folder in folders:
                    info = get_week_folder_info(datetime.strptime(folder.name, "%Y-%m-%d"))
                    print(f"  📁 {folder.name} ({info['week_range']}) - {info['file_count']} 个文件")
            else:
                print("📚 暂无周文件夹")
    else:
        # 创建或获取当前周文件夹
        week_folder = get_current_week_folder(auto_create=True)
        if args.json:
            info = get_week_folder_info()
            print(json.dumps({"folder_path": str(week_folder), **info}, ensure_ascii=False, indent=2))
        else:
            print(f"✅ 当前周文件夹: {week_folder}")
            print(f"💡 提示: 将文档放入此文件夹，然后运行 'python -m scripts.cli ingest' 进行摘要处理")


def cmd_router(args: argparse.Namespace) -> None:
    """使用Agent Router智能路由并执行任务"""
    from agents.router import AgentRouter
    
    ensure_data_dirs()
    router = AgentRouter()
    
    # 准备输入数据
    input_data = {}
    if args.input_type:
        input_data["type"] = args.input_type
    if args.input_value:
        input_data["value"] = args.input_value
    if args.topic:
        input_data["topic"] = args.topic
    if args.question:
        input_data["question"] = args.question
    
    # 准备偏好设置
    preferences = {}
    if args.agent_hint:
        preferences["agent_hint"] = args.agent_hint
    if args.max_agents:
        preferences["max_agents"] = args.max_agents
    if args.sequential:
        preferences["sequential"] = True
    
    # 执行路由
    result = router.route_and_execute(
        task=args.task,
        input_data=input_data,
        preferences=preferences
    )
    
    # 输出结果
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"✅ 选中的Agent: {', '.join(result['selected_agents'])}")
        print(f"\n执行结果:")
        for r in result["results"]:
            agent_id = r["agent_id"]
            if "error" in r:
                print(f"  ❌ {agent_id}: {r['error']}")
            else:
                output = r.get("output", {})
                if isinstance(output, dict) and "output_path" in output:
                    print(f"  ✅ {agent_id}: {output['output_path']}")
                else:
                    print(f"  ✅ {agent_id}: 执行成功")
        
        if result["aggregated_result"]["outputs"]:
            print(f"\n生成的文件:")
            for path in result["aggregated_result"]["outputs"]:
                print(f"  📄 {path}")


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

    p_router = sub.add_parser("router", help="Use Agent Router to intelligently route and execute tasks")
    p_router.add_argument("--task", type=str, required=True, help="Task description")
    p_router.add_argument("--input-type", type=str, choices=["file_path", "text", "question", "context"], 
                         help="Input data type")
    p_router.add_argument("--input-value", type=str, help="Input data value")
    p_router.add_argument("--topic", type=str, help="Topic (for super_analyst)")
    p_router.add_argument("--question", type=str, help="Question (for super_analyst)")
    p_router.add_argument("--agent-hint", type=str, choices=["ingest", "super_analyst", "new_angle", "auto"],
                         default="auto", help="Hint which agent to use (default: auto)")
    p_router.add_argument("--max-agents", type=int, default=1, help="Maximum number of agents to use")
    p_router.add_argument("--sequential", action="store_true", help="Execute agents sequentially")
    p_router.add_argument("--json", action="store_true", help="Output result as JSON")
    p_router.set_defaults(func=cmd_router)

    p_week = sub.add_parser("week-folder", help="Get or create current week folder (Monday-based)")
    p_week.add_argument("--info", action="store_true", help="Show detailed information about current week folder")
    p_week.add_argument("--list", action="store_true", help="List all week folders")
    p_week.add_argument("--json", action="store_true", help="Output result as JSON")
    p_week.set_defaults(func=cmd_week_folder)

    return parser


def main(argv=None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main(sys.argv[1:])


