from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import os
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Load environment variables from .env file
load_dotenv()
# Initialize Flask app
app = Flask(__name__)
CORS(app)
load_dotenv(dotenv_path="E:/MYChatbot/.env")
print("Loaded API KEY:", os.getenv("GOOGLE_API_KEY"))
api_key = os.getenv("GOOGLE_API_KEY")
# Configure Google AI model

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

# List of keywords related to mental health with their variations
mental_health_keywords = [
    # Basic greetings and variations
    "hello", "hi", "hey", "greetings",
    "good morning", "morning", "good afternoon", "afternoon",
    "good evening", "evening", "good night", "night",
    "how are you", "how do you do", "what's up", "wassup",
    
    # General mental health terms
    "mental health", "mental illness", "mental wellness", "mental wellbeing", "mental support",
    
    # Common conditions and their variations
    "low", "down", "low mood", "low energy",
    "anxiety", "anxious", "anxiousness",
    "depression", "depressed", "depressing",
    "stress", "stressed", "stressing", "stressful",
    "trauma", "traumatic", "traumatized",
    "bipolar", "bipolarity",
    "ptsd", "post traumatic",
    "ocd", "obsessive", "compulsive",
    "adhd", "attention deficit",
    "panic", "panicking", "panicked",
    "phobia", "phobic", "fear", "feared", "fearful",
    "eating disorder", "eating issues",
    "addict", "addicted", "addiction", "addictive",
    
    # Symptoms and experiences with variations
    "mood", "moody", "moodiness",
    "emotion", "emotional", "emotionally",
    "burn", "burned", "burning", "burnt out", "burnout",
    "insomnia", "insomniac", "sleep", "sleeping",
    "harm", "harming", "harmed", "harmful", "hurt",
    "suicide", "suicidal", "suicidality",
    "lonely", "loneliness", "alone",
    "isolate", "isolated", "isolation",
    "grief", "grieving", "grieved",
    "anger", "angry", "angered",
    "fear", "feared", "fearful", "fearing",
    "worry", "worried", "worrying", "worrisome",
    "hopeless", "hopelessness",
    
    # Treatment and support terms
    "therapy", "therapist", "therapeutic",
    "counsel", "counseling", "counselor",
    "psychiatry", "psychiatrist", "psychiatric",
    "psychology", "psychologist", "psychological",
    "medicate", "medication", "medicated",
    "support", "supporting", "supported",
    "self-care", "caring", "self care",
    "mindful", "mindfulness", "mindfully",
    "meditate", "meditation", "meditating",
    
    # Emotional states and variations
    "sad", "sadness", "saddened",
    "anxious", "anxiety", "anxiousness",
    "depressed", "depression", "depressing",
    "overwhelm", "overwhelmed", "overwhelming",
    "stressed", "stressful", "stressing",
    "tired", "tiredness", "tiring",
    "exhaust", "exhausted", "exhausting",
    "frustrate", "frustrated", "frustrating",
    "confuse", "confused", "confusing",
    "scared", "scary", "scaring",
    "nervous", "nervousness", "nervously",
    "worried", "worrying", "worrisome",
    "upset", "upsetting", "upsetness",
    "distress", "distressed", "distressing",
    
    # Recovery and wellness variations
    "heal", "healing", "healed",
    "recover", "recovery", "recovering",
    "cope", "coping", "coped",
    "resilient", "resilience", "resiliency",
    "grow", "growth", "growing",
    "well", "wellness", "wellbeing",
    "help", "helping", "helped", "helpful",
    "mental fitness", "emotional health", "psychological health",
    
    # Physical symptoms related to mental health
    "headache", "headaches", "head pain",
    "migraine", "migraines", "migrainous",
    "tension headache", "cluster headache",
    "throbbing", "throbbing head", "throbbing pain",
    "pounding head", "pounding headache",
    "head pressure", "pressure in head",
    "head discomfort", "head ache",
    "depression", "major depressive disorder",
    "bipolar disorder", "seasonal affective disorder", "sad",
    "cyclothymic disorder",
    "generalized anxiety disorder", "gad",
    "panic disorder",
    "social anxiety disorder",
    "obsessive-compulsive disorder", "ocd",
    "phobias", "agoraphobia", "specific phobias",
    "schizophrenia",
    "schizoaffective disorder",
    "delusional disorder",
    "anorexia nervosa",
    "bulimia nervosa",
    "binge-eating disorder",
    "borderline personality disorder",
    "antisocial personality disorder",
    "narcissistic personality disorder",
    "avoidant personality disorder",
    "post-traumatic stress disorder", "ptsd",
    "acute stress disorder",
    "adjustment disorder",
    "autism spectrum disorder", "asd",
    "attention-deficit/hyperactivity disorder", "adhd",
    "intellectual disability",
    "alcohol use disorder",
    "drug addiction",
    "substance-induced psychosis"
]

# Check if the prompt is related to mental health
def is_mental_health_related(prompt):
    prompt_lower = prompt.lower()
    words = prompt_lower.split()
    
    # Check for exact word matches and word boundaries
    for keyword in mental_health_keywords:
        # For multi-word keywords
        if ' ' in keyword:
            if keyword in prompt_lower:
                return True
        # For single-word keywords
        else:
            for word in words:
                if keyword == word or \
                   word.startswith(keyword + '-') or \
                   word.endswith('-' + keyword) or \
                   keyword == word.rstrip('.,!?;:'):
                    return True
    return False

# Generate AI response
def generate(prompt):
    try:
        response = model.generate_content(prompt)
        if response.parts:
            return response.text
        return "I apologize, but I couldn't generate a response. Please try again."
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        raise Exception("Failed to generate AI response. Please try again later.")


# Define the route for getting AI response
@app.route('/getAIResponse', methods=['GET', 'POST'])
def get_ai_response():
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data received"}), 400
        prompt = data.get('prompt', '')
    else:
        return jsonify({"error": "Please use POST method with a JSON payload containing 'prompt'"}), 405

    if prompt:
        if prompt.lower().strip() == 'help':
            return jsonify({"response": "Sure, I can assist with mental health. What are you struggling with?"})
    if is_mental_health_related(prompt):
        try:
            ai_response = generate(prompt)
            return jsonify({"response": ai_response})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return jsonify({
            "response": "I'm here to support mental health discussions only. Please ask about mental wellbeing, stress, emotions, or similar topics."
        })
    return jsonify({"response": "Sorry, I didn't understand that."}), 400

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == "__main__":
    app.run(debug=True)
debug_mode = os.environ.get("DEBUG", "False").lower() == "true"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=debug_mode)
