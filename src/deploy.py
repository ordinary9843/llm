import os
from typing import List
from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn
from transformers import AutoModelForCausalLM, AutoTokenizer
from config import Config
from logger import logger


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


config = Config()
model_path = os.path.join(BASE_DIR, "..", "models", config.model)

try:
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        device_map="auto",
        trust_remote_code=True,
    )
    logger.info("Model loaded successfully!")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    raise

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


class TranslateRequest(BaseModel):
    word: str
    languages: List[str]


@app.post("/v1/translate")
async def translate_word(request: TranslateRequest):
    try:
        word = request.word
        languages = request.languages
        translations = {}
        for lang in languages:
            prompt = f"<|im_start|>user\nTranslate '{word}' into {lang} language (using ISO 639-1 or 639-3 code, e.g., zh-tw for Traditional Chinese, es for Spanish). Return only the translated word, no additional explanation.<|im_end|>\n<|im_start|>assistant\n"
            inputs = tokenizer(
                prompt, return_tensors="pt", truncation=True, max_length=2048
            ).to(model.device)
            outputs = model.generate(
                inputs.input_ids,
                max_new_tokens=500,
                temperature=0.3,
                top_p=0.9,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
            )
            translated_text = tokenizer.decode(
                outputs[0][inputs.input_ids.shape[-1] :], skip_special_tokens=True
            ).strip()
            translations[lang] = translated_text

        return {"word": word, "translations": translations}
    except Exception as e:
        return {"error": f"Failed to translate: {str(e)}"}


class GenerateRequest(BaseModel):
    prompt: str


@app.post("/v1/generate")
async def generate_text(request: GenerateRequest):
    try:
        prompt = (
            f"<|im_start|>user\n{request.prompt}<|im_end|>\n<|im_start|>assistant\n"
        )
        inputs = tokenizer(
            prompt, return_tensors="pt", truncation=True, max_length=2048
        ).to(model.device)
        outputs = model.generate(
            inputs.input_ids,
            max_new_tokens=500,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )
        generated_text = tokenizer.decode(
            outputs[0][inputs.input_ids.shape[-1] :], skip_special_tokens=True
        ).strip()

        return {"prompt": request.prompt, "generated_text": generated_text}

    except Exception as e:
        return {"error": f"Failed to generate text: {str(e)}"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
