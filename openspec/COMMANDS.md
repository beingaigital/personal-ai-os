# OpenSpec 重构命令参考

本文档提供了使用OpenSpec规范完成Agent Router架构重构所需的所有命令。

## 前提条件

确保已安装OpenSpec工具（如果使用）：
```bash
# 如果使用OpenSpec CLI工具
pip install openspec-cli

# 或者使用其他OpenSpec实现
```

## 步骤1: 生成Agent Router实现

```bash
# 生成主路由器代码
openspec generate \
  --spec openspec/agent_router.yaml \
  --output agents/router/ \
  --template python-class \
  --language python

# 或者使用完整路径
openspec generate \
  --spec /Users/biaowenhuang/Documents/personal_ai_os/openspec/agent_router.yaml \
  --output /Users/biaowenhuang/Documents/personal_ai_os/agents/router/
```

## 步骤2: 生成Ingest Agent实现

```bash
# 生成摘要提炼代理
openspec generate \
  --spec openspec/ingest_agent.yaml \
  --output agents/ingest/ \
  --template python-class \
  --language python
```

## 步骤3: 生成Super Analyst Agent实现

```bash
# 生成深度分析代理
openspec generate \
  --spec openspec/super_analyst_agent.yaml \
  --output agents/super_analyst/ \
  --template python-class \
  --language python
```

## 步骤4: 生成New Angle Agent实现

```bash
# 生成广度思考代理
openspec generate \
  --spec openspec/new_angle_agent.yaml \
  --output agents/new_angle/ \
  --template python-class \
  --language python
```

## 步骤5: 批量生成所有Agent

```bash
# 一次性生成所有代理
openspec generate \
  --spec openspec/ \
  --output agents/ \
  --template python-class \
  --language python \
  --recursive
```

## 步骤6: 生成配置文件

```bash
# 生成路由器配置文件
openspec generate-config \
  --spec openspec/agent_router.yaml \
  --output config/router_config.json \
  --format json
```

## 步骤7: 生成测试文件

```bash
# 为所有代理生成测试文件
openspec generate-tests \
  --spec openspec/ \
  --output tests/agents/ \
  --framework pytest
```

## 步骤8: 验证规范文件

```bash
# 验证所有OpenSpec文件的有效性
openspec validate openspec/agent_router.yaml
openspec validate openspec/ingest_agent.yaml
openspec validate openspec/super_analyst_agent.yaml
openspec validate openspec/new_angle_agent.yaml

# 或批量验证
openspec validate openspec/*.yaml
```

## 步骤9: 生成API文档

```bash
# 从OpenSpec生成API文档
openspec docs \
  --spec openspec/ \
  --output docs/api/ \
  --format markdown
```

## 完整重构流程（一键执行）

```bash
#!/bin/bash
# 完整重构脚本

set -e

echo "=== OpenSpec Agent架构重构 ==="

# 1. 验证规范文件
echo "1. 验证OpenSpec规范文件..."
openspec validate openspec/*.yaml

# 2. 生成所有Agent实现
echo "2. 生成Agent实现代码..."
openspec generate \
  --spec openspec/ \
  --output agents/ \
  --template python-class \
  --language python \
  --recursive

# 3. 生成配置文件
echo "3. 生成配置文件..."
openspec generate-config \
  --spec openspec/agent_router.yaml \
  --output config/router_config.json \
  --format json

# 4. 生成测试文件
echo "4. 生成测试文件..."
openspec generate-tests \
  --spec openspec/ \
  --output tests/agents/ \
  --framework pytest

# 5. 生成API文档
echo "5. 生成API文档..."
openspec docs \
  --spec openspec/ \
  --output docs/api/ \
  --format markdown

echo "=== 重构完成 ==="
```

## 手动实现方式（如果OpenSpec工具不可用）

如果OpenSpec CLI工具不可用，可以手动实现。参考以下目录结构：

```
agents/
├── __init__.py
├── router/
│   ├── __init__.py
│   ├── agent_router.py      # 主路由器实现
│   └── llm_router.py        # LLM决策引擎
├── ingest/
│   ├── __init__.py
│   └── ingest_agent.py       # 摘要提炼代理
├── super_analyst/
│   ├── __init__.py
│   └── super_analyst_agent.py  # 深度分析代理
└── new_angle/
    ├── __init__.py
    └── new_angle_agent.py    # 广度思考代理
```

## 集成到现有CLI

重构后，更新CLI以使用新的Agent Router：

```python
# scripts/cli.py 更新示例
from agents.router import AgentRouter

def cmd_router(args):
    router = AgentRouter()
    result = router.route_and_execute(
        task=args.task,
        input_data={
            "type": args.input_type,
            "value": args.input_value
        }
    )
    print(result)
```

## 验证重构结果

```bash
# 运行测试
pytest tests/agents/

# 检查代码质量
flake8 agents/
mypy agents/

# 运行示例
python -m scripts.cli router --task "分析这些文档" --input-type file_path --input-value "data/raw/2025-01-06"
```

## 注意事项

1. **向后兼容**: 确保新的Agent Router架构保持与现有CLI命令的兼容性
2. **配置迁移**: 将现有配置迁移到新的router_config.json格式
3. **测试覆盖**: 确保所有Agent都有充分的测试覆盖
4. **文档更新**: 更新README和SETUP文档以反映新架构

## 故障排除

如果遇到问题：

```bash
# 检查OpenSpec版本
openspec --version

# 查看详细日志
openspec generate --spec openspec/agent_router.yaml --output agents/router/ --verbose

# 验证Python环境
python --version
pip list | grep openspec
```




