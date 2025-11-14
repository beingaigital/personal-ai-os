# 个人AI OS系统 - 完整实现

## 项目结构

```
personal-ai-os/
├── data/
│   ├── raw/                # 原始内容（按周归档）
│   ├── medium-rare/        # 提炼结果
│   └── topic/              # 深度分析报告
├── workflows/
│   ├── super_analyst/
│   │   ├── prompts/
│   │   ├── framework_selector.py
│   │   ├── run.py
│   │   └── pipeline.yaml
│   └── new_angle/
│       ├── prompts/
│       └── run.py
├── scripts/
│   ├── folder_manager.py
│   ├── content_processor.py
│   ├── kimi_client.py
│   └── cli.py
├── config/
│   ├── kimi_api.json
│   ├── system_config.json
│   └── frameworks.json
├── tests/
│   ├── test_folder_manager.py
│   ├── test_framework_selector.py
│   └── test_content_processor.py
├── logs/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

------

## 1. 项目配置文件

### `.env.example`

```env
KIMI_API_KEY=your_kimi_api_key_here
```

### `.gitignore`

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Config & Secrets
.env
config/kimi_api.json

# Logs
logs/*.log

# Data
data/raw/*
!data/raw/.gitkeep
data/medium-rare/*
!data/medium-rare/.gitkeep
data/topic/*
!data/topic/.gitkeep
```

### `requirements.txt`

```txt
httpx>=0.25.0
pydantic>=2.0.0
ruamel.yaml>=0.18.0
typer>=0.9.0
rich>=13.0.0
python-dotenv>=1.0.0
pytest>=7.4.0
pytest-httpx>=0.26.0
```

### `config/kimi_api.json`

```json
{
  "base_url": "https://api.moonshot.cn",
  "model": "moonshot-v1-32k",
  "api_key_env": "KIMI_API_KEY",
  "default_temperature": 0.7,
  "max_tokens": 4096,
  "endpoint_path": "/v1/chat/completions",
  "request_format": "openai"
}
```

### `config/system_config.json`

```json
{
  "timezone": "Asia/Shanghai",
  "week_start": "monday",
  "default_frameworks": ["first_principles", "swot"],
  "summary_sections": ["Summary", "Key Takeaways", "Something New"],
  "log_level": "INFO",
  "enable_parallel": false
}
```

### `config/frameworks.json`

```json
{
  "frameworks": [
    {
      "id": "first_principles",
      "name": "第一性原理分析",
      "description": "从基本假设出发重新构建问题",
      "keywords": ["本质", "基础", "假设", "重构"],
      "problem_types": ["strategic", "innovation", "fundamental"],
      "complexity": "high",
      "expected_time": "long"
    },
    {
      "id": "swot",
      "name": "SWOT分析",
      "description": "优势、劣势、机会、威胁分析",
      "keywords": ["优势", "劣势", "机会", "威胁", "竞争"],
      "problem_types": ["business", "strategic", "evaluation"],
      "complexity": "medium",
      "expected_time": "medium"
    },
    {
      "id": "five_whys",
      "name": "五问法",
      "description": "通过连续提问找到根本原因",
      "keywords": ["原因", "根源", "为什么"],
      "problem_types": ["problem_solving", "diagnosis"],
      "complexity": "low",
      "expected_time": "short"
    },
    {
      "id": "pestel",
      "name": "PESTEL分析",
      "description": "政治、经济、社会、技术、环境、法律因素分析",
      "keywords": ["宏观", "环境", "政策", "趋势"],
      "problem_types": ["strategic", "market_analysis"],
      "complexity": "high",
      "expected_time": "long"
    },
    {
      "id": "bcg_matrix",
      "name": "BCG矩阵",
      "description": "产品组合分析：明星、现金牛、问题、瘦狗",
      "keywords": ["产品", "组合", "市场份额", "增长"],
      "problem_types": ["business", "portfolio"],
      "complexity": "medium",
      "expected_time": "medium"
    },
    {
      "id": "porter_five_forces",
      "name": "波特五力模型",
      "description": "行业竞争结构分析",
      "keywords": ["竞争", "行业", "供应商", "买家", "替代品"],
      "problem_types": ["business", "competitive_analysis"],
      "complexity": "high",
      "expected_time": "long"
    },
    {
      "id": "mckinsey_7s",
      "name": "麦肯锡7S模型",
      "description": "组织效能分析：战略、结构、系统、风格、员工、技能、共享价值",
      "keywords": ["组织", "管理", "效能", "文化"],
      "problem_types": ["organizational", "management"],
      "complexity": "high",
      "expected_time": "long"
    },
    {
      "id": "cost_benefit",
      "name": "成本收益分析",
      "description": "量化评估决策的成本与收益",
      "keywords": ["成本", "收益", "ROI", "投资"],
      "problem_types": ["decision_making", "evaluation"],
      "complexity": "medium",
      "expected_time": "medium"
    },
    {
      "id": "scenario_planning",
      "name": "情景规划",
      "description": "构建多种未来情景以应对不确定性",
      "keywords": ["未来", "情景", "不确定性", "规划"],
      "problem_types": ["strategic", "forecasting"],
      "complexity": "high",
      "expected_time": "long"
    },
    {
      "id": "value_chain",
      "name": "价值链分析",
      "description": "分析企业创造价值的各个环节",
      "keywords": ["价值", "流程", "优化", "竞争力"],
      "problem_types": ["business", "operational"],
      "complexity": "medium",
      "expected_time": "medium"
    },
    {
      "id": "okr",
      "name": "OKR目标管理",
      "description": "目标与关键结果分析框架",
      "keywords": ["目标", "关键结果", "执行", "衡量"],
      "problem_types": ["goal_setting", "performance"],
      "complexity": "low",
      "expected_time": "short"
    },
    {
      "id": "lean_canvas",
      "name": "精益画布",
      "description": "快速验证商业模式",
      "keywords": ["商业模式", "创业", "验证", "迭代"],
      "problem_types": ["business", "innovation"],
      "complexity": "medium",
      "expected_time": "medium"
    }
  ]
}
```

------

## 2. 核心脚本实现

### `scripts/kimi_client.py`

```python
"""Kimi API客户端"""
import os
import json
import time
import logging
from typing import Optional, Dict, Any, List
from pathlib import Path
import httpx
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class KimiClient:
    """Kimi API客户端封装"""
    
    def __init__(self, config_path: str = "config/kimi_api.json"):
        """初始化客户端"""
        config_file = Path(config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"配置文件不存在: {config_path}")
        
        with open(config_file, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        # 从环境变量获取API Key
        api_key_env = self.config.get('api_key_env', 'KIMI_API_KEY')
        self.api_key = os.getenv(api_key_env)
        if not self.api_key:
            raise ValueError(f"未设置环境变量: {api_key_env}")
        
        self.base_url = self.config['base_url']
        self.model = self.config['model']
        self.timeout = self.config.get('timeout', 60)
        self.max_retries = self.config.get('max_retries', 3)
        self.retry_delay = self.config.get('retry_delay', 2)
        
        self.client = httpx.Client(timeout=self.timeout)
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """调用聊天完成API"""
        url = f"{self.base_url}/compatible-mode/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature or self.config['default_temperature'],
            "max_tokens": max_tokens or self.config['max_tokens'],
            "stream": stream
        }
        
        for attempt in range(self.max_retries):
            try:
                logger.info(f"调用Kimi API (尝试 {attempt + 1}/{self.max_retries})")
                response = self.client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                
                result = response.json()
                logger.info("API调用成功")
                return result
                
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP错误: {e.response.status_code} - {e.response.text}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    raise
            
            except httpx.TimeoutException:
                logger.error("请求超时")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    raise
            
            except Exception as e:
                logger.error(f"未知错误: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
                else:
                    raise
        
        raise Exception("API调用失败")
    
    def extract_content(self, response: Dict[str, Any]) -> str:
        """从响应中提取内容"""
        try:
            return response['choices'][0]['message']['content']
        except (KeyError, IndexError) as e:
            logger.error(f"解析响应失败: {e}")
            logger.error(f"响应内容: {response}")
            raise ValueError("无法从响应中提取内容")
    
    def close(self):
        """关闭客户端"""
        self.client.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
```

### `scripts/folder_manager.py`

```python
"""文件夹管理模块"""
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)


class FolderManager:
    """管理周文件夹结构"""
    
    def __init__(self, base_path: str = "data"):
        """初始化管理器"""
        self.base_path = Path(base_path)
        self.raw_path = self.base_path / "raw"
        self.medium_rare_path = self.base_path / "medium-rare"
        self.topic_path = self.base_path / "topic"
        
        # 确保基础目录存在
        self._ensure_directories()
    
    def _ensure_directories(self):
        """确保必要的目录存在"""
        for path in [self.raw_path, self.medium_rare_path, self.topic_path]:
            path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"确保目录存在: {path}")
    
    @staticmethod
    def get_week_monday(date: Optional[datetime] = None) -> datetime:
        """获取指定日期所在周的周一"""
        if date is None:
            date = datetime.now()
        
        # 计算到周一的天数
        days_to_monday = date.weekday()  # 0=周一, 6=周日
        monday = date - timedelta(days=days_to_monday)
        
        # 返回当天0点
        return monday.replace(hour=0, minute=0, second=0, microsecond=0)
    
    def get_week_folder_name(self, date: Optional[datetime] = None) -> str:
        """获取周文件夹名称（YYYY-MM-DD格式）"""
        monday = self.get_week_monday(date)
        return monday.strftime("%Y-%m-%d")
    
    def create_week_folder(self, date: Optional[datetime] = None) -> Path:
        """创建并返回周文件夹路径"""
        folder_name = self.get_week_folder_name(date)
        week_folder = self.raw_path / folder_name
        
        if not week_folder.exists():
            week_folder.mkdir(parents=True, exist_ok=True)
            logger.info(f"创建周文件夹: {week_folder}")
        else:
            logger.debug(f"周文件夹已存在: {week_folder}")
        
        return week_folder
    
    def get_week_folder(self, date: Optional[datetime] = None) -> Optional[Path]:
        """获取周文件夹路径（不创建）"""
        folder_name = self.get_week_folder_name(date)
        week_folder = self.raw_path / folder_name
        
        return week_folder if week_folder.exists() else None
    
    def list_week_folders(self) -> List[Path]:
        """列出所有周文件夹"""
        if not self.raw_path.exists():
            return []
        
        folders = []
        for item in sorted(self.raw_path.iterdir()):
            if item.is_dir() and self._is_valid_week_folder(item.name):
                folders.append(item)
        
        return folders
    
    @staticmethod
    def _is_valid_week_folder(name: str) -> bool:
        """验证是否为有效的周文件夹名称"""
        try:
            datetime.strptime(name, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def get_medium_rare_file(self, date: Optional[datetime] = None) -> Path:
        """获取提炼文档路径"""
        folder_name = self.get_week_folder_name(date)
        return self.medium_rare_path / f"{folder_name}.md"
    
    def get_topic_file(self, topic: str) -> Path:
        """获取主题分析报告路径"""
        # 清理主题名称
        safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_topic = safe_topic.replace(' ', '-')
        return self.topic_path / f"{safe_topic}-分析报告.md"
```

### `scripts/content_processor.py`

```python
"""内容处理模块"""
import logging
from pathlib import Path
from typing import List, Dict
from datetime import datetime

from .folder_manager import FolderManager
from .kimi_client import KimiClient

logger = logging.getLogger(__name__)


class ContentProcessor:
    """内容提炼处理器"""
    
    def __init__(self, folder_manager: FolderManager, kimi_client: KimiClient):
        """初始化处理器"""
        self.folder_manager = folder_manager
        self.kimi_client = kimi_client
    
    def collect_raw_files(self, week_path: Path) -> List[Dict[str, str]]:
        """收集周文件夹中的所有Markdown文件"""
        if not week_path.exists():
            logger.warning(f"周文件夹不存在: {week_path}")
            return []
        
        files = []
        for file_path in week_path.glob("*.md"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                files.append({
                    "name": file_path.name,
                    "path": str(file_path),
                    "content": content
                })
                logger.info(f"读取文件: {file_path.name}")
            
            except Exception as e:
                logger.error(f"读取文件失败 {file_path}: {e}")
        
        return files
    
    def process_single_file(self, file_content: str, file_name: str) -> Dict[str, str]:
        """处理单个文件并生成提炼结果"""
        system_prompt = """你是一个专业的信息提炼助手。请分析用户提供的文章内容，生成以下三个部分：

1. **Summary**（摘要）：用2-3句话概括文章的核心内容
2. **Key Takeaways**（关键要点）：列出3-5个最重要的观点或信息（使用列表）
3. **Something New**（新发现）：指出1-2个你认为特别有价值、有启发性或令人惊讶的见解

请确保输出格式清晰，使用Markdown格式。"""
        
        user_prompt = f"""请分析以下文章内容：

# {file_name}

{file_content}

---

请按照以下格式输出：

## Summary
[摘要内容]

## Key Takeaways
- [要点1]
- [要点2]
- [要点3]

## Something New
[新发现内容]"""
        
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            response = self.kimi_client.chat_completion(messages)
            result = self.kimi_client.extract_content(response)
            
            return {
                "file_name": file_name,
                "summary": result
            }
        
        except Exception as e:
            logger.error(f"处理文件失败 {file_name}: {e}")
            return {
                "file_name": file_name,
                "summary": f"**处理失败**: {str(e)}"
            }
    
    def generate_week_summary(self, date: Optional[datetime] = None) -> str:
        """生成指定周的提炼文档"""
        # 获取周文件夹
        week_folder = self.folder_manager.get_week_folder(date)
        if not week_folder:
            week_folder = self.folder_manager.create_week_folder(date)
        
        # 收集文件
        files = self.collect_raw_files(week_folder)
        
        if not files:
            logger.warning("没有找到待处理的文件")
            return ""
        
        logger.info(f"找到 {len(files)} 个文件待处理")
        
        # 处理每个文件
        results = []
        for i, file_info in enumerate(files, 1):
            logger.info(f"处理进度: {i}/{len(files)} - {file_info['name']}")
            result = self.process_single_file(file_info['content'], file_info['name'])
            results.append(result)
        
        # 生成合并文档
        week_name = self.folder_manager.get_week_folder_name(date)
        output = self._build_summary_document(week_name, results)
        
        # 保存文档
        output_path = self.folder_manager.get_medium_rare_file(date)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output)
        
        logger.info(f"提炼文档已保存: {output_path}")
        return output
    
    @staticmethod
    def _build_summary_document(week_name: str, results: List[Dict[str, str]]) -> str:
        """构建提炼文档"""
        doc = f"""# 周信息提炼 - {week_name}

> 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
> 文件数量: {len(results)}

---

"""
        
        for i, result in enumerate(results, 1):
            doc += f"""## {i}. {result['file_name']}

{result['summary']}

---

"""
        
        return doc
```

### `workflows/super_analyst/framework_selector.py`

```python
"""分析框架选择器"""
import json
import logging
from pathlib import Path
from typing import List, Dict, Tuple

logger = logging.getLogger(__name__)


class FrameworkSelector:
    """分析框架选择器"""
    
    def __init__(self, config_path: str = "config/frameworks.json"):
        """初始化选择器"""
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        self.frameworks = config['frameworks']
        logger.info(f"加载了 {len(self.frameworks)} 个分析框架")
    
    def select_frameworks(
        self,
        question: str,
        max_frameworks: int = 3
    ) -> List[Dict]:
        """根据问题选择合适的分析框架"""
        scores = []
        
        for framework in self.frameworks:
            score = self._calculate_score(question, framework)
            scores.append((framework, score))
        
        # 按分数排序
        scores.sort(key=lambda x: x[1], reverse=True)
        
        # 返回前N个框架
        selected = [
            {
                "framework": fw,
                "score": score,
                "reason": self._get_selection_reason(question, fw)
            }
            for fw, score in scores[:max_frameworks]
        ]
        
        logger.info(f"选择了 {len(selected)} 个框架")
        for item in selected:
            logger.info(f"  - {item['framework']['name']} (分数: {item['score']:.2f})")
        
        return selected
    
    def _calculate_score(self, question: str, framework: Dict) -> float:
        """计算框架匹配分数"""
        score = 0.0
        question_lower = question.lower()
        
        # 关键词匹配（权重40%）
        keyword_matches = sum(
            1 for keyword in framework['keywords']
            if keyword in question_lower
        )
        if framework['keywords']:
            score += (keyword_matches / len(framework['keywords'])) * 40
        
        # 问题类型匹配（权重30%）
        problem_type_keywords = {
            'strategic': ['战略', '策略', '长期', '规划'],
            'business': ['商业', '业务', '盈利', '市场'],
            'innovation': ['创新', '新', '突破', '颠覆'],
            'problem_solving': ['问题', '解决', '改进', '优化'],
            'evaluation': ['评估', '分析', '衡量', '判断'],
            'organizational': ['组织', '团队', '管理', '文化'],
            'decision_making': ['决策', '选择', '权衡'],
            'competitive_analysis': ['竞争', '对手', '优势'],
            'forecasting': ['预测', '未来', '趋势']
        }
        
        for problem_type in framework['problem_types']:
            type_keywords = problem_type_keywords.get(problem_type, [])
            if any(kw in question_lower for kw in type_keywords):
                score += 30 / len(framework['problem_types'])
        
        # 问题复杂度匹配（权重20%）
        question_length = len(question)
        if framework['complexity'] == 'high' and question_length > 100:
            score += 20
        elif framework['complexity'] == 'medium' and 50 <= question_length <= 100:
            score += 20
        elif framework['complexity'] == 'low' and question_length < 50:
            score += 20
        else:
            score += 10  # 部分匹配
        
        # 默认框架加分（权重10%）
        if framework['id'] in ['first_principles', 'swot']:
            score += 10
        
        return score
    
    def _get_selection_reason(self, question: str, framework: Dict) -> str:
        """生成选择理由"""
        reasons = []
        
        question_lower = question.lower()
        matched_keywords = [
            kw for kw in framework['keywords']
            if kw in question_lower
        ]
        
        if matched_keywords:
            reasons.append(f"包含关键词: {', '.join(matched_keywords)}")
        
        reasons.append(f"适用于{framework['problem_types'][0]}类问题")
        reasons.append(f"复杂度: {framework['complexity']}")
        
        return " | ".join(reasons)
    
    def get_framework_by_id(self, framework_id: str) -> Dict:
        """根据ID获取框架"""
        for fw in self.frameworks:
            if fw['id'] == framework_id:
                return fw
        raise ValueError(f"未找到框架: {framework_id}")
```

### `workflows/super_analyst/run.py`

```python
"""Super Analyst工作流执行器"""
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

from scripts.kimi_client import KimiClient
from scripts.folder_manager import FolderManager
from .framework_selector import FrameworkSelector

logger = logging.getLogger(__name__)


class SuperAnalyst:
    """深度分析工作流"""
    
    def __init__(
        self,
        kimi_client: KimiClient,
        folder_manager: FolderManager,
        framework_selector: FrameworkSelector
    ):
        """初始化分析器"""
        self.kimi_client = kimi_client
        self.folder_manager = folder_manager
        self.framework_selector = framework_selector
        self.prompts_dir = Path("workflows/super_analyst/prompts")
    
    def analyze(
        self,
        question: str,
        context: Optional[str] = None,
        frameworks: Optional[List[str]] = None,
        max_frameworks: int = 3
    ) -> str:
        """执行深度分析"""
        logger.info(f"开始分析问题: {question[:50]}...")
        
        # 选择框架
        if frameworks:
            selected = [
                {
                    "framework": self.framework_selector.get_framework_by_id(fw_id),
                    "score": 100.0,
                    "reason": "用户指定"
                }
                for fw_id in frameworks
            ]
        else:
            selected = self.framework_selector.select_frameworks(question, max_frameworks)
        
        # 执行分析
        analyses = []
        for item in selected:
            framework = item['framework']
            logger.info(f"使用框架: {framework['name']}")
            
            analysis = self._analyze_with_framework(question, context, framework)
            analyses.append({
                "framework": framework,
                "content": analysis
            })
        
        # 生成报告
        report = self._generate_report(question, context, selected, analyses)
        
        # 保存报告
        output_path = self.folder_manager.get_topic_file(question[:30])
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"分析报告已保存: {output_path}")
        return report
    
    def _analyze_with_framework(
        self,
        question: str,
        context: Optional[str],
        framework: Dict
    ) -> str:
        """使用特定框架进行分析"""
        # 加载框架提示词
        prompt_file = self.prompts_dir / f"{framework['id']}.md"
        
        if prompt_file.exists():
            with open(prompt_file, 'r', encoding='utf-8') as f:
                framework_prompt = f.read()
        else:
            logger.warning(f"框架提示词文件不存在: {prompt_file}，使用默认模板")
            framework_prompt = self._get_default_prompt(framework)
        
        # 构建消息
        system_prompt = f"""你是一个专业的战略分析师，擅长使用{framework['name']}进行深度分析。

{framework_prompt}

请确保分析结构清晰、逻辑严密、见解深刻。使用Markdown格式输出。"""
        
        user_content = f"""请使用{framework['name']}分析以下问题：

**问题**: {question}"""
        
        if context:
            user_content += f"\n\n**背景信息**:\n{context}"
        
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ]
            
            response = self.kimi_client.chat_completion(messages, temperature=0.7)
            return self.kimi_client.extract_content(response)
        
        except Exception as e:
            logger.error(f"分析失败: {e}")
            return f"**分析失败**: {str(e)}"
    
    def _get_default_prompt(self, framework: Dict) -> str:
        """获取默认框架提示词"""
        return f"""{framework['description']}

请按照以下结构进行分析：
1. 框架概述
2. 核心分析
3. 关键发现
4. 建议与行动项"""
    
    def _generate_report(
        self,
        question: str,
        context: Optional[str],
        selected: List[Dict],
        analyses: List[Dict]
    ) -> str:
        """生成分析报告"""
        report = f"""# 深度分析报告

## 元数据
- **分析问题**: {question}
- **生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **使用框架**: {len(analyses)}个

"""
        
        if context:
            report += f"""## 背景信息
{context}

"""
        
        report += """## 执行摘要

"""
        
        for item in selected:
            fw = item['framework']
            report += f"- **{fw['name']}**: {item['reason']}\n"
        
        report += "\n---\n\n"
        
        # 添加各框架分析
        for i, analysis in enumerate(analyses, 1):
            fw = analysis['framework']
            report += f"""## {i}. {fw['name']}分析

> **框架说明**: {fw['description']}
> **复杂度**: {fw['complexity']} | **预计用时**: {fw['expected_time']}

{analysis['content']}

---

"""
        
        # 综合建议
        report += """## 综合建议

基于以上多维度分析，关键建议如下：

1. [待AI生成或手动补充]
2. [待AI生成或手动补充]
3. [待AI生成或手动补充]

---

*本报告由AI OS自动生成，请结合实际情况判断应用。*
"""
        
        return report
```

------

## 3. New Angle工作流

### `workflows/new_angle/run.py`

```python
"""New Angle广度思考工作流"""
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional

from scripts.kimi_client import KimiClient

logger = logging.getLogger(__name__)


class NewAngle:
    """广度思考工作流"""
    
    def __init__(self, kimi_client: KimiClient):
        """初始化"""
        self.kimi_client = kimi_client
        self.output_dir = Path("data/topic/new-angle")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def analyze(self, input_text: str, topic: str = "未命名") -> str:
        """执行广度思考分析"""
        logger.info(f"开始广度思考分析: {topic}")
        
        # 执行四步分析
        step1 = self._analyze_blind_spots(input_text)
        step2 = self._switch_perspectives(input_text, step1)
        step3 = self._cross_domain_analogy(input_text, step1, step2)
        step4 = self._generate_insights(input_text, step1, step2, step3)
        
        # 生成报告
        report = self._generate_report(topic, input_text, step1, step2, step3, step4)
        
        # 保存报告
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_topic = safe_topic.replace(' ', '-')
        output_path = self.output_dir / f"{safe_topic}_{timestamp}.md"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        logger.info(f"洞察报告已保存: {output_path}")
        return report
    
    def _analyze_blind_spots(self, input_text: str) -> str:
        """步骤1: 分析盲点"""
        logger.info("执行步骤1: 盲点分析")
        
        system_prompt = """你是一个善于发现思维盲点的专家。请分析给定的内容，指出：
1. 可能被忽略的关键因素
2. 隐含的假设
3. 未考虑的风险或机会
4. 需要进一步验证的观点"""
        
        user_prompt = f"""请分析以下内容中可能存在的思维盲点：

{input_text}

请列出3-5个关键盲点，并说明为什么它们重要。"""
        
        return self._call_api(system_prompt, user_prompt)
    
    def _switch_perspectives(self, input_text: str, blind_spots: str) -> str:
        """步骤2: 切换视角"""
        logger.info("执行步骤2: 视角切换")
        
        system_prompt = """你是一个多维度思考专家。请从不同利益相关方的角度重新审视问题：
1. 用户/客户视角
2. 竞争对手视角
3. 合作伙伴视角
4. 未来自己的视角（3-5年后回顾）"""
        
        user_prompt = f"""基于以下内容和已发现的盲点，请从多个视角分析：

**原始内容**:
{input_text}

**已识别盲点**:
{blind_spots}

请从至少3个不同的视角提供洞察。"""
        
        return self._call_api(system_prompt, user_prompt)
    
    def _cross_domain_analogy(
        self,
        input_text: str,
        blind_spots: str,
        perspectives: str
    ) -> str:
        """步骤3: 跨领域类比"""
        logger.info("执行步骤3: 跨领域类比")
        
        system_prompt = """你是一个跨领域思维专家。请从其他领域寻找有启发性的类比：
1. 自然界/生物学
2. 历史事件
3. 其他行业的成功案例
4. 艺术或哲学领域

通过类比产生新的洞察和解决方案。"""
        
        user_prompt = f"""基于以下分析，寻找跨领域的类比和启发：

**原始内容**:
{input_text}

**盲点分析**:
{blind_spots}

**多视角分析**:
{perspectives}

请提供2-3个有价值的跨领域类比，并说明它们如何启发新思路。"""
        
        return self._call_api(system_prompt, user_prompt)
    
    def _generate_insights(
        self,
        input_text: str,
        blind_spots: str,
        perspectives: str,
        analogies: str
    ) -> str:
        """步骤4: 生成创新洞察"""
        logger.info("执行步骤4: 创新洞察")
        
        system_prompt = """你是一个创新战略专家。综合前面的分析，提出：
1. 反直觉的洞察
2. 潜在的突破性机会
3. 具体的行动建议
4. 需要验证的假设"""
        
        user_prompt = f"""综合以下所有分析，提出创新性洞察：

**原始内容**:
{input_text}

**盲点分析**:
{blind_spots}

**多视角分析**:
{perspectives}

**跨领域类比**:
{analogies}

请提出3-5个具有创新性的洞察和建议。"""
        
        return self._call_api(system_prompt, user_prompt)
    
    def _call_api(self, system_prompt: str, user_prompt: str) -> str:
        """调用API"""
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            response = self.kimi_client.chat_completion(messages, temperature=0.8)
            return self.kimi_client.extract_content(response)
        
        except Exception as e:
            logger.error(f"API调用失败: {e}")
            return f"**分析失败**: {str(e)}"
    
    def _generate_report(
        self,
        topic: str,
        input_text: str,
        step1: str,
        step2: str,
        step3: str,
        step4: str
    ) -> str:
        """生成报告"""
        report = f"""# 广度思考洞察报告 - {topic}

> 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 原始输入

{input_text[:500]}{'...' if len(input_text) > 500 else ''}

---

## 1. 盲点分析

{step1}

---

## 2. 多视角审视

{step2}

---

## 3. 跨领域类比

{step3}

---

## 4. 创新洞察

{step4}

---

## 总结

本报告通过四步广度思考法，对原始内容进行了多维度拓展：
1. 识别了可能被忽略的关键盲点
2. 从多个利益相关方视角重新审视
3. 借鉴了跨领域的成功经验和类比
4. 提出了具有创新性的洞察和建议

建议结合实际情况，验证关键假设后采取行动。

---

*本报告由AI OS自动生成*
"""
        
        return report
```

------

## 4. CLI命令行工具

### `scripts/cli.py`

```python
"""命令行工具"""
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, TextColumn

from .folder_manager import FolderManager
from .content_processor import ContentProcessor
from .kimi_client import KimiClient
sys.path.append(str(Path(__file__).parent.parent))
from workflows.super_analyst.framework_selector import FrameworkSelector
from workflows.super_analyst.run import SuperAnalyst
from workflows.new_angle.run import NewAngle

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)]
)
logger = logging.getLogger(__name__)

app = typer.Typer(help="个人AI OS - 命令行工具")
console = Console()


@app.command()
def ingest(
    week: Optional[str] = typer.Option(None, help="周日期 (YYYY-MM-DD)，默认当前周"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="详细输出")
):
    """提炼周内容"""
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    console.print("[bold blue]开始信息提炼流程...[/bold blue]")
    
    try:
        # 解析日期
        date = datetime.strptime(week, "%Y-%m-%d") if week else None
        
        # 初始化组件
        folder_manager = FolderManager()
        kimi_client = KimiClient()
        processor = ContentProcessor(folder_manager, kimi_client)
        
        week_name = folder_manager.get_week_folder_name(date)
        console.print(f"处理周: {week_name}")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("提炼中...", total=None)
            result = processor.generate_week_summary(date)
        
        if result:
            output_path = folder_manager.get_medium_rare_file(date)
            console.print(f"[green]✓[/green] 提炼完成: {output_path}")
        else:
            console.print("[yellow]没有找到待处理的文件[/yellow]")
    
    except Exception as e:
        console.print(f"[red]✗ 错误: {str(e)}[/red]")
        logger.exception("处理失败")
        raise typer.Exit(1)


@app.command()
def analyze(
    question: str = typer.Argument(..., help="要分析的问题"),
    context: Optional[str] = typer.Option(None, "--context", "-c", help="背景信息"),
    frameworks: Optional[str] = typer.Option(None, "--frameworks", "-f", help="指定框架ID（逗号分隔）"),
    max_frameworks: int = typer.Option(3, "--max", "-m", help="最多使用几个框架"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="详细输出")
):
    """深度分析（Super Analyst）"""
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    console.print("[bold blue]开始深度分析...[/bold blue]")
    console.print(f"问题: {question}")
    
    try:
        # 初始化组件
        folder_manager = FolderManager()
        kimi_client = KimiClient()
        framework_selector = FrameworkSelector()
        analyst = SuperAnalyst(kimi_client, folder_manager, framework_selector)
        
        # 解析框架
        framework_list = frameworks.split(',') if frameworks else None
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("分析中...", total=None)
            result = analyst.analyze(question, context, framework_list, max_frameworks)
        
        output_path = folder_manager.get_topic_file(question[:30])
        console.print(f"[green]✓[/green] 分析完成: {output_path}")
    
    except Exception as e:
        console.print(f"[red]✗ 错误: {str(e)}[/red]")
        logger.exception("分析失败")
        raise typer.Exit(1)


@app.command()
def new_angle(
    input_file: str = typer.Argument(..., help="输入文件路径"),
    topic: str = typer.Option("未命名", "--topic", "-t", help="主题名称"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="详细输出")
):
    """广度思考（New Angle）"""
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    console.print("[bold blue]开始广度思考...[/bold blue]")
    
    try:
        # 读取输入
        input_path = Path(input_file)
        if not input_path.exists():
            console.print(f"[red]文件不存在: {input_file}[/red]")
            raise typer.Exit(1)
        
        with open(input_path, 'r', encoding='utf-8') as f:
            input_text = f.read()
        
        # 初始化组件
        kimi_
```