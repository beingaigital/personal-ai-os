# 更新日志

所有重要的项目变更都会记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## [1.1.0] - 2025-11-14

### 新增
- 🚀 信息提炼模块支持并发读取，提升多文件处理效率
- 📄 新增对 PDF、Word（.docx）、TXT、Markdown 文件的统一支持
- 🧩 `load_kimi_client` 支持模型覆盖，不同功能可选择不同模型

### 更新
- 📦 新增依赖 `pypdf`、`python-docx`
- 📘 文档更新（README、SETUP）以反映新特性与依赖
- 📁 新增配置说明，默认使用 `kimi-k2-thinking`，信息提炼覆盖为 `kimi-latest`

---

## [1.0.0] - 2025-11-14

### 新增
- ✨ 基于 Kimi K2 API 的完整工作流系统
- ✨ 信息提炼功能（Ingest）：自动处理 Markdown 文件并生成摘要
- ✨ 深度分析功能（Super Analyst）：使用多种分析框架进行结构化分析
  - 支持 12 种分析框架（First Principles, 5 Whys, SWOT, MECE 等）
  - 智能框架选择器自动推荐最适合的分析框架
- ✨ 广度思考功能（New Angle）：多维度洞察分析
  - 盲点分析
  - 视角转换
  - 跨领域类比
  - 新洞见生成
- ✨ 统一的中文输出格式
- ✨ 命令行界面（CLI）支持所有功能
- ✨ 完整的配置系统（支持环境变量）

### 技术特性
- 使用 Python 标准库实现，无外部依赖
- 支持 OpenAI 兼容的 API 格式
- 内置重试机制和错误处理
- 模块化设计，易于扩展

### 文档
- 📚 完整的 README 文档
- 📚 技术需求文档
- 📚 设置指南（SETUP.md）
- 📚 配置模板文件

### 安全
- 🔒 敏感配置文件已加入 .gitignore
- 🔒 支持环境变量管理 API 密钥
- 🔒 配置模板文件（.example）供参考

---

## 未来计划

### 计划中
- [ ] 支持更多 LLM 提供商
- [ ] Web UI 界面
- [ ] 数据持久化和历史记录
- [ ] 批量处理功能
- [ ] 导出多种格式（PDF, HTML 等）

### 考虑中
- [ ] 插件系统
- [ ] 自定义分析框架
- [ ] 协作功能
- [ ] 云端同步

