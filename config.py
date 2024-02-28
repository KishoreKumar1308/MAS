from dataclasses import dataclass

@dataclass
class GPT35TurboConfig:
    model: str = "gpt-3.5-turbo"
    temprature: float = 0.3
    max_tokens: int = 500
    top_p: float = 1.0


@dataclass
class GPT41106PreviewConfig:
    model: str = "gpt-4-1106-preview"
    temprature: float = 0.3
    max_tokens: int = 1200
    top_p: float = 1.0