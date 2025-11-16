"""
Super Analyst Agent - 深度分析代理
使用多种分析框架进行结构化深度分析
"""

from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional, List

# Add project root to path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from workflows.super_analyst.run import run_super_analyst


class SuperAnalystAgent:
    """深度分析代理"""

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化Super Analyst Agent

        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path or str(ROOT / "config" / "kimi_api.json")

    def execute(
        self,
        topic: str,
        question: str,
        framework_hint: Optional[List[str]] = None,
        max_frameworks: int = 3,
    ) -> Dict[str, Any]:
        """
        执行深度分析任务

        Args:
            topic: 分析报告的主题名称
            question: 用户问题或问题陈述
            framework_hint: 可选，指定要使用的框架ID列表
            max_frameworks: 最多使用的框架数量

        Returns:
            执行结果字典
        """
        start_time = time.time()

        try:
            # 执行深度分析
            output_path = run_super_analyst(topic=topic, question=question)

            # 读取报告内容
            report_content = output_path.read_text(encoding="utf-8")

            # 提取使用的框架（从报告头部）
            frameworks_used = []
            if "使用框架：" in report_content:
                frameworks_line = [
                    line
                    for line in report_content.split("\n")
                    if "使用框架：" in line
                ][0]
                frameworks_used = [
                    f.strip()
                    for f in frameworks_line.split("使用框架：")[1].split(",")
                ]

            # 提取分析章节
            analysis_sections = []
            lines = report_content.split("\n")
            current_section = None
            current_content = []

            for line in lines:
                if line.startswith("## "):
                    if current_section:
                        analysis_sections.append(
                            {
                                "framework": current_section,
                                "content": "\n".join(current_content),
                            }
                        )
                    current_section = line[3:].strip()
                    current_content = []
                else:
                    current_content.append(line)

            if current_section:
                analysis_sections.append(
                    {
                        "framework": current_section,
                        "content": "\n".join(current_content),
                    }
                )

            execution_time = time.time() - start_time

            return {
                "output_path": str(output_path),
                "report_content": report_content,
                "frameworks_used": frameworks_used,
                "analysis_sections": analysis_sections,
                "execution_time": execution_time,
                "status": "success",
            }

        except Exception as e:
            return {
                "output_path": None,
                "report_content": None,
                "frameworks_used": [],
                "analysis_sections": [],
                "execution_time": time.time() - start_time,
                "status": "error",
                "error": str(e),
            }




