import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

API_KEY = "AIzaSyDuknodmQ8T22hsRoWUqNKkQtAg53MkahM"

if not API_KEY:
    raise RuntimeError("GOOGLE_API_KEY is not set in .env or environment variables.")

client = genai.Client(api_key=API_KEY)

app = FastAPI(
    title="Gemini Chatbot API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    text: str

@app.post("/chat/")
async def chat(message: Message):
    try:
        resp = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=message.text
        )
        return {"response": resp.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
