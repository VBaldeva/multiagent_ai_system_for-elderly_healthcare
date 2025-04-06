import sys
import json
import os
from datetime import datetime
import pyttsx3
import ollama

sys.stdout.reconfigure(encoding='utf-8')

# Initialize TTS engine
tts_engine = pyttsx3.init()

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

# Load a JSON report safely
def load_report(path):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        with open(path, "r") as f:
            return json.load(f)
    print(f"⚠️ Warning: File '{path}' is missing or empty.")
    return None


# Load all agent reports
daily_routine = load_report(r"C:/Users/hp/OneDrive/Desktop/ollama/agents/daily_routine/daily_report.json")
health_monitor = load_report(r"C:/Users/hp/OneDrive/Desktop/ollama/agents/health_monitor/health_report.json")
safety_monitor = load_report(r"C:/Users/hp/OneDrive/Desktop/ollama/agents/safety_monitoring/safety_report.json")

# Build the unified context
summary_input = "Unified Elderly Care Report:\n\n"

if daily_routine:
    summary_input += f"🕒 Daily Routine:\n- Reminder Type: {daily_routine['reminder_type']}\n"
    for issue in daily_routine["issues"]:
        summary_input += f"  • {issue}\n"
else:
    summary_input += "🕒 Daily Routine: No issues reported.\n"

if health_monitor:
    summary_input += "\n❤️ Health Monitoring:\n"
    for issue in health_monitor["abnormalities"]:
        summary_input += f"  • {issue}\n"
else:
    summary_input += "\n❤️ Health Monitoring: All vitals normal.\n"

if safety_monitor:
    summary_input += "\n🛡️ Safety Monitoring:\n"
    for issue in safety_monitor["risks_detected"]:
        summary_input += f"  • {issue}\n"
else:
    summary_input += "\n🛡️ Safety Monitoring: No safety concerns detected.\n"

summary_input += "\nProvide a helpful summary for the caregiver with insights and possible actions.\n"

# Query LLM for insights
response = ollama.chat(
    model="mistral",
    messages=[{"role": "user", "content": summary_input}]
)

summary_output = response['message']['content']

# Print + Speak summary
print("\n🧠 Caregiver Summary:\n", summary_output)
speak("Here is the unified summary for the caregiver.")
speak(summary_output)

# Save to JSON
unified_report = {
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "summary": summary_output
}

with open("unified_report.json", "w") as f:
    json.dump(unified_report, f, indent=4)

print("\n📁 Unified report saved to unified_report.json")
