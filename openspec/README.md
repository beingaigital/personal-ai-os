# OpenSpec: Personal AI OS Agent Architecture

本目录包含个人AI OS系统的OpenSpec规范文件，定义了Agent Router和三个SubAgent的架构规范。

## 文件结构

```
openspec/
├── README.md                  # 本文件
├── agent_router.yaml         # 主路由器规范
├── ingest_agent.yaml          # 摘要提炼代理规范
├── super_analyst_agent.yaml   # 深度分析代理规范
└── new_angle_agent.yaml       # 广度思考代理规范
```

## 架构概述

### Agent Router（主路由器）
- **职责**: 接收用户请求，分析任务需求，智能选择并协调子代理执行
- **能力**: 任务分析、代理选择、多代理编排、结果聚合

### SubAgents（子代理）

#### 1. Ingest Agent（摘要提炼代理）
- **职责**: 处理原始文档，生成结构化摘要
- **输入**: 周目录路径或文件列表
- **输出**: 包含Summary、Key Takeaways、Something New的Markdown文档
- **模型**: kimi-latest

#### 2. Super Analyst Agent（深度分析代理）
- **职责**: 使用多种分析框架进行深度分析
- **输入**: 主题和问题
- **输出**: 结构化分析报告
- **模型**: kimi-k2-thinking
- **框架**: 支持12种分析框架，智能选择Top-3

#### 3. New Angle Agent（广度思考代理）
- **职责**: 提供多维度视角和跨领域洞察
- **输入**: 上下文文本或文件
- **输出**: 包含盲点、视角、类比、创新的洞察报告
- **模型**: kimi-k2-thinking

## 使用OpenSpec生成代码

使用以下命令根据OpenSpec规范生成实现代码：

```bash
# 生成Agent Router
openspec generate --spec openspec/agent_router.yaml --output agents/router/

# 生成Ingest Agent
openspec generate --spec openspec/ingest_agent.yaml --output agents/ingest/

# 生成Super Analyst Agent
openspec generate --spec openspec/super_analyst_agent.yaml --output agents/super_analyst/

# 生成New Angle Agent
openspec generate --spec openspec/new_angle_agent.yaml --output agents/new_angle/

# 生成所有Agent
openspec generate --spec openspec/ --output agents/
```

## 扩展性

系统设计支持轻松添加新的SubAgent：

1. 创建新的OpenSpec规范文件（如 `openspec/custom_agent.yaml`）
2. 在 `agent_router.yaml` 中注册新代理
3. 使用OpenSpec生成代码
4. 实现代理逻辑

## 规范格式

OpenSpec使用YAML格式，包含以下主要部分：
- `name`: 代理名称
- `type`: 代理类型（router/subagent）
- `description`: 详细描述
- `capabilities`: 能力列表
- `input_schema`: 输入数据模式
- `output_schema`: 输出数据模式
- `implementation`: 实现细节
- `workflow`: 工作流步骤
- `error_handling`: 错误处理策略

## 版本信息

- OpenSpec版本: 1.0.0
- 系统版本: 1.0.0
- 最后更新: 2025-11-14




