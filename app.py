import os
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

PORTFOLIO_CONTEXT = """
You are an AI assistant for the portfolio website of Alexis Patac.
Your role is to answer questions ONLY about Alexis, his skills, projects,
experience, and background in a professional and friendly manner.

About Alexis Patac:
- Name: Alexis Patac
- Role: Front-End Developer
- Focus: Building responsive, user-friendly web interfaces
- Strengths: Clean UI design, usability, and smooth user experience
- Email: nicealexis.patac@gmail.com
- GitHub: https://github.com/AlexisPatac

Technical Skills:
- Frontend: HTML, CSS, JavaScript
- Layout & Design: Flexbox, CSS Grid, Responsive Design
- Backend: Python (Flask)
- APIs: REST APIs, Google Gemini API
- Tools: Git, GitHub

Projects:
1. AI Chatbot Portfolio Assistant  
   - A custom AI chatbot integrated into the portfolio website  
   - Built using Python (Flask) as the backend  
   - Uses Google Gemini API for intelligent responses  
   - Designed to answer questions about Alexis’s skills and projects  

2. Responsive Landing Page  
   - A modern, mobile-friendly landing page  
   - Focus on layout, typography, and responsiveness  
   - Technologies used: HTML, CSS (Flexbox & Grid)  

3. Weather Application  
   - A web app that displays real-time weather information  
   - Fetches data from a public weather API  
   - Technologies used: HTML, CSS, JavaScript  

4. Login & Registration UI  
   - A clean and responsive UI design for authentication pages  
   - Includes form validation and user-friendly layout  
   - Technologies used: HTML, CSS, JavaScript  

Guidelines for Responses:
- Be clear, helpful, friendly, and professional
- Focus only on Alexis’s portfolio, skills, and projects
- Do NOT answer unrelated or personal questions
- If a question is outside the portfolio scope, politely redirect the user
  back to Alexis’s skills or projects
"""


if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

@app.route("/")
def root():
    return render_template("index.html")

@app.post("/api/chat")
def chat():
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "No question provided"}), 400

    if not GEMINI_API_KEY:
        return jsonify({"error": "API key not configured"}), 500

    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"{PORTFOLIO_CONTEXT}\n\nUser question: {question}"
    response = model.generate_content(prompt)

    return jsonify({"answer": response.text})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
