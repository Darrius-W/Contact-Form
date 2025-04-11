from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from email.message import EmailMessage
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Contact form data model
class ContactData(BaseModel):
    name: str
    email: EmailStr
    message: str

# All domains to allow CORS
origins = [
    "http://localhost:3000",
    "http://localhost:8000/sendMsg"
]

# Middleware configuration for Cross-Origin Resource Sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)

# Grab contact form data and forward to personal email
@app.post('/sendMsg')
async def forward_msg(data: ContactData):
    sender_email = os.getenv("EMAIL_USER")
    sender_pass = os.getenv("EMAIL_PASS")
    receiver_email = os.getenv("EMAIL_RECEIVER", sender_email)
    
    # Create email
    subject = f"New message from {data.name}"
    content = f"""
    You received a new contact submission:
    
    Name: {data.name}
    Email: {data.email}
    Message: {data.message}
    """
    
    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.set_content(content)
    
    # Send the email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_pass)
            smtp.send_message(msg)
        return {"message": "Email sent successfully"}
    
    except Exception as e:
        return {"error": str(e)}