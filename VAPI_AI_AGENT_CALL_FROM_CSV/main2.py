import os
import pandas as pd
import time
from dotenv import load_dotenv
from vapi import Vapi

# Load .env
load_dotenv()

VAPI_API_KEY = os.getenv("VAPI_API_KEY")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

if not all([VAPI_API_KEY, PHONE_NUMBER_ID, ASSISTANT_ID]):
    raise ValueError("Missing VAPI_API_KEY, PHONE_NUMBER_ID, or ASSISTANT_ID in .env")

# Initialize Vapi client
client = Vapi(token=VAPI_API_KEY)

# Load abandoned cart CSV
df = pd.read_csv("abandoned_cart.csv", dtype={"phone": str})

# Prepare log file
log_file = "call_logs.csv"
if not os.path.exists(log_file):
    with open(log_file, "w") as f:
        f.write("timestamp,name,number,items,total,reason,language,status,call_id,call_duration,call_ended_reason\n")

print(f"🚀 Starting calls for {len(df)} abandoned carts...\n")
print(f"📋 Using assistant configuration from Vapi dashboard\n")

# Iterate over customers
for idx, row in df.iterrows():
    phone = row["phone"].strip()
    name = row["name"]
    items = row["items"]
    total = row["total"]
    reason = row["reason"]
    language = row["language"]

    if not phone.startswith("+"):
        print(f"❌ Skipping invalid phone number: {phone}")
        continue

    try:
        # Create call - pass customer data as variables only
        # The first message will come from your Vapi dashboard configuration
        call = client.calls.create(
            assistant_id=ASSISTANT_ID,
            phone_number_id=PHONE_NUMBER_ID,
            customer={
                "number": phone,
                "name": name
            },
            assistant_overrides={
                # Only pass variables, not firstMessage
                "variableValues": {
                    "customerName": name,
                    "items": items,
                    "total": total,
                    "cartReason": reason,
                    "language": language
                }
            }
        )

        status = "initiated"
        call_id = call.id if hasattr(call, 'id') else "unknown"
        call_duration = "pending"
        call_ended_reason = "in_progress"
        
        print(f"✅ Call initiated for {name} → {phone}")
        print(f"   Call ID: {call_id}")
        print(f"   Items: {items} | Total: {total}")
        print(f"   Using dashboard prompt with variables\n")

        # Small delay to avoid rate limiting
        time.sleep(2)

    except Exception as e:
        status = "failed"
        call_id = "N/A"
        call_duration = "0"
        call_ended_reason = str(e)
        print(f"❌ Call failed for {name} → {phone}")
        print(f"   Error: {e}\n")

    # Append to log file
    with open(log_file, "a") as f:
        f.write(
            f"{pd.Timestamp.now()},{name},{phone},{items},{total},{reason},{language},{status},{call_id},{call_duration},{call_ended_reason}\n"
        )

print("=" * 60)
print(f"✓ Completed processing {len(df)} customers")
print(f"✓ Call logs saved to: {log_file}")
print("=" * 60)

print("\n💡 TIPS:")
print("1. Your Vapi dashboard assistant configuration is being used")
print("2. Customer data is passed as variables to personalize the call")
print("3. Use {{customerName}}, {{items}}, {{total}} in your dashboard prompt")
print("4. Check Vapi dashboard for call recordings and transcripts")