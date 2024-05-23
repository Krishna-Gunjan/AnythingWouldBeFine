# access_stored_questions.py
from get_leetcode_questions import stored_questions, initialize_questions

# Initialize the questions (if not already done in main)
if not stored_questions:
    initialize_questions()

# Print the stored questions
for difficulty, questions in stored_questions.items():
    print(f"Questions for {difficulty.capitalize()} difficulty:")
    for question in questions:
        print(f"  Question: {question['question_name']}")
        print(f"  URL: {question['question_url']}")
    print()
