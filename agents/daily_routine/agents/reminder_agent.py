import sys
import pandas as pd
from datetime import datetime
import ollama
import pyttsx3
import json

# Initialize TTS engine
tts_engine = pyttsx3.init()

sys.stdout.reconfigure(encoding='utf-8')

def speak(text):
    """Speak the provided text aloud using TTS"""
    tts_engine.say(text)
    tts_engine.runAndWait()

def load_cleaned_data(csv_path):
    df = pd.read_csv(csv_path)
    
    # Parse datetime columns
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    df["Scheduled Time"] = pd.to_datetime(df["Scheduled Time"], errors="coerce")

    return df

def detect_missed_reminders(df):
    now = datetime.now()
    recent_reminder = df.iloc[-1]

    issues = []

    if recent_reminder["Reminder Sent (Yes/No)"] == 0:
        issues.append("- Reminder was not sent.")

    if recent_reminder["Acknowledged (Yes/No)"] == 0:
        issues.append("- Reminder was not acknowledged.")

    if recent_reminder["Scheduled Time"] < now and recent_reminder["Acknowledged (Yes/No)"] == 0:
        issues.append("- Reminder is past due and still not acknowledged.")

    return recent_reminder, issues

def ask_llm_for_suggestions(recent_reminder):
    prompt = f"""
You are a helpful healthcare assistant. The system missed a reminder for the elderly user.

Reminder Details:
- Type: {recent_reminder['Reminder Type']}
- Scheduled Time: {recent_reminder['Scheduled Time']}
- Reminder Sent: {bool(recent_reminder['Reminder Sent (Yes/No)'])}
- Acknowledged: {bool(recent_reminder['Acknowledged (Yes/No)'])}

Provide strategies to avoid missed or unacknowledged reminders in the future. Keep the tone informative and supportive.
"""
    response = ollama.chat(model="mistral", messages=[
        {"role": "user", "content": prompt}
    ])
    return response['message']['content']


def generate_report_json(recent_reminder, issues,suggestion):
    """Generate a JSON report file with reminder details and issues."""
    report = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": recent_reminder["Device-ID/User-ID"],
        "reminder_type": recent_reminder["Reminder Type"],
        "scheduled_time": recent_reminder["Scheduled Time"].strftime("%Y-%m-%d %H:%M:%S"),
        "issues": issues
    }
    if suggestion:
       report["llm_suggestion"] = suggestion  # 👈 Add this


    with open(r"C:/Users/hp/OneDrive/Desktop/ollama/agents/daily_routine/daily_report.json", "w") as f:
        json.dump(report, f, indent=4)
    print("\n📁 Report saved to report.json")


def main():
    print("📅 Daily Routine Agent is running...\n")

    df = load_cleaned_data(r"C:/Users/hp/OneDrive/Desktop/ollama/agents/daily_routine/data/cleaned_reminders.csv")
    recent_reminder, issues = detect_missed_reminders(df)

    print("🔔 Latest Reminder:")
    print(recent_reminder.to_string())
    print()

    reminder_text = f"You have a {recent_reminder['Reminder Type']} scheduled at {recent_reminder['Scheduled Time'].strftime('%I:%M %p')}."
    speak(reminder_text)

    if issues:
        print("⚠️ Issues Detected:")
        for issue in issues:
            print(issue)
            speak(issue)

        print("\nLLM Suggestion:")
        suggestion = ask_llm_for_suggestions(recent_reminder)
        print(suggestion)
        speak("Here are some suggestions to improve future reminders.")  # Optional
        speak(suggestion)  # 🗣️ Speak LLM advice aloud

        generate_report_json(recent_reminder, issues,suggestion)
        
    else:
        print("✅ All reminders are in order.")
        speak("All reminders are in order.")

if __name__ == "__main__":
    main()
