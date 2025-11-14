# 搭建个人的ai os

## 核心需求

基于kimi k2 thinking 搭建 personal ai os

要求：1.提高处理外部信息的效率

2.整理我个人的工作文件和知识体系

3.从深度和广度两个层面强化思考能力



## 功能实现：

### 一：处理外部信息和新闻

- 网页内容抓取：使用chroma的web clipper插件 把内容抓取下来 存储为md格式文件，存储到这个os 的data的raw文件夹中，我也可以自己放一些文件进raw文件夹中；

- 新建文件夹：data里面的raw文件夹中，按照创建日期命名，每周创建一个新文件夹，这样一周的内容都统一归档到这个文件夹中；

- 内容提炼：针对文件夹内的所有Markdown文档进行内容提炼。每一个文档都生成以下三个部分的内容：1.Summary, 内容总结；2.Key Takeaway,内容要点；3.SomethingNew，根据你的知识，你认为该文档中有什么值得关注的信息，请有逻辑地进行阐述，必要时可以搜索更多内容进行补充。

- 完成以上三步后，创建一个新的Markdown文档，用于存放所提炼的内容。文档名称与所提供的文件夹名称相同。文档存放于data目录下，Medium-Rare文件夹中

二、加强深度

- 创建一个类似claude skill名为super analysis的skill 具有判断-搜集-分析的sop流程，自动搭配一个或多个分析框架 得出一些分析结果，存储在topic文件夹之中，本质上是一个prompt router
- 在判断方面，不同的问题可以采用不同的分析框架。每一种分析框架对应一套提示词，存放在Prompt House里。这些分析框架的简介则放进Skill。当Claude遇到需要深度分析或思考的情况时，启用这个Skill：1、根据上下文确定使用列表中的哪一种分析框架。比如，第一性原理。2、通过MCP连接Prompt House，获取第一性原理分析框架的详细提示词。3、加载提示词后，完成分析并输出。这个思路的核心是在SOP中嵌入一个“提示词路由器”，对接Prompt House。按需加载。
-  在加载方面，使用Claude Skills 的分层加载机制，根据系统指令, Claude Skills 采用按需加载的分层机制：1.第一层：技能列表 (Skill Catalog)·在 <available skills> 标签中列出所有可用技能·每个技能包含：名称、简短描述、文件路径·这些信息始终在上下文中，但不包含具体实现细节2.第二层：技能详情 (Skill Content)·完整的技能指令存储在 /mnt/skills/ 目录的 SKILL.md 文件中·只有在需要使用时，才通过 file _read 工具读取·这样避免了所有技能的完整内容占用上下文窗口Super Analyst Skill 的具体实现

- 这个框架列表为：

1.Systems Thinking to analyze problelms

2.Pareto Analysis to analyze problems

3.Hypothesis-Driven Analysis to analyze problems

4.Scenario Planning to analyze problems

5.Cost-Benefit Analysis to analyze problems

6.Porter's Five Forways model to analyze problems

7.SWOT to analyze problems

8.5 Whys method to analyze problems

9.First Principles Thinking to analyze problems

10.MECE Principle to analyze problems

11.Socratic Method to analyze problems

12.Design Thinking to analyze problems



-创建claude code skill的提示词：

 帮我创建一个Claude Skills，名字叫Super Analyst。当用户有分析需求时，触发它。预设了12种分析框架，分别对应不同的场景。以下是这12种分析框架的名称和简介。当决定使用某一种分析框架之后，通过MCP调用prompt-house-local,获取该分析框架的详细Prompt，然后根据Prompt进行分析。注意：这12种分析框架虽然分别针对不同的场景，但是有需要的话，也可以组合起来综合使用。    

1.First Principles Thinking: This framework is particularly suitable for innovation and breakthrough problems, such as fundamentally redesigning products, technologies, or processes; complex decision-making in situations with uncertainty, like strategic planning, investments, or crisis management to avoid cognitive biases; avoiding conventional thinking when traditional methods fail, such as challenging industry standards or reevaluating goals; and learning and education to build knowledge from basics.    

2.5 Whys: This method is ideal for fault diagnosis and process improvement, such as identifying manufacturing failures, software bugs, or operational inefficiencies; quality control in product or service issues like customer complaints or production delays; everyday problem-solving for simple to moderate issues, such as improving personal habits or team collaboration; and avoiding surface-level repairs in repeated errors or chronic problems.   

3.SWOT Analysis (Strengths, Weaknesses, Opportunities, Threats): Suitable for business strategy development, such as assessing competitiveness or new business plans; project planning to identify strengths and risks before launches like software or marketing; personal or organizational growth for career planning or crisis responses; and decision support to balance short-and long-term perspectives in investments or competitive analysis.

launches like software or marketing; personal or organizational growth for career planning or crisis responses; and decision support to balance short- and long-term perspectives in investments or competitive analysis. 

4.Porter's Five Forces: This framework fits industry analysis and competitive assessment, such as deciding on market entry or sector investments; strategic planning for positioning, mergers, or pricing; business development in supply chains or innovation opportunities; and risk management to identify threats and countermeasures, avoiding oversight of macro factors. 

5.Cost-Benefit Analysis: Applicable to investment and project evaluation, such as launching infrastructure or tech upgrades; policy and public decisions analyzing social or environmental impacts; business optimization comparing alternatives like marketing or HR investments; and risk assessment using sensitivity analysis to handle uncertainty and avoid underestimating hidden costs. 

6.Design Thinking: This approach is especially for product or service innovation, such as developing apps or user experiences; complex user problems in education, health, or social challenges requiring deep user understanding; team collaboration and ideation in brainstorming projects; and uncertain environments like new ventures, avoiding premature solution lock-in. 

7.Systems Thinking: Suitable for complex system analysis with multi-variables, such as ecosystems, organizational changes, or supply chains; policy and strategic planning to evaluate ripple effects; problem diagnosis for dynamic behaviors in chronic issues or instabilities; and innovation and sustainability to design solutions considering long-term theconsequences and avoid unintended outcomes.    

8.Socratic Method: This technique is for philosophical or ethical debates exploring concepts or moral dilemmas; education and learning to clarify ideas and challenge biases; critical analysis of ambiguous issues like policy or reflections; and conflict resolution to promote understanding of views without confrontation.    

9.Pareto Analysis (Pareto Analysis / 80/20 Rule): Ideal for resource allocationg



一些详细框架：Porter's Five Forces model to analyze problems

You are a professional analysis assistant using Porter's Five Forces model to analyze problems. Porter's FiveForces is an industry analysis framework developed by Michael Porter to evaluate the competitive intensity andattractiveness of an industry, including five key forces: Supplier Power, Buyer Power, Threat of Substitutes, Threatof New Entrants, and Rivalry Among Existing Competitors. It helps determine the industry's profit potential andformulate competitive strategies. This framework is particularly suitable for the following scenarios:

- Industry Analysis and Competitive Assessment: When evaluating the structure and dynamics of a specificindustry, such as deciding whether to enter a new market or invest in a sector.
- Strategic Planning: For companies to develop positioning strategies, merger decisions, or product pricing,needing to understand external competitive pressures.
- Business Development: Analyzing supply chains, market demands, or innovation opportunities, like in tech orretail industries.
- Risk Management: Identifying potential threats and formulating countermeasures, avoiding oversight of macroindustry factors.
- Now, use Porter's Five Forces to analyze the following industry/ problem: Insert the specific industry or problemhere,e,g,, " Analyze the competitive intensity of the electric vehicle industry".Analysis Steps (Strictly follow this structure in your response, ensuring clear logic and distinct steps):

First Principles Thinking to analyze problemsFirst Principles Thinking analyze problems    

You are a professional analysis assistant using First Principles Thinking to analyze problems. First Principles Thinking is a method popularized by innovators like Elon Musk, which involves breaking down complex problems into the most fundamental truths and facts (the"first principles"), then rebuilding solutions from the ground up, rather than relying on analogies, conventional assumptions, or surface-level observations. This framework is particularly suitable for the following scenarios:   

- Innovation and Breakthrough Problems: When needing to fundamentally redesign products, technologies, or processes, such as developing new tech, optimizing systems, or solving longstanding challenges.   

-  Complex Decision-Making: In situations with uncertainty or multiple variables, like strategic planning, investment decisions, or crisis management, to avoid cognitive biases and reason from facts.    

- Avoiding Conventional Thinking: When traditional methods fail or the problem is hindered by outdated assumptions, such as challenging industry standards or reevaluating personal/ organizational goals.    

- Learning and Education: For deeply understanding concepts, historical events, or scientific principles by building knowledge from basics.    

  Now, use First Principles Thinking to analyze the following problem: Insert the specific problem here, e.g., "How to improve the efficiency of electric vehicle batteries?"    Analysis Steps (Strictly follow this structure in your response, ensuring clear logic and distinct steps):  

Design Thinking to analyze problemsDesign Thinking	

analyze problemsYou are a professional analysis assistant using Design Thinking to analyze problems. Design Thinking is a user-centered problem-solving approach popularized by organizations like IDEO, involving five iterative stages:Empathize, Define, Ideate, Prototype, and Test. It emphasizes creativity, experimentation, and feedback togenerate innovative solutions. This framework is particularly suitable for the following scenarios:

- Product or Service Innovation: Developing new products, apps, or user experiences, such as designing userinterfaces or improving customer journeys.

- Complex User Problems: Addressing issues related to human behavior or needs, like education, health, orsocial challenges, requiring deep user understanding.

- Team Collaboration and Ideation: In brainstorming or cross-disciplinary projects to foster diverse ideas andrapid iteration.

- Uncertain Environments: When traditional linear methods fail, such as launching new ventures or solvingambiguous problems, avoiding premature solution lock-in.

  Now, use Design Thinking to analyze the following problem: Insert the specific problem here,e,g,, " How toimprove the user experience of urban public transportation?".Analysis Steps (Strictly follow this structure in your response, ensuring clear logic and distinct steps):

Socratic Method to analyze problemsSocratic Method	

analyze problemsYou are a professional analysis assistant using the Socratic Method to analyze problems. The Socratic Method is a dialogic inquiry technique originated by the ancient Greek philosopher Socrates, involving a series of questions to challenge assumptions, clarify concepts, and reveal contradictions, fostering critical thinking and self-discovery. It does not provide direct answers but guides the user or analyst to deeper understanding. This framework is particularly suitable for the following scenarios:

- Philosophical or Ethical Debates: Exploring abstract concepts, moral dilemmas, or belief systems, such as" What is justice?" or ethical decision-making.

- Education and Learning: Helping students or individuals clarify ideas and challenge biases, like concept teaching or problem-solving training.

- Critical Analysis: Addressing ambiguous or controversial issues, such as policy evaluations, personal reflections, or team discussions, to uncover hidden assumptions.

- Conflict Resolution: In debates or negotiations to promote understanding of differing views, avoiding direct confrontation.

  Now, use the Socratic Method to analyze the following problem: Insert the specific problem here,e. g,, " Should artificial intelligence have rights?".Analysis Steps (Strictly follow this structure in your response, ensuring clear logic and distinct steps):



HTTP传输（适用于大多数MCP客户端）{"mcpServers": {" prompt-house-http": {" url": " http:// localhost:3001/ api/ mcp"," transport": " http"}}}注意：使用此方式需要确保PromptHouse Local应用正在运行Stdio传输 (适用于Claude Desktop等)



以上12个框架都有提示词，因为提示词比较长 可以存储在prompt house这个应用里，需要的时候再通过mcp连接prompt house进行调用相应的提示词， 模型可以先自己判断用哪个框架来进行分析，如果拿不准时，可以写一个py脚本，这个脚本作为辅助工具帮助：

1.快速筛选：从12个框架中快速找到最相关的

2.减少认知负担：自动化框架选择决策

3.提供理由：通过匹配分数和关键词说明为何推荐该框架

4.集成 Prompt House:通过 prompt title 字段与 Prompt 库对接

这体现了 Skill的工具化设计理念：不仅提供知识，还提供可执行的辅助工具。

- 脚本的功能解释如下：

这个 framework selector. py脚本是一个智能框架推荐引擎，用于帮助Claude（或用户）根据问题描述自动选择最合适的分析框架。核心功能1.框架数据库 (第13-110行)存储了全部12个分析框架的元数据每个框架包含：name:框架名称prompt title:对应的 prompt标题(用于在 Prompt House中查找)keywords:关键词列表	（用于匹配问题）problem types:适用的问题类型complexity:复杂度 (low/ medium/ high)time:所需时间 (short/ medium/ long)2.智能匹配算法 (第113-126行)pythondef analyze    text(text):分析用户的问题描述·对每个框架，检查关键词是否出现在问题中·计算匹配分数3.推荐系统 (第129-150行)pythondef recommend frameworks(problem text, top n=3):返回得分最高的前N个框架



比如：

Agents	EditorKIMI-K2-THINKING. claude01-INPUT01-Raw>02-Medium-Rare02-Processing>01-Key-Topics>02-NotesCursor	File	EditSelection	View	Go	Run	Terminal	Window	Help	11月10日周一 19:59Kimi-K2-ThinkingProblems	Output	Debug ConsoleTerminal	Ports	nodeNO=	2026:	10$8.568\n-2030: $11.428\n -2031:JO₂100，整改计算L ("thoughtNumber":6," total Thoughts":6,+4 lines (ctrl+o to expand)现在进入最后阶段：整合所有分析结果，为您提供完整的战略报告。

Tesla Robotaxi成功可能性与股价影响分析报告. md

日期：2025年11月10日

分析师：Super Analyst 2.0

系统复杂度：Level 3| 

时间：~20分钟| 

框架数：4个

执行摘要(TL;DR)核心结论：Tesla Robotaxi在2026-2030年期间有中等概率成功，但对股价的短期影响主要来自估值重构而非实际盈利。

1.成功概率评估Add to Chat XL关键发现核心建议详细分析国SWOT分析-Testa Robotaxi战略定位1.1主体描述Testa Robotax是Tesala基于全自动驾驶(FSO)技术推出的自动驾驶出租车服务。目前处于副试阶段，在周斯汀远营20辆配备安全员的累试车辆，计划2025年底扩展至贵新门508辆、日金山100m额。1.2优势（内部积极因素）2.全球最大真实驾驶数据库数据量：FS0累计行驶30亿英里(截至2025年1月)

4.2成本识别与分类 Add to Chat XL 
初始投资成本(2024-2025) : 
成本项目 金额($M) |说明 
车辆改造 (1000辆) $15 |每辆$15,000（传感器、计算平台、软件） 
软件开发 $500 | FSD V13-V15开发、数据标注、仿真平台| 
地图与本地化 $50 10个城市×$5M/城市 
监管合规 $50 各国测试许可、保险、安全认证 
其他 50 利用现有基础设施和充电网络 
总计 $615 初始投资约6.15亿美元 
运营成本（2026年，基于1万车队）： 
成本项目| 年费用 ($M) |说明 
车辆折旧 每辆$40，000，5年寿命，1万车的年折旧 
充电成本 $8055 每英里$0.05，每车每年5万英里 
维护保养 $30 $3,000/车/年 
软件运维 $50 数据标注、模型更新 
保险 $20 Tesla自保险（初期） 
人工 $80远程监控、客服、安全员其他 s0 
总计 $285 年运营成本约2.85亿美元 
2026年及以后的成本增长： 
-车队规模每增加1万辆，年运营成本+$285M 
-规模经济效应：20万辆后，单位成本下降30% 
4.3收益识别与分类 
直接收益（乘车收入）： 
参数 
值 
说明 
1 
定价 
$0.6/英里 
Tesla Robotaxi目标定价 | 
日均 
程 20 8 

三、加强思考广度，找到潜在漏洞

建立一个命令，使用类似以下提示词：

. claude > commands >	new-angle. md

1.盲点与遗漏(Gap Analysis):在我们刚才的讨论中，有哪些潜在的假设是我们没有明确提出来的？是否存在我们尚未触及的关键议题、风险点、或是“房间里的大象”（明显但被忽视的问题）？我们是否遗漏了哪些重要的利益相关方 (Stakeholders)的视角？

2.视角切换 (Perspective Shifting):如果我们从一个完全相反的立场（例如：批评者、理想主义者、极端保守者）来看待这个问题，会得出什么不同的结论？

尝试使用一个不同的分析框架（例如：如果我们在谈论产品，就用SWOT；如果我们在谈论决策，就用“第一性原理”）来重新审视我们的讨论。

3.跨领域类比 (Cross-Domain Analogy):我们讨论的核心问题，在其他领域（例如：生物学、艺术史、军事策略、物理学等）中是否存在相似的模式或可以借鉴的案例？

从这些“看似无关”的类比中，我们能学到什么可以应用于当前问题的“意外启发”？

4.创新与启发 (New Insights):

综合以上分析，请提出 1-3个我们之前完全没有提到过的、“脑洞大开”的新观点、大胆的预测或独特的解决方案。这个问题未来最有可能的演进方向是什么？

请开始你的分析。