from flask import Flask, request, jsonify
import os
import google.generativeai as genai
from flask_cors import CORS  # Import CORS

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes (or you can enable it selectively)
CORS(app)

# Configure Google Generative AI API key
os.environ["API_KEY_NAME"] = "AIzaSyDVxnlcZ1En8IjgW7FEPisL6lOaNJQ3dHg"  # Replace with your actual API key
genai.configure(api_key=os.environ["API_KEY_NAME"])

# Set up the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 512,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="You are a physics chatbot who will help students with their questions.",
)

# Create a chat session
chat_session = model.start_chat()

# Define the API endpoint
@app.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.json
        user_input = data.get("question", "")

        if not user_input.strip():
            return jsonify({"response": "Please enter a valid question."}), 400

        # Get response from AI model
        response = chat_session.send_message(user_input)
        return jsonify({"response": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask server
if __name__ == '__main__':
    app.run(debug=True)
