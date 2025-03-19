import os
from flask import Flask, request, jsonify, send_from_directory
# from flask_cors import CORS 

app = Flask(__name__, static_folder='frontend', static_url_path='')
# CORS(app)

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
    "admission process":["how to apply", "admission process","how to take admission","admission form details"],
    "scholarship":["scholarship details","available scolarships","how to apply for scholarship",],
    "attendance":["attendence rules","minimum attendence required","attendence criteria"],
    "faculty contact":["how to contact faculty","teacher contact details","faculty email id"],
    "transport":["bus service","college transport timing","college bus fee"],
    "lost and found":["lost items","how to report lost item","found items help"],
    "medical facilities":["medical help","first aid in college","college hospital"],
    "labs":["lab timing","computer lab access","when labs are open"],
    "alumni":["alumi network","famous alumni"],
    "placement":["placement record","placement oppurtunities","company visiting campus"]
    
    }

# Define responses for each intent (for "canteen hour" we use a different key in responses)
responses = {
    "hello": "Hello!👋 😇How can I assist you with your college related work today?",
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
    "admission process":"🎓Ready to join us? We have multiple graduation courses available and the eligibility for those is 12th pass in any stream. Recently we have also added 12th in arts and science, for more details please contact 📞+91 89840 79266 📧info@imperial.edu.in ",
     "scholarship":"🧧Good news!!We have scholarships deserving students. We offer scholarships for meritorious students who are university rank holders🏆 and for those who have won prizes in university-level sports competitions⚽🥇. Check your eligibility and apply in account section. Keep striving for excellence!🎓✨",
     "attendance":"📆Don't forget! A minimum of 75% attendance is required to sit for mid-sem as well as final exams.Stay regular and punctual!",
     "faculty contact":"👩‍🏫Need to reach teacher? You can contact HOD's through their emails given below-",
     "transport":"🚌Need a ride? To access college transport and about fees contact 📞+91 89840 79266",
     "lost and found":"🔎 Lost something? No worries! Report it at the admin office or check with security.",
     "medical facilities":"🏥Health first! First aid are available on campus but for severe cases contact the hostel incharge.",
     "labs":"💻Lab hours are from 9:00 AM to 4:00 PM. It's available for different classes at different periods - check your schedule!⌚if you need to use the lab for extra work, just take permission from the lab teacher 👨‍🏫✨",
     "alumni":"🤝We have many wonderful alumini! You can know about their inspiring stiries in icons of imperial.Be inspired and dream big🌟 ",
     "placement":"🏢⭐Excited about placement? Explore our placement records and upcoming drives through the Training and placement committee. Your dream job awaits!",
     
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
