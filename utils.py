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


def format_message(system_prompt: str, user_input: str, chat_history:list)->list:
    formated_messages = [
        {
            'role': 'system',
            'content': f'{system_prompt}'
        }
    ]

    for message in chat_history:
        formated_messages.append({
            'role':'user',
            'content':message[0]
        })

        formated_messages.append({
            'role':'assistant',
            'content':message[1]
        })

    formated_messages.append(
        {
            'role':'user',
            'content':user_input
        }
    )

    return formated_messages