from config import GPT35TurboConfig, GPT41106PreviewConfig

class Agent:
    def __init__(self):
        self.cfg = GPT35TurboConfig()


ag = Agent()
print(ag.cfg.__dict__)