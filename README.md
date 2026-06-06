# 📚 基于情感分析的小说推荐系统

> Sentiment-Based Novel Recommendation System

对小说评论进行 BERT 情感分析（爽点/吐槽/虐点/中性），并基于分析结果向用户推荐匹配风格的网络小说。

---

## 🛠 技术栈

### 后端
| 技术 | 用途 |
|------|------|
| **Python 3** + **Flask** | RESTful API 服务 |
| **Flask-CORS** | 跨域请求支持 |
| **Flask-SQLAlchemy** + **PyMySQL** | ORM 与 MySQL 数据库操作 |
| **PyTorch** + **Transformers (HuggingFace)** | BERT 模型加载与推理 |
| **Pandas** + **scikit-learn** | 数据处理与模型评估 |
| **Requests** + **BeautifulSoup4** | 豆瓣小说评论爬虫 |

### 前端
| 技术 | 用途 |
|------|------|
| **Vue 3** (Composition API) | 前端框架 |
| **TypeScript** | 类型安全 |
| **Vite 8** | 构建工具 |
| **Element Plus** | UI 组件库 |
| **ECharts 6** | 数据可视化 |
| **Pinia** + **Vue Router** | 状态管理与路由 |

### AI / 模型
| 技术 | 用途 |
|------|------|
| **BERT-base-Chinese** | 预训练中文语言模型 |
| **HuggingFace Trainer** | 模型微调训练 |
| **通义千问 (Qwen API)** | AI 辅助数据标注 |

---

## 🔥 核心难点

### 难点一：高质量标注数据获取
- **问题**：BERT 微调需要大量已标注情感类别的评论数据，"爽点/虐点/吐槽/中性"的定义本身主观性强
- **方案**：采用"通义千问 API 自动预标注 + 人工校验"的半自动流水线，效率提升 5 倍以上；结合同义词替换、回译法进行数据增强

### 难点二：中文网络文学语义理解
- **问题**：反讽（"太好了又断更了"实为负面）、领域特定词（"杀伐果断"在小说的褒义）、网络用语（yyds、刀傻了）让通用情感词典完全失效
- **方案**：使用 BERT-base-Chinese 预训练模型在标注数据上微调，利用其海量语料中习得的上下文理解能力，替代传统关键词匹配方法

### 难点三：推荐的"冷启动"与"信息茧房"
- **问题**：新用户无历史行为时协同过滤失效；单一偏好推荐导致内容同质化
- **方案**：混合推荐策略 — 新用户基于内容热度推荐（冷启动），老用户切换协同过滤；引入"探索与利用"机制，强制插入 1-2 本非偏好领域高分小说打破茧房

---

## 🚀 使用方法

### 环境要求
- Python 3.10+
- Node.js 20.19+ / 22.12+
- MySQL 8.0+
- CUDA（可选，GPU 推理加速）

### 1. 克隆项目
```bash
git clone https://github.com/yenaiBu/Sentiment-Based-Novel-Recommendation.git
cd Sentiment-Based-Novel-Recommendation
```

### 2. 后端配置
```bash
cd backend

# 创建虚拟环境
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # macOS/Linux

# 安装依赖
pip install -r requirements.txt

# 下载 BERT 预训练模型（约 400MB）
python download_bert.py

# （可选）训练情感分析模型 — 需要 labeled_data.xlsx
python train_model.py
```

### 3. 数据库配置
- 创建 MySQL 数据库 `novel_db`
- 修改 `app.py` 中的 `DB_CONFIG`（用户名/密码）
- 运行爬虫获取小说与评论数据：
```bash
python spider.py
```

### 4. 前端配置
```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 5. 启动后端
```bash
cd backend
venv\Scripts\activate
python app.py
# 服务运行在 http://localhost:5000
```

### 6. 访问系统
- 前端：`http://localhost:5173`
- 后端 API：`http://localhost:5000`
- 在页面输入评论文本，系统自动分析情感并推荐对应风格的小说

---

## 📁 项目结构
```
novel-system/
├── backend/
│   ├── app.py                  # Flask API 主程序
│   ├── train_model.py          # BERT 微调训练脚本
│   ├── data_preprocess.py      # AI 辅助数据标注（通义千问）
│   ├── spider.py               # 豆瓣小说爬虫
│   ├── download_bert.py        # BERT 模型下载脚本
│   ├── requirements.txt        # Python 依赖
│   ├── labeled_data.xlsx       # 标注训练数据
│   ├── models/                 # 数据库模型
│   ├── templates/              # HTML 模板
│   ├── bert-local/             # 预训练 BERT 模型（config/tokenizer）
│   └── sentiment_model/        # 微调后模型（config/tokenizer）
└── frontend/
    ├── src/
    │   ├── views/              # 页面视图
    │   ├── components/         # Vue 组件
    │   ├── router/             # 路由配置
    │   ├── stores/             # Pinia 状态管理
    │   └── assets/             # 样式与静态资源
    ├── package.json            # Node 依赖
    ├── vite.config.ts          # Vite 配置
    └── tsconfig.json           # TypeScript 配置
```

---

## 📌 说明

- **模型权重文件**（`pytorch_model.bin` / `model.safetensors`）因超过 GitHub 100MB 限制未上传，需通过 `download_bert.py` 下载预训练模型，再运行 `train_model.py` 生成微调模型
- 训练 checkpoint 目录（`sentiment_model/checkpoint-*/`）为训练中间产物，已排除
- `venv/` 和 `node_modules/` 通过 `.gitignore` 排除，克隆后需自行安装
