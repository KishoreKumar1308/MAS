import json
from datetime import datetime

def get_curent_datetime() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def read_agent_prompts(agents: list) -> dict:
    agent_prompts = {}
    for agent in agents:
        agent_prompts[agent] = read_prompt_file(f'prompts/{agent}.txt')
    return agent_prompts


def read_prompt_file(file_path) -> str:
    with open(file_path, 'r') as file:
        return file.read()


def push_to_task_memory(task_list:list,file_path:str):
    with open(file_path, 'w') as file:
        json.dump(task_list, file, indent=4)


def update_assitant_memory(assistant_message:str, file_path:str):
    with open(file_path, 'r') as file:
        task_memory = json.load(file)

    assistant_message = json.loads(assistant_message)
    assistant_message['Task_list'] = task_memory

    return json.dumps(assistant_message, indent=4)