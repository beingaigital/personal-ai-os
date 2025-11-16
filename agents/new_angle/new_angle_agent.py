"""
New Angle Agent - 广度思考代理
提供多维度视角和跨领域洞察
"""

from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional, List

# Add project root to path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from workflows.new_angle.run import run_new_angle


class NewAngleAgent:
    """广度思考代理"""

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化New Angle Agent

        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path or str(ROOT / "config" / "kimi_api.json")

    def execute(
        self,
        context: str,
        input_file: Optional[str] = None,
        focus_areas: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        执行广度思考任务

        Args:
            context: 上下文文本或分析结果
            input_file: 可选，从文件读取上下文
            focus_areas: 可选，指定重点关注的领域

        Returns:
            执行结果字典
        """
        start_time = time.time()

        try:
            # 确定上下文内容
            if input_file:
                context_path = Path(input_file)
                if context_path.exists():
                    context = context_path.read_text(encoding="utf-8")
                else:
                    raise ValueError(f"输入文件不存在: {input_file}")

            if not context or not context.strip():
                raise ValueError("上下文内容不能为空")

            # 如果有focus_areas，添加到context中
            if focus_areas:
                context += f"\n\n重点关注领域：{', '.join(focus_areas)}"

            # 执行广度思考
            output_path = run_new_angle(context_text=context)

            # 读取输出内容
            output_content = output_path.read_text(encoding="utf-8")

            # 解析洞察（尝试从输出中提取结构化信息）
            insights = self._parse_insights(output_content)

            execution_time = time.time() - start_time

            return {
                "output_path": str(output_path),
                "insights": insights,
                "execution_time": execution_time,
                "status": "success",
            }

        except Exception as e:
            return {
                "output_path": None,
                "insights": {},
                "execution_time": time.time() - start_time,
                "status": "error",
                "error": str(e),
            }

    def _parse_insights(self, content: str) -> Dict[str, str]:
        """从输出内容中解析结构化洞察"""
        insights = {
            "blind_spots": "",
            "perspectives": "",
            "analogies": "",
            "innovations": "",
        }

        # 尝试提取各个部分（基于常见的标题模式）
        lines = content.split("\n")
        current_section = None
        current_content = []

        for line in lines:
            line_lower = line.lower()
            if any(kw in line_lower for kw in ["盲点", "blind spot", "遗漏"]):
                if current_section:
                    insights[current_section] = "\n".join(current_content)
                current_section = "blind_spots"
                current_content = []
            elif any(kw in line_lower for kw in ["视角", "perspective", "角度"]):
                if current_section:
                    insights[current_section] = "\n".join(current_content)
                current_section = "perspectives"
                current_content = []
            elif any(kw in line_lower for kw in ["类比", "analogy", "借鉴"]):
                if current_section:
                    insights[current_section] = "\n".join(current_content)
                current_section = "analogies"
                current_content = []
            elif any(kw in line_lower for kw in ["创新", "innovation", "洞察", "insight"]):
                if current_section:
                    insights[current_section] = "\n".join(current_content)
                current_section = "innovations"
                current_content = []
            else:
                current_content.append(line)

        if current_section:
            insights[current_section] = "\n".join(current_content)

        # 如果没有解析到结构化内容，返回完整内容
        if not any(insights.values()):
            insights["full_content"] = content

        return insights




