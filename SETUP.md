# 项目设置指南

## 快速开始

### 1. 克隆项目后，复制配置文件模板

```bash
cp config/kimi_api.json.example config/kimi_api.json
```

### 2. 编辑配置文件

编辑 `config/kimi_api.json`，确保配置正确（通常只需要设置环境变量即可）。

### 3. 设置环境变量

```bash
export KIMI_API_KEY="your_kimi_api_key_here"
```

或者创建 `.env` 文件（如果使用 python-dotenv）：
```bash
KIMI_API_KEY=your_kimi_api_key_here
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

### 5. 创建必要的目录

目录结构会自动创建，但如果你想手动创建：

```bash
mkdir -p data/raw data/medium-rare data/topic/new-angle logs
```

## 注意事项

- **不要提交** `config/kimi_api.json` 到 Git（已加入 .gitignore）
- 使用 `config/kimi_api.json.example` 作为配置模板
- 所有用户数据（`data/` 目录）不会被提交到 Git
- 支持的原始文件格式：Markdown、TXT、PDF、Word（.docx）

