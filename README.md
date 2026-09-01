# 基于 LangGraph 和 RAG 的企业智能客服 Agent

> 一个面向企业行政制度问答的智能客服 Demo，使用 DashScope Embedding、Chroma、LangGraph、SQLite 和 Gradio 构建。
>
> 项目重点展示大模型应用开发中的知识库问答、检索增强生成、Agent 工作流和会话记忆持久化。

## 🖼️ 项目简介

用户可以通过 Web 页面咨询企业行政制度，例如：

- 休假政策
- 差旅与费用报销
- 考勤管理
- 员工离职流程
- 保密与知识产权规定

系统会先从本地企业制度知识库中检索相关内容，再将检索结果交给 Qwen 模型生成回答，减少模型脱离知识库自由编造答案的情况。

## 🆕 项目特性

- **RAG 知识库问答**：基于企业制度文档构建本地向量知识库。
- **检索优先**：用户提问后先检索 Chroma，再将相关原文交给大模型。
- **LangGraph Agent**：使用 LangChain `create_agent` 构建 Agent 图和工具调用流程。
- **SQLite 会话记忆**：使用 LangGraph Checkpoint 保存对话状态。
- **Gradio Web UI**：提供开箱即用的浏览器聊天界面。
- **动态提示词**：支持在页面中修改系统提示词。
- **模块化设计**：将模型、向量库、Agent、配置和页面逻辑拆分到不同模块。

## 📐 基本原理

### 1. Loading

使用 `TextLoader` 读取 `data/政策文件.txt`。

### 2. Splitting

使用 `RecursiveCharacterTextSplitter` 将较长的制度文档切分成多个文本块，方便后续向量检索。

### 3. Embedding

使用 DashScope `text-embedding-v2` 将每个文本块转换成向量。

### 4. Storage

使用 Chroma 将文本向量和原文持久化到本地 `chroma_customer_db/` 目录。

### 5. Retrieval

用户提问后，将问题转换成向量，在 Chroma 中检索最相关的文本块，默认返回前 3 个结果。

### 6. Generation

系统将用户问题和检索到的政策原文组合后提交给 Qwen，模型只根据知识库内容生成最终回答。

```text
政策文件
    -> 文档加载
    -> 文本切分
    -> Embedding 向量化
    -> Chroma 向量库

用户问题
    -> 向量检索
    -> 获取相关政策原文
    -> LangGraph Agent
    -> Qwen 生成回答
    -> Gradio 展示
```

## 🧰 技术栈

- Python
- Qwen `qwen-turbo`
- DashScope Embeddings
- LangChain
- LangGraph
- Chroma
- SQLite
- Gradio

## 📁 项目结构

```text
smart_customer_agent_demo/
├── main.py                 # 程序入口、聊天流程和 Gradio 页面
├── agent_builder.py        # LangGraph Agent 构建
├── chat_model.py           # Qwen 和 Embedding 模型初始化
├── vector_store.py         # 文档加载、切分、向量库和检索工具
├── config.py               # 文件路径、端口和系统提示词配置
├── requirements.txt        # Python 依赖
├── .env.example            # 环境变量配置示例
├── README.md               # 项目说明
└── data/
    └── 政策文件.txt        # 脱敏后的演示知识库文档
```

运行过程中会自动生成以下本地文件或目录，这些内容不会提交到 GitHub：

```text
chroma_customer_db/        # Chroma 向量索引
agent_memory.db            # SQLite 对话记忆
__pycache__/                # Python 缓存
```

## 💻 安装

### 1. 克隆仓库

```shell
git clone https://github.com/<your-username>/smart-customer-agent-demo.git
cd smart-customer-agent-demo
```

### 2. 创建 Python 环境

使用 Conda：

```shell
conda create -n smart-customer-agent python=3.12 -y
conda activate smart-customer-agent
pip install -r requirements.txt
```

也可以使用 Python `venv` 创建虚拟环境。

### 3. 配置 API Key

复制环境变量模板：

Windows PowerShell：

```powershell
Copy-Item .env.example .env
```

Linux/macOS：

```shell
cp .env.example .env
```

然后编辑 `.env`：

```env
DASHSCOPE_API_KEY=your_dashscope_api_key_here
```

也可以直接在终端中设置：

Windows PowerShell：

```powershell
$env:DASHSCOPE_API_KEY="your_dashscope_api_key_here"
```

Linux/macOS：

```shell
export DASHSCOPE_API_KEY="your_dashscope_api_key_here"
```

### 4. 启动 WebUI

```shell
python main.py
```

启动后，在浏览器中打开：

```text
http://127.0.0.1:7860
```

首次启动时，程序会读取 `data/政策文件.txt` 并创建 Chroma 向量库。

## 🔄 更新知识库

如果修改了 `data/政策文件.txt`，需要删除旧向量库后重新启动：

Windows PowerShell：

```powershell
Remove-Item -Recurse -Force chroma_customer_db
python main.py
```

Linux/macOS：

```shell
rm -rf chroma_customer_db
python main.py
```

## 🧩 模块说明

### `main.py`

负责初始化模型和知识库、处理聊天请求、构建 Gradio 页面以及启动服务。

### `vector_store.py`

负责加载政策文档、切分文本、创建 Chroma 向量库，并提供 `search_knowledge` 检索工具。

### `chat_model.py`

负责初始化 Qwen 聊天模型和 DashScope Embedding 模型。

### `agent_builder.py`

负责使用 LangGraph `create_agent` 创建 Agent，并注入系统提示词、工具和 SQLite Checkpointer。

### `config.py`

集中管理文档路径、向量库路径、SQLite 路径、检索数量、服务地址和系统提示词。

## ⚠️ 注意事项

- 不要将 `.env` 或真实 API Key 提交到 GitHub。
- 如果 API Key 曾经被公开，应立即撤销并重新生成。
- `data/政策文件.txt` 仅用于演示，正式使用时应替换为公开或脱敏后的企业文档。
- `chroma_customer_db/` 是本地生成的向量索引，不建议提交到仓库。
- 当前 Demo 使用固定的 `thread_id`，多个用户同时访问时可能共享会话；正式系统应为每个用户生成独立会话 ID。
- `qwen-turbo` 和 DashScope Embedding 调用会产生 API 用量，请注意账户余额和调用限制。

## 📝 简历项目描述

**企业智能客服 Agent**

基于 LangGraph 搭建企业智能客服 Agent，使用 DashScope Embedding 和 Chroma 构建企业行政制度 RAG 知识库，通过检索增强生成方式提升回答的准确性；使用 SQLite 实现会话状态持久化，并使用 Gradio 搭建可交互的 Web 客服界面。

## 🙌 后续优化方向

- 支持 PDF、Word、Markdown 等多种知识库文件格式。
- 增加知识库文件上传和在线更新功能。
- 为不同用户生成独立的会话 ID。
- 增加检索结果相似度阈值和重排序模型。
- 增加单元测试、日志记录和异常监控。
- 使用 Docker 封装部署环境。

## 📄 License

本项目仅用于学习和技术展示。
