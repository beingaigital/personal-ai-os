"""
Personal AI OS - Agent System
基于OpenSpec规范的Agent架构实现
"""

from .router.agent_router import AgentRouter
from .ingest.ingest_agent import IngestAgent
from .super_analyst.super_analyst_agent import SuperAnalystAgent
from .new_angle.new_angle_agent import NewAngleAgent

__all__ = [
    "AgentRouter",
    "IngestAgent",
    "SuperAnalystAgent",
    "NewAngleAgent",
]

__version__ = "1.0.0"




