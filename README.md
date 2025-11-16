## Personal AI OS (Kimi Workflow Edition)

**版本**: v1.1.0  
**最后更新**: 2025-11-14

本项目提供基于 Kimi K2 API 的本地工作流型个人 AI OS，用于：信息提炼、深度分析（Super Analyst）与广度思考（New Angle）。

### 1. 快速开始

1) 准备 Python 环境（3.10+）  
2) 安装依赖  
   ```bash
   pip install -r requirements.txt
   ```  
3) 设置环境变量（推荐使用 Shell 环境变量）

```bash
export KIMI_API_KEY="你的 Kimi API Key"
```

或复制 `ENV.example` 为 `ENV` / `.env`（如果使用你自己的加载方式）。

4) 目录与配置检查  
- `config/kimi_api.json`：LLM API 配置（默认针对 Kimi K2，可按需调整模型、base_url、endpoint_path、超时等）  
- `config/system_config.json`：系统配置（时区、周起始日等）
- `config/frameworks.json`（可选）：自定义框架库；若提供需确保 prompts 中存在对应模板或使用既有别名

5) 准备原始内容  
将 Markdown 文件放入 `data/raw/YYYY-MM-DD/`（以周一日期命名）。

### 2. CLI 使用

所有命令均在项目根目录执行：

#### 2.1 周文件夹管理（推荐工作流）

- **获取/创建当前周文件夹**（以周一为基准）
```bash
# 创建当前周文件夹并显示路径
python -m scripts.cli week-folder

# 查看当前周文件夹详细信息
python -m scripts.cli week-folder --info

# 列出所有周文件夹
python -m scripts.cli week-folder --list
```

**使用流程**：
1. 运行 `python -m scripts.cli week-folder` 获取当前周文件夹路径
2. 将平时搜集的重要文档放入该文件夹
3. 运行 `python -m scripts.cli ingest` 进行自动摘要处理

#### 2.2 摘要提炼

- **摘要提炼**（自动生成当周 `medium-rare/周文档.md`）
```bash
# 自动使用当前周文件夹（推荐）
python -m scripts.cli ingest

# 或指定周目录
python -m scripts.cli ingest --week-path "/绝对路径/data/raw/2025-01-06"
```

#### 2.3 Agent Router（智能路由）

- **使用智能路由自动选择合适的Agent**
```bash
# 智能路由到合适的Agent（推荐）
python -m scripts.cli router \
  --task "总结这周收集的文档" \
  --input-type file_path \
  --input-value "data/raw/2025-11-10"

# 指定使用Ingest Agent
python -m scripts.cli router \
  --task "处理文档并生成摘要" \
  --input-type file_path \
  --input-value "data/raw/2025-11-10" \
  --agent-hint ingest
```

#### 2.4 其他功能

- **深度分析**（Super Analyst 工作流）
```bash
python -m scripts.cli super-analyst \
  --topic "特斯拉Robotaxi分析报告" \
  --question "2026-2030年Robotaxi的商业前景与主要风险是什么？"
# 输出：data/topic/特斯拉Robotaxi分析报告.md
```

- **广度思考**（New Angle 工作流）
```bash
# 传入上下文文件
python -m scripts.cli new-angle --input "/绝对路径/context.md"
# 或直接传文本
python -m scripts.cli new-angle --text "当前战略要点：……"
# 输出：data/topic/new-angle/new-angle-时间戳.md
```

### 3. 功能说明

- 信息提炼：读取周目录下所有 Markdown / TXT / PDF / Word 文档，调用 Kimi K2 生成
  - Summary / Key Takeaways / Something New
  - 输出到 `data/medium-rare/YYYY-MM-DD.md`

- Super Analyst：智能选择 12 个分析框架的 Top-N 并执行
  - 模板位于 `workflows/super_analyst/prompts/`
  - 报告输出到 `data/topic/<topic>.md`

- New Angle：生成盲点、视角切换、类比、创新洞察
  - 模板 `workflows/new_angle/prompts/new_angle.md`
  - 输出到 `data/topic/new-angle/`

### 4. 目录结构

```text
data/
  raw/YYYY-MM-DD/*.md     # 原始内容（按周）
  medium-rare/*.md        # 提炼结果
  topic/*.md              # 深度分析报告
  topic/new-angle/*.md    # 广度思考输出
workflows/
  super_analyst/
    prompts/*.md
    framework_selector.py
    run.py
  new_angle/
    prompts/new_angle.md
    run.py
scripts/
  folder_manager.py
  content_processor.py
  kimi_client.py
  cli.py
config/
  kimi_api.json  # 可配置 endpoint_path 与超时
  system_config.json
  frameworks.json (可选)
logs/
```

### 5. 环境变量与配置

- 环境变量：
  - `KIMI_API_KEY`：访问 Kimi K2 API 的密钥（必填）
- `config/kimi_api.json`：
  - `base_url`、`model`、`default_temperature`、`max_tokens`、`endpoint_path`（默认 `/v1/chat/completions`）、`timeout`
- `config/system_config.json`：
  - `timezone`、`week_start`、`summary_sections` 等
- `config/frameworks.json`（可选）：
  - `frameworks` 数组，支持字段：`id`、`name`、`description`、`keywords`、`problem_types`、`complexity`、`expected_time`、`prompt_template`（若缺失将按 `<id>.md` 猜测并要求模板存在；也支持 `porter_five_forces` → `five_forces.md` 别名）

### 6. 常见问题

- Kimi API 报错/超时：已内置重试（最多3次），请检查网络及密钥有效性
- 输出为空或格式异常：检查模板是否存在、文本长度是否超限
- CLI 找不到模块：确保在项目根目录运行命令

### 7. 开发与测试

- 单元测试建议覆盖：
  - `folder_manager.py`、`content_processor.py`、`framework_selector.py`、`cli.py`
- 集成测试：
  - 模拟 Kimi API 响应进行端到端流程测试


