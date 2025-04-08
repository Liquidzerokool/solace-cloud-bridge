from fastapi import FastAPI, Request, HTTPException
import httpx
import os

app = FastAPI()
NGROK_ENDPOINT = os.getenv("NGROK_ENDPOINT")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

@app.post("/task")
async def forward_task(request: Request):
    auth = request.headers.get("Authorization")
    if auth != f"Bearer {AUTH_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    task_data = await request.json()

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{NGROK_ENDPOINT}/task",
            headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
            json=task_data,
            timeout=30
        )

    return {"status": "forwarded", "ngrok_response": resp.text}
