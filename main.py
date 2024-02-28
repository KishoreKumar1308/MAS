import json
import gradio as gr
import asyncio
from rich import print
import agents
from utils import get_curent_datetime, read_agent_prompts
import constants


employee = constants.GARRY

agent_prompts = read_agent_prompts(constants.AGENTS.keys())
_agents = {
        "MasterAgent": agents.MasterAgent(agent_prompts["MasterAgent"], **employee),
        "TaskMinerAgent": agents.TaskMinerAgent(agent_prompts["TaskMinerAgent"], employee["skills"]),
        "ETAAgent": agents.ETAAgent(agent_prompts["ETAAgent"]),
        "ComplianceAgent": agents.ComplianceAgent(agent_prompts["ComplianceAgent"]),
        "PayWallAgent": agents.PayWallAgent(agent_prompts["PayWallAgent"])
}

miner_history = []

async def chat(user_input, chat_history, _agents = _agents):
    formatted_time = get_curent_datetime()
    formatted_query = f"Current Time: {formatted_time} IST User: {user_input}"
    
    print(formatted_query)
    tasks = []
    tasks.append(asyncio.create_task(_agents["TaskMinerAgent"].get_response(formatted_query, miner_history)))

    for agent in list(constants.AGENTS.keys())[2:]:
        task = asyncio.create_task(_agents[agent].get_response(formatted_query, chat_history))
        tasks.append(task)

    responses = await asyncio.gather(*tasks)

    formatted_responses = responses
    miner_history.append((formatted_query,formatted_responses[0]))

    formatted_responses[0] = json.loads(formatted_responses[0])["instructions_for_MasterAgent"]

    formatted_agent_query = {}
    formatted_agent_query["user"] = formatted_query

    for agent, response in zip(list(constants.AGENTS.keys())[1:], formatted_responses):
        formatted_agent_query[agent] = response

    print("Agent's Input for master to generate User response:")
    print("~"*50)
    print(formatted_agent_query)
    print("~"*50)

    master_response = await asyncio.gather(asyncio.create_task(_agents["MasterAgent"].get_response(str(formatted_agent_query), chat_history)))
    
    chat_history.append([user_input, master_response[0]])

    return '',chat_history
    

async def main():
    with gr.Blocks() as demo:

        chatbot = gr.Chatbot(label='MAS - Multi Agent System', height=650, layout = "panel", show_copy_button = True)
        msg = gr.Textbox()
        clear = gr.ClearButton([msg, chatbot])

        msg.submit(chat, [msg, chatbot], [msg, chatbot])

    demo.launch()

if __name__ == "__main__":
    asyncio.run(main())