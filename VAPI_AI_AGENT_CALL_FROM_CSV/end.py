import os
import pandas as pd
from dotenv import load_dotenv
from vapi import Vapi  # your installed SDK

# Load .env
load_dotenv()

VAPI_API_KEY = os.getenv("VAPI_API_KEY")        # PRIVATE key from VAPI dashboard
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")  # UUID of your attached phone number
ASSISTANT_ID = os.getenv("ASSISTANT_ID")        # UUID of your assistant

if not all([VAPI_API_KEY, PHONE_NUMBER_ID, ASSISTANT_ID]):
    raise ValueError("Missing VAPI_API_KEY, PHONE_NUMBER_ID, or ASSISTANT_ID in .env")

# Initialize Vapi client
client = Vapi(token=VAPI_API_KEY)

# Load abandoned cart CSV (ensure phone numbers are strings)
df = pd.read_csv("abandoned_cart.csv", dtype={"phone": str})

# Prepare log file
log_file = "call_logs.csv"
if not os.path.exists(log_file):
    with open(log_file, "w") as f:
        f.write("timestamp,name,number,items,total,reason,language,status,call_id\n")

# Iterate over customers
for _, row in df.iterrows():
    phone = row["phone"].strip()

    if not phone.startswith("+"):
        print(f"Skipping invalid phone number: {phone}")
        continue

    try:
        # Create call with messages list
        call = client.calls.create(
            assistant_id=ASSISTANT_ID,
            phone_number_id=PHONE_NUMBER_ID,
            customer={
                "number": phone,
                "name": row["name"]
            },
            messages=[
                {
                    "type": "text",
                    "text": f"Hi {row['name']}, I see you left {row['items']} in your cart totaling {row['total']}. Can I help you complete your purchase?"
                },
                {
                    "type": "voicemail",
                    "text": "Please call back when you're available."
                },
                {
                    "type": "end",
                    "text": "Thank you! Goodbye."
                }
            ]
        )

        status = "success"
        call_id = call.id
        print(f"📞 Call processed for {row['name']} → {phone} | Call ID: {call_id}")

    except Exception as e:
        status = "failed"
        call_id = str(e)
        print(f"❌ Call failed for {row['name']} → {phone}: {e}")

    # Append to log file
    with open(log_file, "a") as f:
        f.write(
            f"{pd.Timestamp.now()},{row['name']},{phone},{row['items']},{row['total']},{row['reason']},{row['language']},{status},{call_id}\n"
        )
