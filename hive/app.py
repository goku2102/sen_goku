from flask import Flask, request, jsonify
from flask import Flask, render_template
from flask_cors import CORS
import time
import random
import logging
from datetime import datetime


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Ensure index.html is inside the 'templates/' folder

if __name__ == "__main__":
    app.run(debug=True)
CORS(app) # Enable CORS for all origins by default

# Configure logging
logging.basicConfig(level=logging.INFO,
format='[%(asctime)s] %(levelname)s: %(message)s',
datefmt='%Y-%m-%d %H:%M:%S')

# Predefined keywords & responses
KEYWORD_RESPONSES = [
{
"keys": ['hi', 'hello', 'hey'],
"responses": [
"Hi there! I'm Hive AI, here to help you. 😊",
"Hello! How can I assist you today?",
"Hey! What's on your mind?"
]
},
{
"keys": ['how are you', 'how is it going'],
"responses": [
"I'm just a bunch of code, but I'm doing great!",
"Doing well, thanks for asking! How about you?",
"I appreciate you asking, I'm ready to chat!"
]
},
{
"keys": ['good morning', 'morning'],
"responses": [
"Good morning! Hope your day is off to a great start! ☀️",
"Morning! Ready to seize the day?",
"Hello! Wishing you a productive day ahead!"
]
},
{
"keys": ['good night', 'night'],
"responses": [
"Good night! Sleep well and sweet dreams!",
"Night! Rest up for tomorrow!",
"Wishing you a peaceful night."
]
},
{
"keys": ['thank you', 'thanks'],
"responses": [
"You're very welcome! 😊",
"No problem at all!",
"Glad I could help!"
]
},
{
"keys": ['bye', 'goodbye', 'see you'],
"responses": [
"Goodbye! Talk to you soon!",
"See you later! Have a great one!",
"Bye! Stay safe and happy!"
]
},
{
"keys": ['what can you do', 'features', 'help'],
"responses": [
"I can chat and keep you company! Try typing greetings or whatever is on your mind.",
"I'm a fun chat AI. Let's talk!",
"I have new cool features like message reactions, stickers, dark mode and more!"
]
}
]

GENERIC_RESPONSES = [
"That's interesting! Tell me more.",
"I'm here to listen. What else can you say?",
"Could you elaborate on that?",
"I'm learning more each day. Thanks for chatting!",
"Hmm, I don't fully understand that yet, but I’m eager to learn."
]

FEATURES_LIST = [
"Real-time AI chat replies",
"Message reactions (emoji)",
"Message editing support",
"Favorite/star important messages",
"Chat export functionality",
"Dark mode support",
"Sticker messages",
"Sound effects toggling",
"Background customization",
"Auto-scroll toggle for chat"
]

def generate_ai_reply(user_input):
    normalized = user_input.lower().strip()
    
    for entry in KEYWORD_RESPONSES:
        for key in entry['keys']:
            # Perform some operations inside the loop
            print(key)  # Example action, replace this with your intended logic
            
            if key in normalized:
                response = random.choice(entry['responses'])
                return response
    
    # Return generic fallback if no keyword matches
    return random.choice(GENERIC_RESPONSES)
@app.route('/')
def health_check():
    return "Hive AI Chat Backend is alive and running!"
@app.route('/features', methods=['GET'])
def get_features():
    """Return the list of features supported by the chat app."""
    
    return jsonify({"features": FEATURES_LIST})
@app.route('/message', methods=['POST'])
def message():
    """
    Receive user message, generate AI reply with simulated processing delay, return reply.
    Expects: JSON {"message": "<user message>"}
    Returns: JSON {"reply": "<AI reply>"}
    """
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Request JSON must contain 'message' field"}), 400

    user_message = data['message']
    if not isinstance(user_message, str) or not user_message.strip():
        return jsonify({"error": "'message' must be a non-empty string"}), 400

    logging.info(f"Received message: {user_message}")

    # Simulate thinking delay proportional to message length (min 0.8s, max 3.5s) + random jitter
    base_delay = min(max(len(user_message) * 0.06, 0.8), 3.5)
    delay = base_delay + random.uniform(0, 0.5)
    time.sleep(delay)

    reply_text = generate_ai_reply(user_message)

    logging.info(f"Reply generated: {reply_text}")

    response = {
        "reply": reply_text,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)