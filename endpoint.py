import modal
app = modal.App("example-hello-world")
image = (
    modal.Image.debian_slim()
    .pip_install("fastapi[standard]", "openai")
    .add_local_file("index.html", "/root/index.html")
    .add_local_file("prompt.txt", "/root/prompt.txt")
)
@app.function(image=image, secrets=[modal.Secret.from_name("openai-secret")])
@modal.asgi_app()
def fast_api():
    from fastapi import FastAPI, File, UploadFile, Form, Request, HTTPException
    from fastapi.responses import HTMLResponse
    from openai import OpenAI
    web_app = FastAPI()
    @web_app.get("/")
    async def index():
        with open(file="/root/index.html") as f:
            skeleton = f.read()
        return HTMLResponse(content=skeleton)
    @web_app.post("/evolve")
    async def call_api():
        with open("/root/prompt.txt", "r") as f:
            prompt = f.read()
        client = OpenAI()
        messages = [
            {
                "role": "user",
                "content": []
            }
        ]
        messages[0]["content"].append({
            "type": "text",
            "text": prompt
        })
        response = client.chat.completions.create(
            model="gpt-4.1-mini", 
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
        )
        return response.choices[0].message.content
    return web_app