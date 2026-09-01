from langchain.agents import create_agent
from config import SYSTEM_PROMPT_TPL

def build_agent(llm, tools, system_prompt: str = SYSTEM_PROMPT_TPL, checkpointer=None):
    """
    创建Agent Graph对象
    :param llm: 大模型实例
    :param tools: 工具列表
    :param system_prompt: 系统提示词
    :return: agent graph
    """
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt,
        checkpointer=checkpointer
    )
    return agent
