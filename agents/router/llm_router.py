"""
LLM Router - 基于LLM的智能路由决策引擎
根据任务描述智能选择最合适的Agent
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

# Add project root to path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from scripts.kimi_client import load_kimi_client

CONFIG_DIR = ROOT / "config"


class LLMRouter:
    """基于LLM的智能路由决策引擎"""

    def __init__(self, config_path: Optional[str] = None):
        """初始化LLM路由器"""
        if config_path is None:
            config_path = str(CONFIG_DIR / "kimi_api.json")
        self.client = load_kimi_client(config_path, model_override="kimi-k2-thinking")

    def select_agents(
        self,
        task: str,
        input_data: Optional[Dict[str, Any]] = None,
        available_agents: Optional[List[str]] = None,
    ) -> List[str]:
        """
        根据任务描述选择最合适的Agent

        Args:
            task: 用户任务描述
            input_data: 输入数据信息
            available_agents: 可用的Agent列表

        Returns:
            选中的Agent ID列表
        """
        if available_agents is None:
            available_agents = ["ingest", "super_analyst", "new_angle"]

        # 构建路由提示词
        agent_descriptions = {
            "ingest": "摘要提炼代理：处理原始文档（Markdown、PDF、Word、TXT），生成包含Summary、Key Takeaways、Something New的结构化摘要。适用于文档整理、信息提炼任务。",
            "super_analyst": "深度分析代理：使用多种分析框架（First Principles、SWOT、MECE等）进行结构化深度分析。适用于问题分析、战略思考、决策支持任务。",
            "new_angle": "广度思考代理：提供多维度视角、盲点分析、跨领域类比和创新洞察。适用于寻找新视角、发现盲点、创新思考任务。",
        }

        input_type = input_data.get("type", "text") if input_data else "text"
        input_value = input_data.get("value", "") if input_data else ""

        prompt = f"""你是一个智能Agent路由器，需要根据用户任务选择最合适的Agent。

可用Agent：
{chr(10).join(f"- {agent_id}: {agent_descriptions.get(agent_id, '')}" for agent_id in available_agents)}

用户任务：{task}
输入类型：{input_type}
输入内容预览：{input_value[:200] if input_value else '无'}

请分析任务需求，选择最合适的Agent（可以选1-3个）。返回JSON格式：
{{
  "selected_agents": ["agent_id1", "agent_id2"],
  "reasoning": "选择理由"
}}

只返回JSON，不要其他文字。"""

        messages = [
            {
                "role": "system",
                "content": "你是一个专业的Agent路由决策系统。请根据任务特征准确选择最合适的Agent。只返回JSON格式的决策结果。",
            },
            {"role": "user", "content": prompt},
        ]

        try:
            response = self.client.chat_completion(messages)
            # 尝试解析JSON响应
            response = response.strip()
            # 移除可能的markdown代码块标记
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()

            result = json.loads(response)
            selected = result.get("selected_agents", [])

            # 验证选中的Agent是否在可用列表中
            selected = [a for a in selected if a in available_agents]
            if not selected:
                # 默认选择第一个
                selected = [available_agents[0]]

            return selected
        except Exception as e:
            # 如果LLM路由失败，使用基于关键词的简单路由
            return self._fallback_routing(task, input_type, available_agents)

    def _fallback_routing(
        self, task: str, input_type: str, available_agents: List[str]
    ) -> List[str]:
        """回退路由：基于关键词的简单路由"""
        task_lower = task.lower()

        # 关键词匹配
        if any(
            kw in task_lower
            for kw in ["摘要", "提炼", "总结", "文档", "文件", "整理", "ingest", "summarize"]
        ) or input_type in ["file_path", "text"]:
            if "ingest" in available_agents:
                return ["ingest"]

        if any(
            kw in task_lower
            for kw in [
                "分析",
                "框架",
                "战略",
                "问题",
                "决策",
                "评估",
                "analyze",
                "analysis",
                "framework",
            ]
        ):
            if "super_analyst" in available_agents:
                return ["super_analyst"]

        if any(
            kw in task_lower
            for kw in [
                "视角",
                "盲点",
                "创新",
                "洞察",
                "新角度",
                "类比",
                "insight",
                "angle",
                "perspective",
            ]
        ):
            if "new_angle" in available_agents:
                return ["new_angle"]

        # 默认返回第一个
        return [available_agents[0]] if available_agents else []




