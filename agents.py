import openai
import asyncio
import json
from profanity_check import predict_prob
from rich import print_json
import chromadb
import constants
from config import GPT35TurboConfig, GPT41106PreviewConfig
from utils import update_assitant_memory,get_curent_datetime


class Agent:
    def __init__(self, system_prompt):
        self.system_prompt = system_prompt
        self.client = openai.Client(api_key = constants.OPEN_AI_KEY)

        self.cfg = GPT35TurboConfig().__dict__


    def format_message(self, system_prompt: str, user_input: str, chat_history:list)->list:
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

    async def get_response(self, user_input, chat_history):
        messages = self.format_message(self.system_prompt, user_input, chat_history)
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: self.client.chat.completions.create(
            model = self.cfg['model'],
            messages = messages,
            temperature = self.cfg['temprature'],
            max_tokens = self.cfg['max_tokens'],
            top_p = self.cfg['top_p']
        ))
        
        out = dict(response)
        out = dict(out['choices'][0])
        out = dict(out['message'])
        out = out['content']

        return out


class MasterAgent(Agent):
    def __init__(self, system_prompt, name, role, skills):
        super().__init__(system_prompt)
        self.name = name
        self.role = role
        self.skills = skills
        self.system_prompt = self.set_system_prompt(self.system_prompt)

        self.cfg = GPT41106PreviewConfig().__dict__
    
    def set_system_prompt(self,system_prompt):
        system_prompt = system_prompt.replace("{name}",self.name)
        system_prompt = system_prompt.replace("{role}",self.role)
        system_prompt = system_prompt.replace("{skills}",", ".join(self.skills))
        return system_prompt
    

class MemoryAgent(Agent):
    def __init__(self, system_prompt):
        super().__init__(system_prompt)
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.get_or_create_collection(name = "meomry",metadata = {"hnsw:space": "cosine"})

    def add_to_collection(self, docs):
        self.collection.add(documents = docs,ids = get_curent_datetime())

    def retrieve_data(self,query,number_of_documents):
        results = self.collection.query(
                    query_texts=[query],
                    n_results=number_of_documents)   
        return results
    
    def get_data(self):
        return self.collection.get()


class TaskMinerAgent(Agent):
    def __init__(self, system_prompt, skills):
        super().__init__(system_prompt)
        self.skills = skills
        self.system_prompt = self.set_system_prompt(system_prompt)

        self.cfg = GPT41106PreviewConfig().__dict__


    def format_message(self, system_prompt: str, user_input: str, chat_history: list, memory:str) -> list:
        system_prompt = system_prompt.replace("{memory}",str(memory["documents"]))

        formated_messages = [
        {
            'role': 'system',
            'content': f'{system_prompt}'
        }
        ]

        if len(chat_history) > 0:
            user_messages = [messages[0] for messages in chat_history[-10:]]
            formated_messages.append({
                'role':'user',
                'content':f'Here are the last 10 user messages: {user_messages}'
            })

            formated_messages.append({
                'role':'assistant',
                'content':update_assitant_memory(chat_history[-1][1], constants.TASK_MEMORY)
            })

        formated_messages.append(
        {
            'role':'user',
            'content':user_input
        }
        )

        print("--------->>>>>>>> TASK MINER")
        print_json(data = formated_messages)
        return formated_messages
         

    def set_system_prompt(self,system_prompt):
        system_prompt = system_prompt.replace("{skills}",", ".join(self.skills))
        return system_prompt
    

    async def get_response(self, user_input, chat_history, memory):
        messages = self.format_message(self.system_prompt, user_input, chat_history, memory)
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: self.client.chat.completions.create(
            model = self.cfg['model'],
            messages = messages,
            temperature = self.cfg['temprature'],
            max_tokens = self.cfg['max_tokens'],
            top_p = self.cfg['top_p']
        ))
        
        out = dict(response)
        out = dict(out['choices'][0])
        out = dict(out['message'])
        out = out['content']

        print("TASK LIST:")
        print("====================================")
        print(user_input,chat_history)
        print_json(data=json.loads(str(out)))
        print("====================================")

        return out
   

# Hardcoded for now, to be implemented in future
class ETAAgent(Agent):
    def __init__(self, system_prompt):
        super().__init__(system_prompt)

    async def get_response(self, user_input, chat_history):
        if "eta" in user_input.lower():
            return "Task is currently being executed. It is expected to be completed in 2 hours. You will be notified once it is completed."
        return ""
    

# Hardcoded for now, to be implemented in future
class ComplianceAgent(Agent):
    def __init__(self, system_prompt):
        super().__init__(system_prompt)

    async def get_response(self, user_input, chat_history):
        # Check if the task is compliant with the company policy based on presence of inappropriate words
        if predict_prob([user_input])[0] > 0.5:
            return "Your request contains inappropriate words. This goes against our Company policy. Please rephrase your message."
        return ""
        

# Hardcoded for now, to be implemented in future
class PayWallAgent(Agent):
    def __init__(self, system_prompt):
        super().__init__(system_prompt)

    async def get_response(self, user_input, chat_history):
        if len(chat_history) > 30:
            return "You have reached the maximum number of free requests. Please subscribe to our premium plan to continue."
        return ""