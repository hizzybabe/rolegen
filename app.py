from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
import markdown2

load_dotenv()

app = Flask(__name__)

# Configure Gemini AI
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_prompt(role, responsibilities, tone, additional_info):
    prompt = f"""
    Create a detailed AI role prompt for a chatbot with the following specifications:
    Role: {role}
    Responsibilities: {responsibilities}
    Tone: {tone}
    Additional Information: {additional_info}
    
    Format the response as a complete prompt that starts with "You are a..." and includes
    clear instructions about the role's purpose, responsibilities, and behavior.
    """
    
    response = model.generate_content(prompt)
    return response.text

# Add this after configuring Gemini AI
def process_markdown(text):
    return markdown2.markdown(text)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    role = data.get('role')
    responsibilities = data.get('responsibilities')
    tone = data.get('tone')
    additional_info = data.get('additionalInfo')
    
    try:
        generated_prompt = generate_prompt(role, responsibilities, tone, additional_info)
        processed_prompt = process_markdown(generated_prompt)
        return jsonify({'prompt': processed_prompt})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
