import requests

url = "http://localhost:8000/v1/chat/completions"
payload = {
    "messages": [{"role": "user", "content": "將 'Hello, world!' 翻譯成繁體中文"}]
}
response = requests.post(url, json=payload)
print(response.json()["choices"][0]["message"]["content"])
