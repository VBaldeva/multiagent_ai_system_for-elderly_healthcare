import sys
import pandas as pd
import time
from ollama import chat

# Ensure console supports UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Load cleaned data
df = pd.read_csv(r"C:/Users/hp/OneDrive/Desktop/ollama/agents/safety_monitoring/data/cleaned_safety_monitoring.csv")

# Drop unnamed column if exists
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# Function to get the latest activity
def get_latest_activity():
    return df.iloc[-1]

# Function to check safety abnormalities
def check_safety_risks(activity):
    risks = []

    if activity['Fall Detected (Yes/No)'] == 1:
        risks.append("Fall Detected")

    if pd.notna(activity['Impact Force Level']) and activity['Impact Force Level'] > 5:
        risks.append(f"High Impact Force: {activity['Impact Force Level']}")

    if pd.notna(activity['Post-Fall Inactivity Duration (Seconds)']) and activity['Post-Fall Inactivity Duration (Seconds)'] > 30:
        risks.append(f"Prolonged Inactivity: {activity['Post-Fall Inactivity Duration (Seconds)']} seconds")

    return risks

# Function to consult Ollama for smart suggestions
def consult_llm_with_context(risks, activity):
    model_name = "mistral"  # Change to llama3, gemma, etc. as needed
    messages = [
        {
            "role": "user",
            "content": f"""
The following safety issues were detected: {risks}
Here is the full context of the user's latest activity:
{activity.to_dict()}

What could be the possible causes of this situation? Suggest possible actions or precautions for a caregiver.
"""
        }
    ]

    try:
        response = chat(model=model_name, messages=messages)
        print("\nLLM Suggestion:\n", response['message']['content'])
    except Exception as e:
        print("Error calling Ollama LLM:", e)

# Main agent loop
if __name__ == "__main__":
    print("Safety Monitoring Agent is running...\n")
    time.sleep(2)

    activity = get_latest_activity()
    print("Latest Activity:\n", activity)

    risks = check_safety_risks(activity)

    if risks:
        print("\n Safety Concerns Detected:")
        for risk in risks:
            print("-", risk)
        consult_llm_with_context(risks, activity)

            # Generate JSON report
        from datetime import datetime
        import json

        report = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": activity.get("User ID", "unknown"),
            "risks_detected": risks,
            "activity_details": activity.to_dict()
        }

        with open(r"C:/Users/hp/OneDrive/Desktop/ollama/agents/safety_monitoring/safety_report.json", "w") as f:
            json.dump(report, f, indent=4)

        print("\n📁 Safety report saved as safety_report.json")

