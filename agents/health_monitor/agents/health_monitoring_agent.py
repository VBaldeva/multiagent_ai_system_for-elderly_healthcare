import sys
import pandas as pd
import time
import json
from datetime import datetime
from ollama import chat

sys.stdout.reconfigure(encoding='utf-8') 

# Load the cleaned dataset
df = pd.read_csv(r"C:/Users/hp/OneDrive/Desktop/ollama/agents/health_monitor/data/cleaned_health_vitals.csv")
# Function to get latest data entry (simulate real-time)
def get_latest_vitals():
    return df.iloc[-1]  # Assuming the last row is the latest reading

# Define threshold values (customize as needed)
THRESHOLDS = {
    "Heart Rate": (60, 100),
    "Glucose Levels": (70, 140),
    "Oxygen Saturation (SpO₂%)": (95, 100),
    "Systolic BP": (90, 140),
    "Diastolic BP": (60, 90),
}

# Function to check for abnormalities
def check_abnormal_vitals(vitals):
    alerts = []
    for vital, (low, high) in THRESHOLDS.items():
        value = vitals.get(vital)
        if pd.notna(value) and (value < low or value > high):
            alerts.append(f"{vital} is abnormal: {value}")
    return alerts

# Function to consult LLM via Ollama
def consult_llm(alerts, vitals):
    model_name = "mistral"  # or "llama3", "gemma", etc.
    messages = [
        {"role": "user", "content": f"The following abnormalities were detected:\n{alerts}\nVitals: {vitals.to_dict()}\nWhat could this indicate and what actions should be taken?"}
    ]
    try:
        response = chat(model=model_name, messages=messages)
        return response['message']['content']
    except Exception as e:
        print("Error calling Ollama LLM:", e)
        return "Error consulting LLM."
    
def save_health_report(vitals, alerts, llm_suggestion):
    report = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": vitals["Device-ID/User-ID"],
        "abnormalities": alerts,
        "llm_suggestion": llm_suggestion
    }
    with open(r"C:/Users/hp/OneDrive/Desktop/ollama/agents/health_monitor/health_report.json", "w") as f:
        json.dump(report, f, indent=4)
    print("\n📁 Report saved to report.json")


# Main loop (simulate periodic monitoring)
if __name__ == "__main__":
    print("Health Monitoring Agent is running...\n")
    time.sleep(2)
    # vitals = get_latest_vitals()

    vitals=df.iloc[-2]

    print("Latest Vitals:\n", vitals)
    alerts = check_abnormal_vitals(vitals)
    
    if alerts:
        print("\n Alerts Detected:")
        for alert in alerts:
            print("-", alert)

        suggestion = consult_llm(alerts, vitals)
        print("\n🤖 LLM Suggestion:\n", suggestion)

        save_health_report(vitals, alerts, suggestion)
    else:
        print("\n All vitals are within normal range.")

