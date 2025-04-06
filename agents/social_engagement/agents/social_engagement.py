# import sys
# import pandas as pd
# from datetime import datetime, timedelta
# import ollama
# import pyttsx3
# import json
# import os

# # Initialize TTS engine
# tts_engine = pyttsx3.init()
# sys.stdout.reconfigure(encoding='utf-8')

# def speak(text):
#     tts_engine.say(text)
#     tts_engine.runAndWait()

# def load_data():
#     health_path = r"C:/Users/hp/OneDrive/Desktop/ollama/agents/health_monitor/data/cleaned_health_vitals.csv"
#     routine_path = r"C:/Users/hp/OneDrive/Desktop/ollama/agents/daily_routine/data/cleaned_reminders.csv"
#     safety_path = r"C:/Users/hp/OneDrive/Desktop/ollama/agents/safety_monitoring/data/cleaned_safety_monitoring.csv"

#     health_df = pd.read_csv(health_path)
#     routine_df = pd.read_csv(routine_path)
#     safety_df = pd.read_csv(safety_path)

#     # Parse date columns properly
#     health_df["Timestamp"] = pd.to_datetime(health_df["Timestamp"], errors="coerce")
#     routine_df["Timestamp"] = pd.to_datetime(routine_df["Timestamp"], errors="coerce")
#     routine_df["Scheduled Time"] = pd.to_datetime(routine_df["Scheduled Time"], errors="coerce")
#     safety_df["Timestamp"] = pd.to_datetime(safety_df["Timestamp"], errors="coerce")

#     # Drop rows with invalid/missing datetimes
#     health_df.dropna(subset=["Timestamp"], inplace=True)
#     routine_df.dropna(subset=["Timestamp", "Scheduled Time"], inplace=True)
#     safety_df.dropna(subset=["Timestamp"], inplace=True)

#     return health_df, routine_df, safety_df

# def detect_social_disengagement(health_df, routine_df, safety_df):
#     now = datetime.now()
#     one_day_ago = now - timedelta(days=1)

#     inactivity = {}

#     # 1. Health data gap
#     recent_health = health_df[health_df["Timestamp"] >= one_day_ago]
#     if recent_health.empty:
#         inactivity["Health Monitoring"] = "No health data in the last 24 hours."

#     # 2. Reminders not acknowledged
#     recent_reminders = routine_df[routine_df["Scheduled Time"] >= one_day_ago]
#     if not recent_reminders.empty:
#         unacknowledged = recent_reminders[recent_reminders["Acknowledged (Yes/No)"] == 0]
#         if len(unacknowledged) > 0:
#             inactivity["Daily Routine"] = f"{len(unacknowledged)} reminders were not acknowledged today."

#     # 3. Safety sensor activity
#     recent_safety = safety_df[safety_df["Timestamp"] >= one_day_ago]
#     if recent_safety.empty:
#         inactivity["Safety Monitoring"] = "No safety sensor activity in the last 24 hours."

#     return inactivity

# def ask_llm_for_social_suggestions(inactivity_issues):
#     prompt = f"""
# You are a compassionate elderly care assistant. The following inactivity patterns have been observed today:

# {chr(10).join([f"- {k}: {v}" for k, v in inactivity_issues.items()])}

# Based on these, suggest light, friendly, and engaging social or mental activities (e.g., call a loved one, play a game, short walk, etc.) tailored for an elderly user. Keep the tone uplifting.
# """
#     response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
#     return response['message']['content']

# def save_report_json(inactivity, suggestions):
#     report = {
#         "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         "issues_detected": inactivity,
#         "llm_suggestions": suggestions
#     }

#     output_path = r"C:/Users/hp/OneDrive/Desktop/ollama/agents/social_engagement/social_report.json"
#     os.makedirs(os.path.dirname(output_path), exist_ok=True)

#     with open(output_path, "w", encoding="utf-8") as f:
#         json.dump(report, f, indent=4, ensure_ascii=False)

#     print(f"\n📁 Report saved to {output_path}")

# def main():
#     print("🤝 Social Engagement Agent is running...\n")

#     health_df, routine_df, safety_df = load_data()
#     inactivity = detect_social_disengagement(health_df, routine_df, safety_df)

#     if inactivity:
#         print("⚠️ Inactivity Patterns Detected:")
#         for k, v in inactivity.items():
#             print(f"- {k}: {v}")
#             speak(v)

#         print("\n🤖 LLM Suggestions:")
#         suggestions = ask_llm_for_social_suggestions(inactivity)
#         print(suggestions)
#         speak("Here are some ideas to keep engaged.")
#         speak(suggestions)

#         save_report_json(inactivity, suggestions)
#     else:
#         print("✅ No signs of social disengagement detected.")
#         speak("You're doing great today. Keep it up!")

# if __name__ == "__main__":
#     main()



import sys
import pandas as pd
from datetime import datetime, timedelta
import ollama
import pyttsx3
import json
import os

# Initialize TTS engine
tts_engine = pyttsx3.init()
sys.stdout.reconfigure(encoding='utf-8')

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def load_data():
    health_path = r"C:/Users/hp/OneDrive/Desktop/ollama/agents/health_monitor/data/cleaned_health_vitals.csv"
    routine_path = r"C:/Users/hp/OneDrive/Desktop/ollama/agents/daily_routine/data/cleaned_reminders.csv"
    safety_path = r"C:/Users/hp/OneDrive/Desktop/ollama/agents/safety_monitoring/data/cleaned_safety_monitoring.csv"

    health_df = pd.read_csv(health_path)
    routine_df = pd.read_csv(routine_path)
    safety_df = pd.read_csv(safety_path)

    # Parse date columns properly
    health_df["Timestamp"] = pd.to_datetime(health_df["Timestamp"], errors="coerce")
    routine_df["Timestamp"] = pd.to_datetime(routine_df["Timestamp"], errors="coerce")
    routine_df["Scheduled Time"] = pd.to_datetime(routine_df["Scheduled Time"], errors="coerce")
    safety_df["Timestamp"] = pd.to_datetime(safety_df["Timestamp"], errors="coerce")

    # Drop rows with invalid/missing datetimes
    health_df.dropna(subset=["Timestamp"], inplace=True)
    routine_df.dropna(subset=["Timestamp", "Scheduled Time"], inplace=True)
    safety_df.dropna(subset=["Timestamp"], inplace=True)

    return health_df, routine_df, safety_df

def detect_social_disengagement(health_df, routine_df, safety_df):
    now = datetime.now()
    one_day_ago = now - timedelta(days=1)

    inactivity = {}

    # 1. Health data gap
    recent_health = health_df[health_df["Timestamp"] >= one_day_ago]
    if recent_health.empty:
        inactivity["Health Monitoring"] = "No health data in the last 24 hours."

    # 2. Reminders not acknowledged
    recent_reminders = routine_df[routine_df["Scheduled Time"] >= one_day_ago]
    if not recent_reminders.empty:
        unacknowledged = recent_reminders[recent_reminders["Acknowledged (Yes/No)"] == 0]
        if len(unacknowledged) > 0:
            inactivity["Daily Routine"] = f"{len(unacknowledged)} reminders were not acknowledged today."

    # 3. Safety sensor activity
    recent_safety = safety_df[safety_df["Timestamp"] >= one_day_ago]
    if recent_safety.empty:
        inactivity["Safety Monitoring"] = "No safety sensor activity in the last 24 hours."

    return inactivity

def ask_llm_for_social_suggestions(inactivity_issues):
    prompt = f"""
You are a compassionate elderly care assistant. The following inactivity patterns have been observed today:

{chr(10).join([f"- {k}: {v}" for k, v in inactivity_issues.items()])}

Based on these, suggest light, friendly, and engaging social or mental activities (e.g., call a loved one, play a game, short walk, etc.) tailored for an elderly user. Keep the tone uplifting.
"""
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

def extract_latest_user_info(health_df, routine_df, safety_df):
    latest_health = health_df.sort_values("Timestamp", ascending=False)
    latest_routine = routine_df.sort_values("Timestamp", ascending=False)
    latest_safety = safety_df.sort_values("Timestamp", ascending=False)

    latest_user = None
    latest_timestamp = None

    for df in [latest_health, latest_routine, latest_safety]:
        if not df.empty:
            user_col = next((col for col in df.columns if "ID" in col), None)
            if user_col:
                latest_row = df.iloc[0]
                timestamp = latest_row["Timestamp"]
                if not latest_timestamp or timestamp > latest_timestamp:
                    latest_user = latest_row[user_col]
                    latest_timestamp = timestamp

    return latest_user, latest_timestamp.strftime("%Y-%m-%d %H:%M:%S") if latest_timestamp else None

def save_report_json(inactivity, suggestions, user_id, timestamp):
    report_entry = {
        "user_id": user_id,
        "timestamp": timestamp,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "issues_detected": inactivity,
        "llm_suggestions": suggestions
    }

    output_path = r"C:/Users/hp/OneDrive/Desktop/ollama/agents/social_engagement/social_report.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Check if file exists and load it
    if os.path.exists(output_path):
        with open(output_path, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    else:
        existing_data = {"entries": []}

    existing_data["entries"].append(report_entry)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)

    print(f"\n📁 Report saved to {output_path}")

def main():
    print("🤝 Social Engagement Agent is running...\n")

    health_df, routine_df, safety_df = load_data()
    inactivity = detect_social_disengagement(health_df, routine_df, safety_df)

    user_id, timestamp = extract_latest_user_info(health_df, routine_df, safety_df)

    if inactivity:
        print("⚠️ Inactivity Patterns Detected:")
        for k, v in inactivity.items():
            print(f"- {k}: {v}")
            speak(v)

        print("\n🤖 LLM Suggestions:")
        suggestions = ask_llm_for_social_suggestions(inactivity)
        print(suggestions)
        speak("Here are some ideas to keep engaged.")
        speak(suggestions)

        save_report_json(inactivity, suggestions, user_id, timestamp)
    else:
        print("✅ No signs of social disengagement detected.")
        speak("You're doing great today. Keep it up!")

if __name__ == "__main__":
    main()
