from dataclasses import dataclass


@dataclass
class Config:
    model: str = "Qwen2-1.5B-Instruct"
    endpoint: str = "http://127.0.0.1:8000"
