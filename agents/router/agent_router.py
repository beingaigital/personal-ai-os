"""
Agent Router - 主路由器
负责接收用户请求并智能路由到相应的子代理
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

from .llm_router import LLMRouter

# 延迟导入以避免循环依赖
# from ..ingest.ingest_agent import IngestAgent
# from ..super_analyst.super_analyst_agent import SuperAnalystAgent
# from ..new_angle.new_angle_agent import NewAngleAgent


class AgentRouter:
    """主路由器，负责智能路由和协调子代理"""

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化Agent Router

        Args:
            config_path: 路由器配置文件路径
        """
        self.config_path = config_path
        self.config = self._load_config()
        self.llm_router = LLMRouter()
        self._agents = {}  # 延迟加载Agent实例

    def _load_config(self) -> Dict[str, Any]:
        """加载路由器配置"""
        if self.config_path is None:
            config_file = Path(__file__).resolve().parents[3] / "config" / "router_config.json"
        else:
            config_file = Path(self.config_path)

        if config_file.exists():
            with open(config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            # 返回默认配置
            return {
                "router": {
                    "decision_engine": "llm",
                    "default_model": "kimi-k2-thinking",
                    "max_agents_per_task": 3,
                    "enable_sequential_execution": False,
                },
                "agents": {
                    "ingest": {"enabled": True, "model": "kimi-latest", "priority": 1},
                    "super_analyst": {
                        "enabled": True,
                        "model": "kimi-k2-thinking",
                        "priority": 2,
                    },
                    "new_angle": {
                        "enabled": True,
                        "model": "kimi-k2-thinking",
                        "priority": 3,
                    },
                },
            }

    def _get_agent(self, agent_id: str):
        """获取Agent实例（延迟加载）"""
        if agent_id in self._agents:
            return self._agents[agent_id]

        # 动态导入Agent类
        if agent_id == "ingest":
            from ..ingest.ingest_agent import IngestAgent

            self._agents[agent_id] = IngestAgent()
        elif agent_id == "super_analyst":
            from ..super_analyst.super_analyst_agent import SuperAnalystAgent

            self._agents[agent_id] = SuperAnalystAgent()
        elif agent_id == "new_angle":
            from ..new_angle.new_angle_agent import NewAngleAgent

            self._agents[agent_id] = NewAngleAgent()
        else:
            raise ValueError(f"Unknown agent ID: {agent_id}")

        return self._agents[agent_id]

    def route_and_execute(
        self,
        task: str,
        input_data: Optional[Dict[str, Any]] = None,
        preferences: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        路由任务并执行

        Args:
            task: 用户任务描述
            input_data: 输入数据
            preferences: 用户偏好设置

        Returns:
            执行结果
        """
        if input_data is None:
            input_data = {}
        if preferences is None:
            preferences = {}

        # 获取可用Agent列表
        available_agents = [
            agent_id
            for agent_id, agent_config in self.config.get("agents", {}).items()
            if agent_config.get("enabled", True)
        ]

        # 检查用户是否指定了Agent
        agent_hint = preferences.get("agent_hint", "auto")
        if agent_hint != "auto" and agent_hint in available_agents:
            selected_agents = [agent_hint]
        else:
            # 使用LLM路由器选择Agent
            selected_agents = self.llm_router.select_agents(
                task, input_data, available_agents
            )

        # 限制Agent数量
        max_agents = preferences.get("max_agents", self.config["router"]["max_agents_per_task"])
        selected_agents = selected_agents[:max_agents]

        # 构建执行计划
        execution_plan = []
        for idx, agent_id in enumerate(selected_agents):
            execution_plan.append(
                {
                    "agent_id": agent_id,
                    "order": idx + 1,
                    "input": self._prepare_agent_input(agent_id, task, input_data),
                }
            )

        # 执行Agent
        results = []
        sequential = preferences.get("sequential", False)

        for plan_item in execution_plan:
            agent_id = plan_item["agent_id"]
            agent_input = plan_item["input"]

            try:
                agent = self._get_agent(agent_id)
                start_time = time.time()

                # 执行Agent
                if agent_id == "ingest":
                    output = agent.execute(week_path=agent_input.get("week_path"))
                elif agent_id == "super_analyst":
                    output = agent.execute(
                        topic=agent_input.get("topic"),
                        question=agent_input.get("question"),
                    )
                elif agent_id == "new_angle":
                    output = agent.execute(context=agent_input.get("context"))

                execution_time = time.time() - start_time

                results.append(
                    {
                        "agent_id": agent_id,
                        "output": output,
                        "execution_time": execution_time,
                    }
                )

                # 如果是顺序执行，将前一个Agent的输出作为下一个Agent的输入
                if sequential and len(results) > 0:
                    prev_output = results[-1]["output"]
                    if isinstance(prev_output, dict) and "output_path" in prev_output:
                        # 读取前一个Agent的输出文件作为下一个Agent的输入
                        if agent_id == "new_angle" and "output_path" in prev_output:
                            with open(prev_output["output_path"], "r", encoding="utf-8") as f:
                                input_data["value"] = f.read()
                                input_data["type"] = "text"

            except Exception as e:
                results.append(
                    {
                        "agent_id": agent_id,
                        "error": str(e),
                        "execution_time": 0,
                    }
                )

        # 聚合结果
        aggregated_result = self._aggregate_results(results)

        return {
            "selected_agents": selected_agents,
            "execution_plan": execution_plan,
            "results": results,
            "aggregated_result": aggregated_result,
        }

    def _prepare_agent_input(
        self, agent_id: str, task: str, input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """为Agent准备输入数据"""
        agent_input = {}

        if agent_id == "ingest":
            # Ingest Agent需要week_path
            if input_data.get("type") == "file_path":
                week_path = input_data.get("value", "")
                agent_input["week_path"] = week_path
            else:
                # 尝试从task中提取路径，或使用默认路径
                agent_input["week_path"] = input_data.get("week_path", "")

        elif agent_id == "super_analyst":
            # Super Analyst需要topic和question
            agent_input["topic"] = input_data.get("topic", task[:50])  # 使用task前50字符作为topic
            agent_input["question"] = input_data.get("question", task)

        elif agent_id == "new_angle":
            # New Angle需要context
            if input_data.get("type") == "file_path":
                # 从文件读取
                file_path = input_data.get("value", "")
                if file_path:
                    with open(file_path, "r", encoding="utf-8") as f:
                        agent_input["context"] = f.read()
            else:
                agent_input["context"] = input_data.get("value", task)

        return agent_input

    def _aggregate_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """聚合多个Agent的执行结果"""
        aggregated = {
            "total_agents": len(results),
            "successful": len([r for r in results if "error" not in r]),
            "failed": len([r for r in results if "error" in r]),
            "total_time": sum(r.get("execution_time", 0) for r in results),
            "outputs": [],
        }

        for result in results:
            if "error" not in result:
                output = result.get("output", {})
                if isinstance(output, dict) and "output_path" in output:
                    aggregated["outputs"].append(output["output_path"])

        return aggregated




