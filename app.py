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

# List of keywords related to mental health with their variations and weights
mental_health_keywords = {
    # Basic greetings and variations
    "hello": 1.2,
    "hi": 1.2,
    "hey": 1.2,
    "greetings": 1.2,
    "good morning": 1.2,
    "morning": 0.1,
    "good afternoon": 1.2,
    "afternoon": 0.1,
    "good evening": 1.2,
    "evening": 0.1,
    "good night": 1.2,
    "night": 0.1,
    "how are you": 1.2,
    "how do you do": 1.2,
    "what's up": 1.2,
    "wassup": 1.2,
    
    # General mental health terms
    "mental health": 1.2,
    "mental illness": 1.2,
    "mental wellness": 1.2,
    "mental wellbeing": 1.2,
    "mental support": 1.2,
    
    # Common conditions and their variations
    "low": 0.3,
    "down": 0.3,
    "feeling": 1.0,
    "hurts": 1.0,
    "hurting": 1.2,
    "hurtful": 1.2,
    "low mood": 1.2,
    "low energy": 1.2,
    "anxiety": 1.2,
    "anxious": 1.2,
    "anxiousness": 1.2,
    "depression": 1.2,
    "depressed": 1.2,
    "depressing": 1.2,
    "stress": 1.2,
    "stressed": 1.2,
    "stressing": 1.2,
    "stressful": 1.2,
    "trauma": 1.2,
    "traumatic": 1.2,
    "traumatized": 1.2,
    "bipolar": 1.2,
    "bipolarity": 1.2,
    "ptsd": 1.2,
    "post traumatic": 1.2,
    "ocd": 1.2,
    "obsessive": 1.2,
    "compulsive": 1.2,
    "adhd": 1.2,
    "attention deficit": 1.2,
    "panic": 1.2,
    "panicking": 1.2,
    "panicked": 1.2,
    "phobia": 1.2,
    "phobic": 1.2,
    "fear": 1.2,
    "feared": 1.2,
    "fearful": 1.2,
    "eating disorder": 1.2,
    "eating issues": 1.2,
    "addict": 1.2,
    "addicted": 1.2,
    "addiction": 1.2,
    "addictive": 1.2,
    
    # Symptoms and experiences with variations
    "mood": 1.2,
    "moody": 1.2,
    "moodiness": 1.2,
    "emotion": 1.2,
    "emotional": 1.2,
    "emotionally": 1.2,
    "burn": 1.2,
    "burned": 1.2,
    "burning": 1.2,
    "burnt out": 1.2,
    "burnout": 1.2,
    "insomnia": 1.2,
    "insomniac": 1.2,
    "sleep": 1.2,
    "sleeping": 1.2,
    "harm": 1.2,
    "harming": 1.2,
    "harmed": 1.2,
    "harmful": 1.2,
    "hurt": 1.2,
    "suicide": 0.3,
    "commit": 0.9,
    "suicidal": 0.3,
    "suicidality": 1.2,
    "lonely": 1.2,
    "loneliness": 1.2,
    "alone": 1.2,
    "isolate": 1.2,
    "isolated": 1.2,
    "isolation": 1.2,
    "grief": 1.2,
    "grieving": 1.2,
    "grieved": 1.2,
    "anger": 1.2,
    "angry": 1.2,
    "angered": 1.2,
    "fear": 1.2,
    "feared": 1.2,
    "fearful": 1.2,
    "fearing": 1.2,
    "worry": 1.2,
    "worried": 1.2,
    "worrying": 1.2,
    "worrisome": 1.2,
    "hopless": 1.2,
    "hoplessness": 1.2,
    
    # Treatment and support terms
    "therapy": 1.2,
    "therapist": 1.2,
    "therapeutic": 1.2,
    "counsel": 1.2,
    "counseling": 1.2,
    "counselor": 1.2,
    "psychiatry": 1.2,
    "psychiatrist": 1.2,
    "psychiatric": 1.2,
    "psychology": 1.2,
    "psychologist": 1.2,
    "psychological": 1.2,
    "medicate": 1.2,
    "medication": 1.2,
    "medicated": 1.2,
    "support": 1.2,
    "supporting": 1.2,
    "supported": 1.2,
    "self-care": 1.2,
    "caring": 1.2,
    "self care": 1.2,
    "mindful": 1.2,
    "mindfulness": 1.2,
    "mindfully": 1.2,
    "meditate": 1.2,
    "meditation": 1.2,
    "meditating": 1.2,
    
    # Emotional states and variations
    "sad": 1.2,
    "sadness": 1.2,
    "saddened": 1.2,
    "anxious": 1.2,
    "anxiety": 1.2,
    "anxiousness": 1.2,
    "depressed": 1.2,
    "depression": 1.2,
    "depressing": 1.2,
    "overwhelm": 1.2,
    "overwhelmed": 1.2,
    "overwhelming": 1.2,
    "stressed": 1.2,
    "stressful": 1.2,
    "stressing": 1.2,
    "tired": 1.2,
    "tiredness": 1.2,
    "tiring": 1.2,
    "exhaust": 1.2,
    "exhausted": 1.2,
    "exhausting": 1.2,
    "frustrate": 1.2,
    "frustrated": 1.2,
    "frustrating": 1.2,
    "confuse": 1.2,
    "confused": 1.2,
    "confusing": 1.2,
    "scared": 1.2,
    "scary": 1.2,
    "scaring": 1.2,
    "nervous": 1.2,
    "nervousness": 1.2,
    "nervously": 1.2,
    "worried": 1.2,
    "worrying": 1.2,
    "worrisome": 1.2,
    "upset": 1.2,
    "upsetting": 1.2,
    "upsetness": 1.2,
    "distress": 1.2,
    "distressed": 1.2,
    "distressing": 1.2,
    
    # Recovery and wellness variations
    "heal": 1.2,
    "healing": 1.2,
    "healed": 1.2,
    "recover": 1.2,
    "recovery": 1.2,
    "recovering": 1.2,
    "cope": 1.2,
    "coping": 1.2,
    "coped": 1.2,
    "resilient": 1.2,
    "resilience": 1.2,
    "resiliency": 1.2,
    "grow": 1.2,
    "growth": 1.2,
    "growing": 1.2,
    "well": 1.2,
    "wellness": 1.2,
    "wellbeing": 1.2,
    "help": 1.2,
    "helping": 1.2,
    "helped": 1.2,
    "helpful": 1.2,
    "mental fitness": 1.2,
    "emotional health": 1.2,
    "psychological health": 1.2,
    
    # Physical symptoms related to mental health
    "headache": 1.2,
    "headaches": 1.2,
    "head pain": 1.2,
    "migraine": 1.2,
    "migraines": 1.2,
    "migrainous": 1.2,
    "tension headache": 1.2,
    "cluster headache": 1.2,
    "throbbing": 1.2,
    "throbbing head": 1.2,
    "throbbing pain": 1.2,
    "pounding head": 1.2,
    "pounding headache": 1.2,
    "head pressure": 1.2,
    "having": 0.2,
    "pressure in head": 1.2,
    "head discomfort": 1.2,
    "head ache": 1.2,
    "depression": 1.2,
    "major depressive disorder": 1.2,
    "bipolar disorder": 1.2,
    "seasonal affective disorder": 1.2,
    "sad": 1.2,
    "cyclothymic disorder": 1.2,
    "generalized anxiety disorder": 1.2,
    "panic disorder": 1.2,
    "social anxiety disorder": 1.2,
    "obsessive-compulsive disorder": 1.2,
    "phobias": 1.2,
    "agoraphobia": 1.2,
    "specific phobias": 1.2,
    "schizophrenia": 1.2,
    "schizoaffective disorder": 1.2,
    "delusional disorder": 1.2,
    "anorexia nervosa": 1.2,
    "bulimia nervosa": 1.2,
    "binge-eating disorder": 1.2,
    "borderline personality disorder": 1.2,
    "antisocial personality disorder": 1.2,
    "narcissistic personality disorder": 1.2,
    "avoidant personality disorder": 1.2,
    "post-traumatic stress disorder": 1.2,
    "ptsd": 1.2,
    "acute stress disorder": 1.2,
    "adjustment disorder": 1.2,
    "autism spectrum disorder": 1.2,
    "asd": 1.2,
    "attention-deficit/hyperactivity disorder": 1.2,
    "adhd": 1.2,
    "intellectual disability": 1.2,
    "alcohol use disorder": 1.2,
    "drug addiction": 1.2,
    "substance-induced psychosis": 1.2,
    "dizzy": 1.0,
}  # Add this closing brace

def is_mental_health_related(prompt):
    prompt_lower = prompt.lower()
    score = 0.0
    matches = 0
    
    # Split prompt into words to avoid partial matches
    prompt_words = set(prompt_lower.split())
    
    for keyword, weight in mental_health_keywords.items():
        # For multi-word keywords
        if ' ' in keyword:
            if keyword in prompt_lower:
                score += weight
                matches += 1
        # For single word keywords
        elif keyword in prompt_words:  # Check exact word matches only
            score += weight
            matches += 1

    # Make the threshold more strict
    return score >= 1.2 or (matches >= 2 and score >= 1.5)

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

    # Check if prompt is empty
    if not prompt:
        return jsonify({"response": "Sorry, I didn't understand that."}), 400

    # Check for help command
    if prompt.lower().strip() == 'help':
        return jsonify({"response": "Sure, I can assist with mental health. What are you struggling with?"})

    # Check if mental health related
    if is_mental_health_related(prompt):
        try:
            ai_response = generate(prompt)
            return jsonify({"response": ai_response})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    # If not mental health related, return guidance message
    return jsonify({
        "response": "I'm here to support mental health discussions only. Please ask about mental wellbeing, stress, emotions, or similar topics."
    })

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
