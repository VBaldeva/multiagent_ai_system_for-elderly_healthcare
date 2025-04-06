from flask import Flask, render_template, request, jsonify
import json
import ollama

app = Flask(__name__)

# Load all reports once
def load_json(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}

health_data = load_json("C:/Users/hp/OneDrive/Desktop/ollama/agents/health_monitor/health_report.json")
safety_data = load_json("C:/Users/hp/OneDrive/Desktop/ollama/agents/safety_monitoring/safety_report.json")
routine_data = load_json("C:/Users/hp/OneDrive/Desktop/ollama/agents/daily_routine/daily_report.json")
social_data = load_json("C:/Users/hp/OneDrive/Desktop/ollama/agents/social_engagement/social_report.json")

@app.route('/')
def dashboard():
    return render_template("dashboard.html",
                           health=health_data,
                           safety=safety_data,
                           routine=routine_data,
                           social=social_data)

@app.route('/chatbot')
def chatbot_page():
    return render_template("chatbot.html")

@app.route('/chatbot', methods=['POST'])
def chatbot_reply():
    user_message = request.json.get('message', '')
    print("Received user message:", user_message)

    if not user_message:
        return jsonify({'reply': 'Please ask a valid question.'})

    try:
        
        report_context = f"""
        You are a helpful assistant who answers based on elderly care reports.

        Health Report: {json.dumps(health_data)}
        Safety Report: {json.dumps(safety_data)}
        Daily Routine Report: {json.dumps(routine_data)}
        Social Engagement Report: {json.dumps(social_data)}
        """
        print("DEBUG: Entered try block")
        response = ollama.chat(model='mistral', messages=[
            {"role": "system", "content": report_context},
            {"role": "user", "content": user_message}
        ])
        
        reply=response['messages']['content']
        print("Ollama Response:", response)
        return jsonify({'reply': reply})

    except Exception as e:
        print("Error from Ollama:", e)
        return jsonify({'reply': f"Error: {str(e)}"})

@app.route('/report/<report_type>')
def get_report(report_type):
    path_map = {
        'health': r'C:/Users/hp/OneDrive/Desktop/ollama/agents/health_monitor/health_report.json',
        'safety': r'C:/Users/hp/OneDrive/Desktop/ollama/agents/safety_monitoring/safety_report.json',
        'routine': r'C:/Users/hp/OneDrive/Desktop/ollama/agents/daily_routine/daily_report.json',
        'social': r'C:/Users/hp/OneDrive/Desktop/ollama/agents/social_engagement/social_report.json',
    }
    file_path = path_map.get(report_type)
    if file_path:
        return jsonify(load_json(file_path))
    return jsonify({"error": "Invalid report type"}), 404


if __name__ == '__main__':
    app.run(debug=True)
