from dataclasses import dataclass


@dataclass
class Config:
    model: str = "Qwen2-1.5B-Instruct"
    # model: str = "Mistral-7B-Instruct-v0.3"
    endpoint: str = "http://127.0.0.1:8000"
