import os
from fastapi import FastAPI
from groq import Groq
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# ----------------------------
# Fake Abandoned Cart Data
# ----------------------------
FAKE_CART = {
    "customer_name": "Rahul Sharma",
    "phone": "+917499902809",  # <-- your testing number
    "items": ["Wireless Headphones", "Bluetooth Speaker"],
    "cart_value": 4098,
    "discount_code": "SAVE10"
}

# ----------------------------
# AI Script Generator
# ----------------------------
def generate_script(cart):
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""
    Create a polite 20-second call script.

    Customer: {cart['customer_name']}
    Items: {', '.join(cart['items'])}
    Cart Value: ₹{cart['cart_value']}
    Discount Code: {cart['discount_code']}

    Script should be friendly and simple.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    # Correct way to access message content
    return response.choices[0].message.content

# ----------------------------
# Twilio Call
# ----------------------------
def call_customer_twilio(message, phone):
    client = Client(
        os.getenv("TWILIO_ACCOUNT_SID"),
        os.getenv("TWILIO_AUTH_TOKEN")
    )

    call = client.calls.create(
        to=phone,
        from_=os.getenv("TWILIO_NUMBER"),
        twiml=f"<Response><Say>{message}</Say></Response>"
    )

    return call.sid

# ----------------------------
# API Endpoint
# ----------------------------
@app.get("/call-customer")
def call_customer():
    script = generate_script(FAKE_CART)
    sid = call_customer_twilio(script, FAKE_CART["phone"])

    return {
        "status": "call started",
        "call_sid": sid,
        "script": script
    }
