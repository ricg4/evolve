import modal
import sys
app = modal.App("example-hello-world")
image = (
    modal.Image.debian_slim()
    .pip_install("fastapi[standard]", "openai", "asyncio")
    .add_local_file("index.html", "/root/index.html")
    .add_local_file("prompt.txt", "/root/prompt.txt")
    .add_local_file("apply_diff.py", "/root/apply_diff.py")
    .add_local_file("view_skeleton.py", "/root/parent_program.py")
    .add_local_file("response.txt", "/root/response.txt")
)
@app.function(image=image, secrets=[modal.Secret.from_name("openai-secret")])
@modal.asgi_app()
def fast_api():
    from fastapi import FastAPI, File, UploadFile, Form, Request, HTTPException
    from fastapi.responses import HTMLResponse, StreamingResponse
    from openai import OpenAI
    import asyncio
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
        stream = client.chat.completions.create(
            model="gpt-4o", 
            messages=messages,
            max_tokens=1024,
            temperature=0.7,
            stream = True
        )
        
        # with open("/root/response.txt", "r") as f:
        #     response = f.read()
        
        # return response.choices[0].message.content
        async def event_stream():
            for event in stream:
                word = event.choices[0].delta.content
                if word != None:
                    yield word
                    await asyncio.sleep(0.1)        
        return StreamingResponse(event_stream(), media_type="text/plain")
    return web_app