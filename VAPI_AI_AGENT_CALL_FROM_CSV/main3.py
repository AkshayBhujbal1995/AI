import os
import pandas as pd
import time
from datetime import datetime
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

# Enhanced log file with comprehensive tracking
log_file = "call_logs_detailed.csv"

# Create detailed CSV header if file doesn't exist
if not os.path.exists(log_file):
    with open(log_file, "w") as f:
        headers = [
            # Basic Info
            "timestamp",
            "call_date",
            "call_time",
            "customer_name",
            "customer_phone",
            
            # Cart Info
            "cart_items",
            "cart_total",
            "cart_quantity",
            "cart_abandoned_date",
            "days_since_abandonment",
            
            # Call Status
            "call_id",
            "call_status",
            "call_initiated",
            "call_answered",
            "call_duration_seconds",
            "call_ended_reason",
            
            # Customer Response
            "customer_sentiment",
            "customer_interest_level",
            "customer_engagement_score",
            
            # Objections & Reasons
            "primary_objection",
            "secondary_objection",
            "objection_details",
            "price_concern",
            "quality_concern",
            "timing_concern",
            "technical_issue",
            "competitor_mention",
            "changed_mind",
            "not_interested",
            "just_browsing",
            
            # Conversion Info
            "conversion_result",
            "purchase_completed",
            "purchase_amount",
            "discount_offered",
            "discount_accepted",
            "discount_amount",
            
            # AI Performance
            "ai_technique_used",
            "objection_handled_successfully",
            "rapport_established",
            "follow_up_scheduled",
            "follow_up_date",
            
            # Customer Behavior
            "callback_requested",
            "voicemail_left",
            "hung_up_early",
            "call_back_attempts",
            "previous_contact_count",
            
            # Additional Data
            "customer_language",
            "customer_location",
            "customer_timezone",
            "time_of_day",
            "day_of_week",
            
            # Notes & Learning
            "call_notes",
            "ai_learnings",
            "improvement_suggestions",
            "script_effectiveness_rating"
        ]
        f.write(",".join(headers) + "\n")

print(f"🚀 Starting enhanced call tracking for {len(df)} abandoned carts...\n")
print(f"📊 Detailed analytics will be saved to: {log_file}\n")

# Iterate over customers
for idx, row in df.iterrows():
    phone = row["phone"].strip()
    name = row["name"]
    items = row["items"]
    total = row["total"]
    reason = row.get("reason", "Unknown")
    language = row.get("language", "en")

    if not phone.startswith("+"):
        print(f"❌ Skipping invalid phone number: {phone}")
        continue

    # Get current timestamp
    now = datetime.now()
    call_date = now.strftime("%Y-%m-%d")
    call_time = now.strftime("%H:%M:%S")
    day_of_week = now.strftime("%A")
    time_of_day = "Morning" if now.hour < 12 else "Afternoon" if now.hour < 17 else "Evening"

    try:
        # Create call with enhanced metadata
        call = client.calls.create(
            assistant_id=ASSISTANT_ID,
            phone_number_id=PHONE_NUMBER_ID,
            customer={
                "number": phone,
                "name": name
            },
            assistant_overrides={
                "variableValues": {
                    "customerName": name,
                    "items": items,
                    "total": total,
                    "cartReason": reason,
                    "language": language,
                    "callDate": call_date,
                    "callTime": call_time
                }
            }
        )

        call_id = call.id if hasattr(call, 'id') else "unknown"
        
        # Initialize default values (these will be updated after call completes)
        log_data = {
            # Basic Info
            "timestamp": now,
            "call_date": call_date,
            "call_time": call_time,
            "customer_name": name,
            "customer_phone": phone,
            
            # Cart Info
            "cart_items": items,
            "cart_total": total,
            "cart_quantity": items.split("x")[1] if "x" in items else "1",
            "cart_abandoned_date": "Unknown",
            "days_since_abandonment": "Unknown",
            
            # Call Status
            "call_id": call_id,
            "call_status": "initiated",
            "call_initiated": "Yes",
            "call_answered": "Pending",
            "call_duration_seconds": "0",
            "call_ended_reason": "in_progress",
            
            # Customer Response
            "customer_sentiment": "Pending",
            "customer_interest_level": "Pending",
            "customer_engagement_score": "Pending",
            
            # Objections & Reasons (Initialize all as No)
            "primary_objection": "Pending",
            "secondary_objection": "None",
            "objection_details": "Pending",
            "price_concern": "No",
            "quality_concern": "No",
            "timing_concern": "No",
            "technical_issue": "No",
            "competitor_mention": "No",
            "changed_mind": "No",
            "not_interested": "No",
            "just_browsing": "No",
            
            # Conversion Info
            "conversion_result": "Pending",
            "purchase_completed": "No",
            "purchase_amount": "0",
            "discount_offered": "No",
            "discount_accepted": "No",
            "discount_amount": "0",
            
            # AI Performance
            "ai_technique_used": "Barnum Effect, Reciprocity",
            "objection_handled_successfully": "Pending",
            "rapport_established": "Pending",
            "follow_up_scheduled": "No",
            "follow_up_date": "None",
            
            # Customer Behavior
            "callback_requested": "No",
            "voicemail_left": "No",
            "hung_up_early": "No",
            "call_back_attempts": "1",
            "previous_contact_count": "0",
            
            # Additional Data
            "customer_language": language,
            "customer_location": "Unknown",
            "customer_timezone": "Unknown",
            "time_of_day": time_of_day,
            "day_of_week": day_of_week,
            
            # Notes & Learning
            "call_notes": f"Call initiated to {name} for {items}",
            "ai_learnings": "To be updated after call completion",
            "improvement_suggestions": "To be analyzed",
            "script_effectiveness_rating": "Pending"
        }
        
        print(f"✅ Call initiated for {name} → {phone}")
        print(f"   Call ID: {call_id}")
        print(f"   Items: {items} | Total: {total}")
        print(f"   Day: {day_of_week} | Time: {time_of_day}\n")
        
        # Write to CSV
        with open(log_file, "a") as f:
            f.write(",".join([str(log_data[h]) for h in log_data.keys()]) + "\n")

        # Small delay to avoid rate limiting
        time.sleep(2)

    except Exception as e:
        error_log = {
            "timestamp": now,
            "call_date": call_date,
            "call_time": call_time,
            "customer_name": name,
            "customer_phone": phone,
            "cart_items": items,
            "cart_total": total,
            "cart_quantity": "Unknown",
            "cart_abandoned_date": "Unknown",
            "days_since_abandonment": "Unknown",
            "call_id": "N/A",
            "call_status": "failed",
            "call_initiated": "Yes",
            "call_answered": "No",
            "call_duration_seconds": "0",
            "call_ended_reason": f"Error: {str(e)}",
            "customer_sentiment": "Unknown",
            "customer_interest_level": "Unknown",
            "customer_engagement_score": "0",
            "primary_objection": "Technical Error",
            "secondary_objection": "None",
            "objection_details": str(e),
            "price_concern": "No",
            "quality_concern": "No",
            "timing_concern": "No",
            "technical_issue": "Yes",
            "competitor_mention": "No",
            "changed_mind": "No",
            "not_interested": "No",
            "just_browsing": "No",
            "conversion_result": "Failed",
            "purchase_completed": "No",
            "purchase_amount": "0",
            "discount_offered": "No",
            "discount_accepted": "No",
            "discount_amount": "0",
            "ai_technique_used": "None - Call Failed",
            "objection_handled_successfully": "No",
            "rapport_established": "No",
            "follow_up_scheduled": "No",
            "follow_up_date": "None",
            "callback_requested": "No",
            "voicemail_left": "No",
            "hung_up_early": "No",
            "call_back_attempts": "1",
            "previous_contact_count": "0",
            "customer_language": language,
            "customer_location": "Unknown",
            "customer_timezone": "Unknown",
            "time_of_day": time_of_day,
            "day_of_week": day_of_week,
            "call_notes": f"Call failed: {str(e)}",
            "ai_learnings": "System error - needs investigation",
            "improvement_suggestions": "Fix technical issues",
            "script_effectiveness_rating": "0"
        }
        
        print(f"❌ Call failed for {name} → {phone}")
        print(f"   Error: {e}\n")
        
        with open(log_file, "a") as f:
            f.write(",".join([str(error_log[h]) for h in error_log.keys()]) + "\n")

print("=" * 70)
print(f"✓ Completed processing {len(df)} customers")
print(f"✓ Detailed call logs saved to: {log_file}")
print("=" * 70)

print("\n📊 TRACKED VARIABLES (58 data points per call):")
print("""
✅ BASIC INFO (5): timestamp, date, time, name, phone
✅ CART DATA (5): items, total, quantity, abandoned date, days since
✅ CALL STATUS (6): ID, status, initiated, answered, duration, end reason
✅ SENTIMENT (3): sentiment, interest level, engagement score
✅ OBJECTIONS (11): primary, secondary, price, quality, timing, technical, 
                    competitor, changed mind, not interested, browsing
✅ CONVERSION (6): result, completed, amount, discount offered/accepted/amount
✅ AI PERFORMANCE (5): technique used, objection handled, rapport, follow-up
✅ BEHAVIOR (6): callback requested, voicemail, hung up, attempts, previous contacts
✅ CONTEXT (5): language, location, timezone, time of day, day of week
✅ LEARNING (4): notes, AI learnings, improvements, effectiveness rating

Total: 58 variables for comprehensive AI learning!
""")