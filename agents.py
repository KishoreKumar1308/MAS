import openai
import asyncio
from profanity_check import predict_prob
from rich import print_json
from constants import OPEN_AI_KEY
from config import GPT35TurboConfig, GPT41106PreviewConfig
from utils import format_message


class Agent:
    def __init__(self, system_prompt):
        self.system_prompt = system_prompt
        self.client = openai.Client(api_key = OPEN_AI_KEY)

        self.cfg = GPT35TurboConfig().__dict__

    async def get_response(self, user_input, chat_history):
        messages = format_message(self.system_prompt, user_input, chat_history)
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
    

class TaskMinerAgent(Agent):
    def __init__(self, system_prompt, skills):
        super().__init__(system_prompt)
        self.skills = skills
        self.system_prompt = self.set_system_prompt(system_prompt)

        self.cfg = GPT41106PreviewConfig().__dict__


    def set_system_prompt(self,system_prompt):
        system_prompt = system_prompt.replace("{skills}",", ".join(self.skills))
        return system_prompt
    
    async def get_response(self, user_input, chat_history):
        response = await super().get_response(user_input, chat_history)
        print("TASK LIST:")
        print("====================================")
        print(user_input,chat_history)
        print_json(data=response)
        print("====================================")
        return response
   

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