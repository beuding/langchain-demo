"""项目全局配置参数"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PERSIST_DIR = os.path.join(BASE_DIR, "chroma_customer_db")
CHECKPOINT_DB_PATH = os.path.join(BASE_DIR, "agent_memory.db")
DOC_FILE = os.path.join(BASE_DIR, "data", "政策文件.txt")
TOP_K = 3

SYSTEM_PROMPT_TPL = """
你是企业智能客服助手，请严格遵循下面规则：
1. 所有业务问题必须先调用「search_knowledge」工具检索知识库,根据返回内容回答;
2. 如果知识库没有相关信息，请回复：「抱歉，该问题我暂时无法解答，请联系人工客服。」，禁止编造答案；
3. 回答简洁口语化，不要复杂 markdown 格式；
4. 拒绝回答与业务无关闲聊。
"""

GRADIO_SERVER_NAME = "0.0.0.0"
GRADIO_SERVER_PORT = 7860
