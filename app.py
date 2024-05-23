# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from get_leetcode_questions import stored_questions, initialize_questions
import random  # Add this import statement

app = Flask(__name__)
CORS(app, resources={r"/run-python": {"origins": "http://127.0.0.1:3000"}})

@app.route('/run-python', methods=['POST'])
def run_python():
    if not stored_questions:
        initialize_questions()
    
    data = request.get_json()
    button_id = data.get('id')
    difficulty_map = {'easy': 'easy', 'medium': 'medium', 'hard': 'hard'}
    
    try:
        difficulty = difficulty_map.get(button_id)
        if difficulty and difficulty in stored_questions and stored_questions[difficulty]:
            question = random.choice(stored_questions[difficulty])
            result = {
                'question_name': question['question_name'],
                'difficulty': question['difficulty'],
                'question_url': question['question_url'],
                'status': question['status']
            }
        else:
            result = 'Invalid button ID or no questions available for the selected difficulty'
    except Exception as e:
        result = str(e)
    
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
