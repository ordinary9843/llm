import os
from fastapi import FastAPI, Request
import uvicorn
from transformers import AutoModelForCausalLM, AutoTokenizer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "7B-Instruct-v0.3")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    device_map="auto",
    trust_remote_code=True,
)
app = FastAPI()


@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()
    messages = body.get("messages", [])
    user_prompt = "".join(msg["content"] for msg in messages if msg["role"] == "user")
    inputs = tokenizer(user_prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        inputs.input_ids, max_length=2048, temperature=0.7, do_sample=True
    )
    generated_text = tokenizer.decode(
        outputs[0][inputs.input_ids.shape[-1] :], skip_special_tokens=True
    )

    return {"choices": [{"message": {"content": generated_text}}]}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
