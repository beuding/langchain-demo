from dotenv import load_dotenv
import gradio as gr
from langgraph.checkpoint.sqlite import SqliteSaver
from chat_model import get_llm, get_embedding
from vector_store import init_vector_store, search_knowledge
from agent_builder import build_agent
import vector_store

load_dotenv()

from config import (
    SYSTEM_PROMPT_TPL,
    GRADIO_SERVER_NAME,
    GRADIO_SERVER_PORT,
    TOP_K,
    CHECKPOINT_DB_PATH
)

agent = None
llm = None
tools = None
current_system_prompt = SYSTEM_PROMPT_TPL
THREAD_ID = "gradio_demo_session"   

def chat_response(message, history):
    try:
        with SqliteSaver.from_conn_string(CHECKPOINT_DB_PATH) as checkpointer:
            chat_agent = build_agent(llm, tools, current_system_prompt, checkpointer=checkpointer)
            config = {"configurable": {"thread_id": THREAD_ID}}
            knowledge = search_knowledge.invoke({"query": message})
            input_state = {
                "messages": [{
                    "role": "user",
                    "content": (
                        f"用户问题：{message}\n\n"
                        f"已检索到的知识库内容：\n{knowledge}\n\n"
                        "请只依据以上知识库内容回答用户问题。"
                    ),
                }]
            }
            resp = chat_agent.invoke(input_state, config=config)

            messages = resp.get("messages", [])
            if messages:
                last_msg = messages[-1]
                return getattr(last_msg, "content", str(last_msg))
            return str(resp)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"执行异常：{str(e)}"

def update_prompt(new_prompt):
    global agent, current_system_prompt
    # 更新提示词，重新构建agent graph
    current_system_prompt = new_prompt
    agent = build_agent(llm, tools, new_prompt)
    return "✅ 系统提示词更新成功！新对话将生效"


def build_ui():
    with gr.Blocks(title="智能客服助手 Demo") as demo:
        gr.Markdown("# 智能客服助手 Demo")
        gr.Markdown("基于私有知识库 RAG + LangGraph Agent，对话记忆持久化SQLite")
        with gr.Accordion("⚙️ 动态修改系统提示词", open=False):
            prompt_input = gr.Textbox(
                value=SYSTEM_PROMPT_TPL,
                label="系统提示词",
                lines=10
            )
            update_btn = gr.Button("更新提示词")
            msg_output = gr.Textbox(label="状态反馈")
            update_btn.click(
                fn=update_prompt,
                inputs=[prompt_input],
                outputs=[msg_output]
            )
        gr.ChatInterface(
            fn=chat_response,
            examples=["休假政策是什么？", "报销政策是什么？", "离职流程是什么？"],
        )
    return demo


if __name__ == "__main__":
    try:
        llm = get_llm()
        embedding = get_embedding()
        vectordb = init_vector_store(embedding)
        vector_store.retriever = vectordb.as_retriever(search_kwargs={"k": TOP_K})
        tools = [search_knowledge]
        agent = build_agent(llm, tools, current_system_prompt)
        demo = build_ui()
        demo.launch(server_name=GRADIO_SERVER_NAME, server_port=GRADIO_SERVER_PORT, share=False)
    except Exception as e:
        import traceback
        print("\n程序初始化异常")
        traceback.print_exc()
