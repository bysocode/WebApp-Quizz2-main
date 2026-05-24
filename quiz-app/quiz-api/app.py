from flask_cors import CORS
import hashlib
import jwt
import os
from flask import Flask, request, jsonify
from jwt_utils import build_token, JwtError , decode_token
from model import Question,Answer
from serialize import json_to_question, question_to_json
from database import get_total_questions,calculate_score, get_all_scores,insert_question_with_answers,create_tables ,delete_all_participations,insert_participation,delete_all_questions,get_question_by_id,get_question_by_position,update_question_with_answers,delete_question_with_answers
app = Flask(__name__)

CORS(app)
HARD_CODED_PASSWORD_HASH = "d8170650479293c12e0201e5fdf45f40"
@app.route('/')
def hello_world():
	x = 'world'
	return f"stupid, {x}"


@app.route('/rebuild-db', methods=['POST'])
def rebuild_db():
    try:
        # Check if the database file exists and delete it
        if os.path.exists('QuizDB.db'):
            os.remove('QuizDB.db')

        # Recreate the tables
        create_tables()

        return "Ok", 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
    try:
        total_questions = get_total_questions()  # Get the total number of questions
        scores = get_all_scores()  # Get all scores
        return {"size": total_questions, "scores": scores}, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    payload = request.get_json()

    password = payload.get('password')

    if not password:
        return jsonify({"error": "Password is required"}), 400


    hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()

  
    if hashed_password == HARD_CODED_PASSWORD_HASH :
            token = build_token()
            print(f"Token: {token}")
            return jsonify({"token":token}), 200
        
        
    return jsonify({"error": "Unauthorized"}), 401
    
@app.route('/questions', methods=['POST'])
def post_question():
    """
    Endpoint to add a new question with its possible answers.
    """
    # Validate authorization token
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Token is missing"}), 401

    try:
        auth_token = auth_header.split(" ")[1]
    except IndexError:
        return jsonify({"error": "Invalid token format"}), 401

    try:
        user_id = decode_token(auth_token)
    except JwtError as e:
        return jsonify({"error": str(e)}), 401

    # Get JSON data from the request
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400

    # Convert JSON to Question object
    question = json_to_question(data)
    print(question)
    # Insert the question and answers into the database
    try:
        question_id = insert_question_with_answers(question)
        return jsonify({"id": question_id}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400  # Handle unique constraint violation
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
    """
    Endpoint to fetch a question and its possible answers by ID.
    """
    try:
        # Fetch the question from the database
        question = get_question_by_id(question_id)
        if not question:
            return jsonify({"error": "Question not found"}), 404

        # Convert the Question object to JSON
        question_json = question_to_json(question)
        return jsonify(question_json), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/questions', methods=['GET'])
def get_question_by_position_endpoint():
    """
    Endpoint to fetch a question and its possible answers by position.
    Uses a query parameter: /questions?position=2
    """
    try:
        # Get the position from the query parameters
        position = request.args.get('position', type=int)

        if position is None:
            return jsonify({"error": "Position query parameter is required"}), 400

        # Fetch the question from the database
        question = get_question_by_position(position)
        if not question:
            return jsonify({"error": "Question not found"}), 404

        # Convert the Question object to JSON
        question_json = question_to_json(question)
        return jsonify(question_json), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/questions/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    """
    Endpoint to update a question and its possible answers by ID.
    """
    # Validate authorization token
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Token is missing"}), 401

    try:
        auth_token = auth_header.split(" ")[1]
    except IndexError:
        return jsonify({"error": "Invalid token format"}), 401

    try:
        user_id = decode_token(auth_token)
    except JwtError as e:
        return jsonify({"error": str(e)}), 401

    # Get JSON data from the request
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400

    # Convert JSON to Question object
    updated_question = json_to_question(data)

    # Update the question and answers in the database
    try:
        success = update_question_with_answers(question_id, updated_question)
        if not success:
            return jsonify({"error": "Failed to update question"}), 500

        return jsonify({"message": "Question updated successfully"}), 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    """
    Endpoint to delete a question and its possible answers by ID.
    """
    # Validate authorization token
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Token is missing"}), 401

    try:
        auth_token = auth_header.split(" ")[1]
    except IndexError:
        return jsonify({"error": "Invalid token format"}), 401

    try:
        user_id = decode_token(auth_token)
    except JwtError as e:
        return jsonify({"error": str(e)}), 401

    # Delete the question and its answers from the database
    try:
        success = delete_question_with_answers(question_id)
        if not success:
            return jsonify({"error": "Failed to delete question"}), 500

        return jsonify({"message": "Question deleted successfully"}), 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/questions/all', methods=['DELETE'])
def delete_all_questions_endpoint():
    """
    Endpoint to delete all questions and their possible answers.
    """
    # Validate authorization token
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Token is missing"}), 401

    try:
        auth_token = auth_header.split(" ")[1]
    except IndexError:
        return jsonify({"error": "Invalid token format"}), 401

    try:
        user_id = decode_token(auth_token)
    except JwtError as e:
        return jsonify({"error": str(e)}), 401

    # Delete all questions and answers from the database
    try:
        success = delete_all_questions()
        if not success:
            return jsonify({"error": "Failed to delete all questions"}), 500

        return jsonify({"message": "All questions deleted successfully"}), 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/participations', methods=['POST'])
def add_participation():
    """
    Endpoint to add a new participation record.
    Validates the request, calculates the score, and inserts the record into the database.
    """
    data = request.get_json()

    # Validate the request
    if not data or "playerName" not in data or "answers" not in data:
        return jsonify({"error": "playerName and answers are required"}), 400

    player_name = data["playerName"]
    answers = data["answers"]

    # Ensure there are exactly 10 answers
    if len(answers) != 10:
        return jsonify({"error": "Exactly 10 answers are required"}), 400

    # Calculate the score
    try:
        score = calculate_score(answers)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Insert the participation record
    try:
        participation_id = insert_participation(player_name, answers, score)
        return jsonify({"playerName": player_name, "score": score, "answers": answers}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/participations/all', methods=['DELETE'])
def delete_all_participations_endpoint():
    """
    Endpoint to delete all participation records.
    Requires a valid JWT token in the Authorization header.
    """
    # Validate authorization token
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"error": "Token is missing"}), 401

    try:
        auth_token = auth_header.split(" ")[1]
    except IndexError:
        return jsonify({"error": "Invalid token format"}), 401

    try:
        user_id = decode_token(auth_token)
    except JwtError as e:
        return jsonify({"error": str(e)}), 401

    # Delete all participation records from the database
    try:
        success = delete_all_participations()
        if not success:
            return jsonify({"error": "Failed to delete all participations"}), 500

        return jsonify({"message": "All participations deleted successfully"}), 204
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
