import os
from dotenv import load_dotenv
load_dotenv('.env')

from graph.workflow import graph_workflow

app = graph_workflow()

app.name = "SQL-Workflow"
user_id = "my_user_ids"

if __name__ == "__main__":
    question = "what's (3 + 5) x 7?"

    try:
        from IPython.display import display, Image
        display(Image(app.get_graph().draw_mermaid_png()))

        import config
        main_config = {**config.get_global_config(user_id, thread_id=None), **config.sub_configs.get("supervisor",{})}
        
        print(f"🧔‍♀️사용자 질문) {question}\n")
        reponse = app.invoke({"input": question}, config=main_config)
        print(f"\n🤖Chatbot 응답) {reponse['messages'] if len(reponse['messages']) == 0 else reponse['messages'][-1].content}\n=============================")
    except Exception as e:
        raise e