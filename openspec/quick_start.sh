#!/bin/bash
# OpenSpec Agent架构重构 - 快速开始脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_ROOT"

echo "=========================================="
echo "OpenSpec Agent架构重构"
echo "=========================================="
echo ""

# 检查OpenSpec是否安装
if ! command -v openspec &> /dev/null; then
    echo "⚠️  OpenSpec CLI未安装，将使用手动实现方式"
    echo "   安装命令: pip install openspec-cli"
    echo ""
    MANUAL_MODE=true
else
    echo "✅ OpenSpec CLI已安装"
    MANUAL_MODE=false
    echo ""
fi

# 步骤1: 验证规范文件
echo "步骤1: 验证OpenSpec规范文件..."
if [ "$MANUAL_MODE" = false ]; then
    openspec validate openspec/*.yaml || {
        echo "❌ 规范文件验证失败"
        exit 1
    }
    echo "✅ 规范文件验证通过"
else
    echo "⏭️  跳过验证（手动模式）"
fi
echo ""

# 步骤2: 创建agents目录结构
echo "步骤2: 创建agents目录结构..."
mkdir -p agents/{router,ingest,super_analyst,new_angle}
touch agents/__init__.py
touch agents/router/__init__.py
touch agents/ingest/__init__.py
touch agents/super_analyst/__init__.py
touch agents/new_angle/__init__.py
echo "✅ 目录结构创建完成"
echo ""

# 步骤3: 生成Agent实现
if [ "$MANUAL_MODE" = false ]; then
    echo "步骤3: 生成Agent实现代码..."
    openspec generate \
        --spec openspec/ \
        --output agents/ \
        --template python-class \
        --language python \
        --recursive || {
        echo "⚠️  OpenSpec生成失败，请手动实现"
        MANUAL_MODE=true
    }
    if [ "$MANUAL_MODE" = false ]; then
        echo "✅ Agent实现代码生成完成"
    fi
else
    echo "步骤3: 准备手动实现模板..."
    echo "   请参考 openspec/COMMANDS.md 中的手动实现指南"
fi
echo ""

# 步骤4: 生成配置文件
echo "步骤4: 生成配置文件..."
if [ "$MANUAL_MODE" = false ] && command -v openspec &> /dev/null; then
    openspec generate-config \
        --spec openspec/agent_router.yaml \
        --output config/router_config.json \
        --format json || {
        echo "⚠️  配置文件生成失败，将创建模板"
    }
fi

# 创建默认配置文件模板
if [ ! -f config/router_config.json ]; then
    cat > config/router_config.json << 'EOF'
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
EOF
    echo "✅ 配置文件模板创建完成"
else
    echo "✅ 配置文件已存在"
fi
echo ""

# 步骤5: 创建测试目录
echo "步骤5: 创建测试目录..."
mkdir -p tests/agents
echo "✅ 测试目录创建完成"
echo ""

# 步骤6: 更新.gitignore
echo "步骤6: 更新.gitignore..."
if ! grep -q "agents/__pycache__" .gitignore 2>/dev/null; then
    echo "" >> .gitignore
    echo "# Agents" >> .gitignore
    echo "agents/__pycache__/" >> .gitignore
    echo "agents/*/__pycache__/" >> .gitignore
    echo "✅ .gitignore已更新"
else
    echo "✅ .gitignore已包含agents相关规则"
fi
echo ""

# 完成
echo "=========================================="
echo "✅ 重构准备完成！"
echo "=========================================="
echo ""
echo "下一步："
echo "1. 如果使用OpenSpec CLI，代码已自动生成"
echo "2. 如果手动实现，请参考 openspec/COMMANDS.md"
echo "3. 实现Agent Router和各个SubAgent"
echo "4. 更新 scripts/cli.py 以使用新的Agent Router"
echo "5. 运行测试: pytest tests/agents/"
echo ""
echo "查看详细文档:"
echo "  - openspec/README.md - 架构说明"
echo "  - openspec/COMMANDS.md - 命令参考"
echo ""




