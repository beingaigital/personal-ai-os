# OpenSpec 重构 - 完整命令清单

本文档列出了完成Agent Router架构重构所需的所有OpenSpec命令。

## 📋 快速执行（推荐）

```bash
# 一键执行所有步骤
cd /Users/biaowenhuang/Documents/personal_ai_os
./openspec/quick_start.sh
```

## 🔧 分步执行命令

### 1. 验证OpenSpec规范文件

```bash
# 验证所有规范文件
openspec validate openspec/agent_router.yaml
openspec validate openspec/ingest_agent.yaml
openspec validate openspec/super_analyst_agent.yaml
openspec validate openspec/new_angle_agent.yaml

# 或批量验证
openspec validate openspec/*.yaml
```

### 2. 生成Agent Router实现

```bash
openspec generate \
  --spec openspec/agent_router.yaml \
  --output agents/router/ \
  --template python-class \
  --language python
```

### 3. 生成Ingest Agent实现

```bash
openspec generate \
  --spec openspec/ingest_agent.yaml \
  --output agents/ingest/ \
  --template python-class \
  --language python
```

### 4. 生成Super Analyst Agent实现

```bash
openspec generate \
  --spec openspec/super_analyst_agent.yaml \
  --output agents/super_analyst/ \
  --template python-class \
  --language python
```

### 5. 生成New Angle Agent实现

```bash
openspec generate \
  --spec openspec/new_angle_agent.yaml \
  --output agents/new_angle/ \
  --template python-class \
  --language python
```

### 6. 批量生成所有Agent（推荐）

```bash
openspec generate \
  --spec openspec/ \
  --output agents/ \
  --template python-class \
  --language python \
  --recursive
```

### 7. 生成路由器配置文件

```bash
openspec generate-config \
  --spec openspec/agent_router.yaml \
  --output config/router_config.json \
  --format json
```

### 8. 生成测试文件

```bash
openspec generate-tests \
  --spec openspec/ \
  --output tests/agents/ \
  --framework pytest
```

### 9. 生成API文档

```bash
openspec docs \
  --spec openspec/ \
  --output docs/api/ \
  --format markdown
```

## 📝 完整命令序列（复制粘贴执行）

```bash
#!/bin/bash
# 完整重构命令序列

cd /Users/biaowenhuang/Documents/personal_ai_os

# 1. 验证规范
echo "验证OpenSpec规范..."
openspec validate openspec/*.yaml

# 2. 生成所有Agent
echo "生成Agent实现..."
openspec generate \
  --spec openspec/ \
  --output agents/ \
  --template python-class \
  --language python \
  --recursive

# 3. 生成配置
echo "生成配置文件..."
openspec generate-config \
  --spec openspec/agent_router.yaml \
  --output config/router_config.json \
  --format json

# 4. 生成测试
echo "生成测试文件..."
openspec generate-tests \
  --spec openspec/ \
  --output tests/agents/ \
  --framework pytest

# 5. 生成文档
echo "生成API文档..."
openspec docs \
  --spec openspec/ \
  --output docs/api/ \
  --format markdown

echo "✅ 重构完成！"
```

## 🎯 核心命令（最小集）

如果只需要生成核心代码，执行以下命令：

```bash
# 生成Agent Router
openspec generate --spec openspec/agent_router.yaml --output agents/router/

# 生成三个SubAgent
openspec generate --spec openspec/ingest_agent.yaml --output agents/ingest/
openspec generate --spec openspec/super_analyst_agent.yaml --output agents/super_analyst/
openspec generate --spec openspec/new_angle_agent.yaml --output agents/new_angle/
```

## 🔍 验证和检查命令

```bash
# 检查生成的代码结构
tree agents/

# 验证Python语法
python -m py_compile agents/**/*.py

# 检查导入
python -c "from agents.router import AgentRouter; print('✅ Import successful')"

# 运行测试
pytest tests/agents/ -v
```

## 📦 依赖安装（如需要）

```bash
# 安装OpenSpec CLI（如果使用）
pip install openspec-cli

# 或使用其他OpenSpec实现
# 参考具体工具的安装文档
```

## 🚀 使用新架构

重构完成后，使用新的Agent Router：

```bash
# 通过CLI使用（需要更新cli.py）
python -m scripts.cli router \
  --task "分析这些文档" \
  --input-type file_path \
  --input-value "data/raw/2025-01-06"

# 或直接使用Python
python -c "
from agents.router import AgentRouter
router = AgentRouter()
result = router.route_and_execute(
    task='分析文档',
    input_data={'type': 'file_path', 'value': 'data/raw/2025-01-06'}
)
print(result)
"
```

## 📚 相关文档

- `openspec/README.md` - 架构说明和概述
- `openspec/COMMANDS.md` - 详细命令参考
- `openspec/*.yaml` - OpenSpec规范文件

## ⚠️ 注意事项

1. **备份现有代码**: 执行重构前建议先提交当前代码
   ```bash
   git add .
   git commit -m "Backup before OpenSpec refactoring"
   ```

2. **检查OpenSpec版本**: 确保使用兼容的OpenSpec版本
   ```bash
   openspec --version
   ```

3. **手动实现备选**: 如果OpenSpec工具不可用，参考`COMMANDS.md`中的手动实现指南

4. **测试验证**: 生成代码后务必运行测试确保功能正常
   ```bash
   pytest tests/agents/ -v
   ```

## 🔄 回滚（如需要）

如果重构出现问题，可以回滚：

```bash
# 删除生成的agents目录
rm -rf agents/

# 恢复原有代码
git checkout HEAD -- scripts/cli.py workflows/
```




