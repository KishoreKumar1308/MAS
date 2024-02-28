import json
import gradio as gr
import asyncio
from rich import print
import agents
from utils import get_curent_datetime, read_agent_prompts
import constants


employee = constants.KELLY

agent_prompts = read_agent_prompts(constants.AGENTS.keys())
_agents = {
        "MasterAgent": agents.MasterAgent(agent_prompts["MasterAgent"], **employee, agent_list = list(constants.AGENTS.items())),
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
    master_response = await asyncio.gather(asyncio.create_task(_agents["MasterAgent"].get_response(formatted_query, chat_history)))
    master_response = json.loads(master_response[0])

    print("Master's input to other agents from User Query:")
    print("#"*50)
    print(master_response)
    print("#"*50)

    tasks = []
    tasks.append(asyncio.create_task(_agents["TaskMinerAgent"].get_response(master_response["TaskMinerAgent"], miner_history)))

    for agent in list(constants.AGENTS.keys())[2:]:
        task = asyncio.create_task(_agents[agent].get_response(master_response[agent], chat_history))
        tasks.append(task)

    responses = await asyncio.gather(*tasks)

    formatted_responses = responses
    miner_history.append((master_response["TaskMinerAgent"],formatted_responses[0]))

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

    return master_response[0]
    

async def main():
    iface = gr.ChatInterface(
        chat,
        chatbot = gr.Chatbot(layout = "panel",show_copy_button = True),
        title = "MAS - Multi Agent System",
    )

    iface.launch()

if __name__ == "__main__":
    asyncio.run(main())