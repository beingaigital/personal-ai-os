# Agent Router 使用指南

## 概述

Agent Router 是个人AI OS系统的智能路由系统，可以根据任务描述自动选择最合适的Agent执行任务。系统包含三个SubAgent：

1. **Ingest Agent** - 摘要提炼代理
2. **Super Analyst Agent** - 深度分析代理  
3. **New Angle Agent** - 广度思考代理

## 快速开始

### 基本使用

```bash
# 使用Agent Router智能路由（自动选择Agent）
python -m scripts.cli router \
  --task "分析这些文档并生成摘要" \
  --input-type file_path \
  --input-value "data/raw/2025-01-06"
```

### 指定Agent

```bash
# 明确指定使用Ingest Agent
python -m scripts.cli router \
  --task "提炼这些文档" \
  --input-type file_path \
  --input-value "data/raw/2025-01-06" \
  --agent-hint ingest
```

### 深度分析任务

```bash
# 使用Super Analyst Agent进行深度分析
python -m scripts.cli router \
  --task "分析特斯拉Robotaxi的商业前景" \
  --topic "特斯拉Robotaxi分析报告" \
  --question "2026-2030年Robotaxi的商业前景与主要风险是什么？" \
  --agent-hint super_analyst
```

### 广度思考任务

```bash
# 使用New Angle Agent进行广度思考
python -m scripts.cli router \
  --task "从新角度分析这个战略" \
  --input-type text \
  --input-value "当前战略要点：..." \
  --agent-hint new_angle
```

### 多Agent协作

```bash
# 使用多个Agent协作（先分析，再寻找新角度）
python -m scripts.cli router \
  --task "深度分析并寻找新视角" \
  --topic "战略分析" \
  --question "如何提升产品竞争力？" \
  --max-agents 2 \
  --sequential
```

## 命令行参数

### router 命令参数

- `--task` (必需): 任务描述
- `--input-type`: 输入数据类型 (`file_path`, `text`, `question`, `context`)
- `--input-value`: 输入数据值
- `--topic`: 主题（用于super_analyst）
- `--question`: 问题（用于super_analyst）
- `--agent-hint`: Agent提示 (`ingest`, `super_analyst`, `new_angle`, `auto`)
- `--max-agents`: 最多使用的Agent数量（默认：1）
- `--sequential`: 顺序执行Agent（前一个的输出作为下一个的输入）
- `--json`: 以JSON格式输出结果

## Python API 使用

### 基本使用

```python
from agents.router import AgentRouter

# 创建路由器
router = AgentRouter()

# 执行任务
result = router.route_and_execute(
    task="分析这些文档",
    input_data={
        "type": "file_path",
        "value": "data/raw/2025-01-06"
    }
)

print(f"选中的Agent: {result['selected_agents']}")
print(f"执行结果: {result['results']}")
```

### 指定Agent

```python
result = router.route_and_execute(
    task="深度分析问题",
    input_data={
        "topic": "战略分析",
        "question": "如何提升竞争力？"
    },
    preferences={
        "agent_hint": "super_analyst"
    }
)
```

### 多Agent协作

```python
result = router.route_and_execute(
    task="分析并寻找新视角",
    input_data={
        "topic": "产品策略",
        "question": "如何优化用户体验？"
    },
    preferences={
        "max_agents": 2,
        "sequential": True  # 顺序执行
    }
)
```

## Agent 说明

### Ingest Agent

**功能**: 处理原始文档并生成结构化摘要

**输入**:
- `week_path`: 周目录路径（data/raw/YYYY-MM-DD/）

**输出**:
- `output_path`: 生成的摘要文件路径
- `summary_content`: 摘要内容
- `file_count`: 处理的文件数量

**使用场景**:
- 文档整理
- 信息提炼
- 周报生成

### Super Analyst Agent

**功能**: 使用多种分析框架进行深度分析

**输入**:
- `topic`: 分析主题
- `question`: 分析问题

**输出**:
- `output_path`: 分析报告路径
- `report_content`: 报告内容
- `frameworks_used`: 使用的分析框架列表

**使用场景**:
- 战略分析
- 问题诊断
- 决策支持

### New Angle Agent

**功能**: 提供多维度视角和跨领域洞察

**输入**:
- `context`: 上下文文本
- `input_file`: 输入文件路径（可选）

**输出**:
- `output_path`: 洞察报告路径
- `insights`: 结构化洞察（盲点、视角、类比、创新）

**使用场景**:
- 寻找新视角
- 发现盲点
- 创新思考

## 配置

路由器配置位于 `config/router_config.json`:

```json
{
  "router": {
    "decision_engine": "llm",
    "default_model": "kimi-k2-thinking",
    "max_agents_per_task": 3,
    "enable_sequential_execution": false
  },
  "agents": {
    "ingest": {
      "enabled": true,
      "model": "kimi-latest",
      "priority": 1
    },
    "super_analyst": {
      "enabled": true,
      "model": "kimi-k2-thinking",
      "priority": 2
    },
    "new_angle": {
      "enabled": true,
      "model": "kimi-k2-thinking",
      "priority": 3
    }
  }
}
```

## 向后兼容性

原有的CLI命令仍然可用：

```bash
# 直接使用Ingest
python -m scripts.cli ingest --week-path "data/raw/2025-01-06"

# 直接使用Super Analyst
python -m scripts.cli super-analyst --topic "分析" --question "问题"

# 直接使用New Angle
python -m scripts.cli new-angle --text "上下文"
```

## 扩展性

系统设计支持轻松添加新的SubAgent：

1. 创建新的Agent类（继承基础Agent接口）
2. 在 `config/router_config.json` 中注册
3. 在 `AgentRouter` 中添加路由逻辑
4. 更新OpenSpec规范文件

## 故障排除

### Agent选择不正确

如果自动选择的Agent不符合预期，可以使用 `--agent-hint` 明确指定。

### 多Agent执行失败

检查 `--sequential` 参数，确保Agent之间的数据传递正确。

### 配置文件错误

确保 `config/router_config.json` 格式正确，所有必需的Agent都已启用。




