"""
Ingest Agent - 摘要提炼代理
负责处理原始文档并生成结构化摘要
"""

from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional

# Add project root to path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from scripts.content_processor import summarize_week
from scripts.folder_manager import ensure_data_dirs, create_week_folder, get_current_week_folder


class IngestAgent:
    """摘要提炼代理"""

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化Ingest Agent

        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path or str(ROOT / "config" / "kimi_api.json")

    def execute(
        self,
        week_path: Optional[str] = None,
        files: Optional[list] = None,
        model_override: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        执行摘要提炼任务

        Args:
            week_path: 周目录路径（data/raw/YYYY-MM-DD/）
            files: 可选，直接指定文件列表
            model_override: 可选，覆盖默认模型

        Returns:
            执行结果字典
        """
        start_time = time.time()

        try:
            ensure_data_dirs()

            # 确定week_path：如果未指定，使用当前周（周一为基准）的文件夹
            if week_path:
                week_dir = Path(week_path).resolve()
            else:
                # 自动使用当前周文件夹（以周一为基准）
                week_dir = get_current_week_folder(auto_create=True)

            if not week_dir.exists():
                raise ValueError(f"周目录不存在: {week_dir}")

            # 执行摘要提炼
            output_path = summarize_week(week_dir)

            # 读取输出内容
            summary_content = output_path.read_text(encoding="utf-8")

            # 统计文件数量
            file_count = len(
                [
                    f
                    for f in week_dir.iterdir()
                    if f.is_file()
                    and f.suffix.lower() in {".md", ".markdown", ".txt", ".pdf", ".docx"}
                ]
            )

            processing_time = time.time() - start_time

            return {
                "output_path": str(output_path),
                "summary_content": summary_content,
                "file_count": file_count,
                "processing_time": processing_time,
                "status": "success",
            }

        except Exception as e:
            return {
                "output_path": None,
                "summary_content": None,
                "file_count": 0,
                "processing_time": time.time() - start_time,
                "status": "error",
                "error": str(e),
            }




