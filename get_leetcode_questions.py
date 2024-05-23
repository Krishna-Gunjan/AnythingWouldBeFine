# get_leetcode_questions.py
import os
import random
import sys
import leetcode
from leetcode.api_client import ApiClient
from leetcode.configuration import Configuration
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve tokens from environment variables
csrf_token = os.getenv("LEETCODE_CSRF_TOKEN")
session_token = os.getenv("LEETCODE_SESSION_TOKEN")

# Set up the configuration
configuration = Configuration()
configuration.api_key["x-csrftoken"] = csrf_token
configuration.api_key["LEETCODE_SESSION"] = session_token
configuration.api_key_prefix["x-csrftoken"] = "csrftoken"

api_instance = leetcode.DefaultApi(ApiClient(configuration))

# Global variable to store questions
stored_questions = {}

def fetch_problem_list():
    """
    Fetch the list of problems and their statuses.
    """
    return api_instance.api_problems_topic_get(topic="algorithms")

def filter_unsolved_nonpremium(problems):
    """
    Filter out premium and already solved questions and group by difficulty.
    """
    unsolved_nonpremium_easy = [
        pair for pair in problems.stat_status_pairs
        if pair.status != "ac" and not pair.paid_only and pair.difficulty.level == 1
    ]

    unsolved_nonpremium_medium = [
        pair for pair in problems.stat_status_pairs
        if pair.status != "ac" and not pair.paid_only and pair.difficulty.level == 2
    ]

    unsolved_nonpremium_hard = [
        pair for pair in problems.stat_status_pairs
        if pair.status != "ac" and not pair.paid_only and pair.difficulty.level == 3
    ]

    return unsolved_nonpremium_easy, unsolved_nonpremium_medium, unsolved_nonpremium_hard

def select_random_questions(easy, medium, hard):
    """
    Select random questions from each difficulty category.
    """
    selected_pairs = {
        'easy': random.sample(easy, min(3, len(easy))),
        'medium': random.sample(medium, min(3, len(medium))),
        'hard': random.sample(hard, min(3, len(hard)))
    }
    return selected_pairs

def initialize_questions():
    """
    Initialize the stored_questions dictionary with selected questions from each difficulty.
    """
    global stored_questions

    # Fetch problem list and statuses
    problems = fetch_problem_list()

    # Filter out premium and already solved questions and group by difficulty
    easy, medium, hard = filter_unsolved_nonpremium(problems)

    # Randomly select questions from each difficulty category
    selected_pairs = select_random_questions(easy, medium, hard)

    for difficulty, pairs in selected_pairs.items():
        stored_questions[difficulty] = []
        for pair in pairs:
            question_title = pair.stat.question__title
            question_slug = pair.stat.question__title_slug
            question_url = f"https://leetcode.com/problems/{question_slug}"
            question_status = "Unsolved" if pair.status != "ac" else "Solved"
            stored_questions[difficulty].append({
                'question_name': question_title,
                'difficulty': difficulty,
                'question_url': question_url,
                'status': question_status
            })

def main():
    
    # Initialize questions once
    initialize_questions()
    # Check if difficulty is provided as command-line argument
    if len(sys.argv) != 2 or sys.argv[1] not in ['easy', 'medium', 'hard']:
        print("Usage: python get_leetcode_questions.py [easy|medium|hard]")
        return

    difficulty = sys.argv[1]
    if difficulty in stored_questions:
        for question in stored_questions[difficulty]:
            print(f"Difficulty: {difficulty.capitalize()}")
            print(f"Question: {question['question_name']}")
            print(f"URL: {question['question_url']}")
            print(f"Status: {question['status']}\n")
    else:
        print(f"No questions available for difficulty: {difficulty}")

if __name__ == "__main__":
    main()
