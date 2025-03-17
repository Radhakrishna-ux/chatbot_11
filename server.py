import os
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='frontend', static_url_path='')

# Define intents and corresponding phrases (all in lowercase for matching)
intents = {
    "hello": ["hii", "what's up", "hello", "hi", "hey"],
    "courses": ["what are the courses", "give me courses"],
    "fee": ["what's the fee", "fee structure", "my next payment"],
    "syllabus": ["what's the syllabus for my course", "where can i download my syllabus"],
    "exam timetable": ["when is exam", "exam", "exam schedule"],
    "holidays": ["next holidays"],
    "results": ["topper's list", "university topper"],
    "clubs": ["what clubs available", "clubs detail", "how many clubs"],
    "library timings": ["when is library open", "library timing", "what are library hours", "library open time", "until what time is the library open"],
    "canteen hour": ["canteen timing", "brakfast time", "lunch", "dinner", "when does the canteen open", "what time is breakfast in the canteen", "when is lunch served", "dinner time in the canteen", "canteen open hours"],
    "hostel facilities": ["where can i stay", "hostel", "hostel details"],
}

# Define responses for each intent (for "canteen hour" we use a different key in responses)
responses = {
    "hello": "Hello! How can I assist you with your college related work today?",
    "courses": "The college offers BBA, BCA, BA, PSC. See details on the college website.",
    "fee": "💰The fee structure depends on the course. To know about installments or payment deadlines, check here: <a href='https://www.imperial.edu.in/fee-details' target='_blank'>Fee Details</a>",
    "syllabus": "📚You can find the syllabus for your course at <a href='https://www.imperial.edu.in/downloads/Syllabus#programme-syllabus' target='_blank'>Download Syllabus</a>",
    "exam timetable": "The exam schedule 🗓️ will be published by the university. Keep an eye on the noticeboard.",
    "holidays": "For holidays, you can check the academic calendar in your Sahaj app.",
    "results": "Want to know who aced it 🏆? For the latest ranking, visit <a href='https://www.imperial.edu.in/academic-achievements' target='_blank'>Academic Achievements</a>.",
    "clubs": "Clubs run the show! 🎤 Cultural, sports, social activities and more—find your place! Check details here: <a href='https://www.imperial.edu.in/campus-life/clubs' target='_blank'>Clubs Info</a>",
    "library timings": "📖 Books, Peace, and Knowledge! Visit the library from 10 AM to 4 PM.",
    "Canteen hours": "🍕 Hungry! Breakfast: 8:30 AM to 8:45 AM, Lunch: 1:15 PM to 2:00 PM, Dinner: 7:30 PM to 8:00 PM.",
    "hostel facilities": "🏡 Hostel life is fun! The details are available with the warden.",
    "unknown": "I'm sorry, I don't understand. Can you rephrase it?"
}

def get_response(user_input):
    user_input_lower = user_input.lower()
    # Loop through each intent (except fallback)
    for key, phrases in intents.items():
        for phrase in phrases:
            if phrase in user_input_lower:
                # For "canteen hour", use response key "Canteen hours"
                response_key = "Canteen hours" if key == "canteen hour" else key
                return responses.get(response_key, responses["unknown"])
    return responses["unknown"]

# API endpoint for chat: receives a JSON { "message": ... } and returns a JSON response
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    bot_reply = get_response(user_message)
    return jsonify({"bot_response": bot_reply})

# Serve frontend static files
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
