import json
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# ----------------------------
# Load SOP Data
# ----------------------------

with open("sop_data.json", "r") as file:
    sop_data = json.load(file)

# ----------------------------
# Variables
# ----------------------------

conversation_history = []
lead_details = {}

unanswered_questions = 0

# ----------------------------
# Escalation Detection
# ----------------------------

def check_escalation(user_message):

    lower_text = user_message.lower()

    escalation_keywords = [
        "angry",
        "complaint",
        "refund",
        "lawsuit",
        "terrible",
        "frustrated",
        "manager",
        "human",
        "real person"
    ]

    for word in escalation_keywords:
        if word in lower_text:
            return True, f"Detected escalation keyword: {word}"

    return False, ""

# ----------------------------
# FAQ Response
# ----------------------------

def generate_ai_response(user_message):

    system_prompt = f"""
    You are a polite customer support AI for Bloom Aesthetics Clinic.

    ONLY answer using the SOP information provided below.

    If information is not present in SOP:
    - Clearly say you do not have that information
    - Politely escalate to a human agent
    - Never make up information

    SOP DATA:
    {json.dumps(sop_data, indent=2)}

    Tone:
    Friendly, professional, short and clear.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    return response.choices[0].message.content

# ----------------------------
# Lead Qualification
# ----------------------------

def collect_lead_details():

    print("\nBefore we continue, I would like to ask a few quick questions.\n")

    business_type = input("What type of business do you run? : ")
    team_size = input("How many people are in your team? : ")
    current_tools = input("What tools or systems are you currently using? : ")

    lead_details["Business Type"] = business_type
    lead_details["Team Size"] = team_size
    lead_details["Current Tools"] = current_tools

# ----------------------------
# Conversation Summary
# ----------------------------

def generate_summary():

    summary_prompt = f"""
    Create a structured conversation summary.

    Include:
    - Customer Intent
    - Lead Details
    - Important Conversation Points
    - SOP Gaps
    - Recommended Next Action

    Conversation:
    {conversation_history}

    Lead Details:
    {lead_details}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a support conversation summarizer."
            },
            {
                "role": "user",
                "content": summary_prompt
            }
        ]
    )

    return response.choices[0].message.content

# ----------------------------
# Main Workflow
# ----------------------------

print("\n===================================")
print(" Bloom Aesthetics Clinic Assistant ")
print("===================================\n")

collect_lead_details()

while True:

    user_input = input("\nCustomer: ")

    if user_input.lower() == "exit":
        break

    conversation_history.append(f"Customer: {user_input}")

    # Escalation Detection
    escalation, reason = check_escalation(user_input)

    if escalation:

        escalation_message = f"""
This conversation has been escalated to a human support agent.

Reason:
{reason}
"""

        print("\nAI:", escalation_message)

        with open("logs/escalation_logs.txt", "a") as log_file:
            log_file.write(escalation_message + "\n")

        break

    # AI Response
    ai_response = generate_ai_response(user_input)

    conversation_history.append(f"AI: {ai_response}")

    print("\nAI:", ai_response)

# ----------------------------
# Final Summary
# ----------------------------

print("\nGenerating final conversation summary...\n")

summary = generate_summary()

print(summary)

print("\nSession ended successfully.")