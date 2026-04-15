from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","https://personal-portfolio-one-phi-85.vercel.app"], 
    allow_methods=["*"],
    allow_headers=["*"],
)
class ContactForm(BaseModel):
     name:str
     email:str
     message:str

@app.get("/")
def root():
    return {"status": "API working"}     

@app.post("/send-message")
async def submit_contact(form:ContactForm):
     text = f"New Message!\n Name: {form.name}\n Email: {form.email}\n Message: {form.message}"
     async with httpx.AsyncClient() as client:
       try:
         response = await client.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", json={"chat_id":CHAT_ID,"text":text})  
         response.raise_for_status()
       except httpx.HTTPError as exc:
            return {"success":False, "detail":f"HTTP Exception for {exc.request.url} - {str(exc)}"}
       except Exception as exc:
           return {"success":False, "detail":f"HTTP Exception for {str(exc)}"}
       
       return {"success":True,"detail":"Message sent!"}
      
          
       
                
      
       