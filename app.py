import os
from flask import Flask, request, render_template, send_from_directory, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__, static_folder="templates", static_url_path="/static")
CORS(app)  # Enable CORS for AJAX requests

# Configure Gemini API key via environment variable
# Example:
#   $env:GEMINI_API_KEY="your-api-key-here"   (Windows PowerShell)
#   set GEMINI_API_KEY=your-api-key-here      (Windows CMD)
#   export GEMINI_API_KEY=your-api-key-here   (macOS/Linux)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCDmSARcdDhETbH_0cMurPasrJHgD3ujqU")

# Portfolio context for the AI assistant
PORTFOLIO_CONTEXT = """
You are an AI assistant for Alexis Patac's portfolio website. 
Here's some information about Alexis:

- Name: Alexis Patac
- Role: Front-End Developer
- Specialization: Building responsive, user-friendly web interfaces with clean design and smooth user experiences
- Email: nicealexis.patac@gmail.com
- GitHub: github.com/AlexisPatac

Projects:
1. AI Chatbot - A custom chatbot integrated into the portfolio using a Python backend and Google's Gemini API
2. Responsive Landing Page - A modern, mobile-friendly landing page focusing on layout, typography, and user experience (Technologies: HTML, CSS - Flexbox/Grid)
3. Weather App - A weather application that fetches real-time weather data based on user input (Technologies: HTML, CSS, JavaScript, Public API)
4. Login & Registration UI - A front-end design for login and registration system with form validation and responsive layout (Technologies: HTML, CSS, JavaScript)

When answering questions, be helpful, friendly, and professional. Focus on Alexis's skills, projects, and experience. If asked about something not in the context, politely redirect to the portfolio information.
"""

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


@app.route("/")
def root():
    """Serve the portfolio page."""
    return render_template("index.html")


@app.post("/api/chat")
def chat():
    """Receive a question and return Gemini's response."""
    data = request.get_json()
    question = data.get("question", "").strip() if data else ""
    
    if not question:
        return jsonify({"error": "No question provided."}), 400

    if not GEMINI_API_KEY:
        return jsonify({
            "error": "GEMINI_API_KEY is not configured. Set it as an environment variable before running the app."
        }), 500

    try:
        # List available models to find one that works
        available_model_name = None
        try:
            models = genai.list_models()
            # Look for a model that supports generateContent
            for m in models:
                if 'generateContent' in m.supported_generation_methods:
                    # Extract just the model name (remove 'models/' prefix if present)
                    model_name = m.name.split('/')[-1] if '/' in m.name else m.name
                    # Prefer gemini models
                    if 'gemini' in model_name.lower():
                        available_model_name = model_name
                        break
            if not available_model_name and models:
                # Use the first available model's name
                first_model = models[0]
                available_model_name = first_model.name.split('/')[-1] if '/' in first_model.name else first_model.name
        except Exception as list_error:
            print(f"Error listing models: {list_error}")
            # Fallback to trying common model names
            available_model_name = None
        
        # Try to initialize the model - use available_model_name or try common names
        model = None
        model_names_to_try = []
        if available_model_name:
            model_names_to_try.append(available_model_name)
        # Add fallback model names
        model_names_to_try.extend(['gemini-pro', 'gemini-1.5-pro', 'gemini-1.5-flash'])
        
        for model_name in model_names_to_try:
            if not model_name:
                continue
            try:
                model = genai.GenerativeModel(model_name)
                # If we got here, the model was created successfully
                break
            except Exception as model_error:
                print(f"Model {model_name} failed: {model_error}")
                model = None
                continue
        
        if model is None:
            raise Exception("No available Gemini model found. Please check your API key and model access.")
        
        # Create the prompt with context
        prompt = f"{PORTFOLIO_CONTEXT}\n\nUser question: {question}\n\nAssistant response:"
        
        # Generate response
        response = model.generate_content(prompt)
        answer = response.text.strip()
        
        return jsonify({"answer": answer})
    
    except Exception as exc:
        print(f"Error calling Gemini: {exc}")
        return jsonify({
            "error": f"Sorry, there was a problem contacting the AI service: {str(exc)}"
        }), 500


if __name__ == "__main__":
  # Run the Flask dev server
  # In production, use: gunicorn app:app
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port, debug=True)


