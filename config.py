import uuid
from langchain_core.runnables import RunnableConfig


def get_global_config(user_id=None, thread_id=None) -> RunnableConfig:
    return {
        "configurable": {
            "thread_id": thread_id or str(uuid.uuid4())
        },
        "metadata": {
            "user_id": user_id,
            "env": "prod"
        },
        "tags": ["prod", "chat"],
        "max_concurrency": 50,
        "run_name": "main_workflow",
    }

sub_configs = {
    "supervisor": {
        "recursion_limit": 10
    }
}