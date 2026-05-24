import sqlite3
from model import Question,Answer,Participation
from typing import List, Optional


def create_tables():
    conn = sqlite3.connect('QuizDB.db')
    cur = conn.cursor()

    # Drop existing tables if they exist
    cur.execute("DROP TABLE IF EXISTS answers")
    cur.execute("DROP TABLE IF EXISTS question")
    cur.execute("DROP TABLE IF EXISTS participation")

    # Create the question table
    cur.execute("""
        CREATE TABLE question (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            position INTEGER NOT NULL,
            titre TEXT NOT NULL,
            text TEXT NOT NULL,
            pic TEXT
        )
    """)

    # Create the answers table
    cur.execute("""
        CREATE TABLE answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            isCorrect BOOLEAN NOT NULL,
            FOREIGN KEY (question_id) REFERENCES question (ID)
        )
    """)

    # Create the participation table
    cur.execute("""
        CREATE TABLE participation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            playerName TEXT NOT NULL,
            answers TEXT NOT NULL,
            score INTEGER NOT NULL
            
        )
    """)

    conn.commit()
    conn.close()


    
def connect_db():
    """
    Crée une connexion à la base de données SQLite.
    """
    return sqlite3.connect("QuizDB.db",timeout=10)

def insert_question_with_answers(question: Question) -> int:
    """
    Inserts a question and its possible answers into the database.
    If the position is already taken, shifts existing questions forward.
    Returns the ID of the newly inserted question.
    """
    conn = connect_db()
    cur = conn.cursor()

    try:
        cur.execute("begin")

        # Check if the position is already occupied
        cur.execute("SELECT id FROM question WHERE position = ?", (question.position,))
        existing_question = cur.fetchone()

        if existing_question:
            # Shift all questions with position >= new question's position
            cur.execute(
                "UPDATE question SET position = position + 1 WHERE position >= ?",
                (question.position,)
            )

        # Insert the new question
        cur.execute(
            "INSERT INTO question (position, titre, text, pic) VALUES (?, ?, ?, ?)",
            (question.position, question.title, question.text, question.image)
        )
        question_id = cur.lastrowid  # Get the ID of the newly inserted question

        # Insert the answers
        for answer in question.possibleAnswers:
            cur.execute(
                "INSERT INTO answers (question_id, text, isCorrect) VALUES (?, ?, ?)",
                (question_id, answer.text, answer.isCorrect)
            )

        cur.execute("commit")
        return question_id  # Return the ID of the inserted question
    except sqlite3.IntegrityError as e:
        cur.execute("rollback")
        raise ValueError("A question with this position already exists.") from e
    except Exception as e:
        cur.execute("rollback")
        raise e
    finally:
        conn.close()

def get_question_by_id(question_id: int) -> Question:
    """
    Fetches a question and its possible answers from the database by ID.
    Returns a Question object or None if the question is not found.
    """
    conn = connect_db()
    cur = conn.cursor()

    try:
        # Fetch the question
        cur.execute("SELECT ID, position, titre, text, pic FROM question WHERE ID = ?", (question_id,))
        question_row = cur.fetchone()

        if not question_row:
            return None  # Question not found

        # Create the Question object
        question = Question(
            id=question_row[0],  # Pass the ID
            position=question_row[1],
            title=question_row[2],
            text=question_row[3],
            image=question_row[4]
        )

        # Fetch the answers
        cur.execute("SELECT id, text, isCorrect FROM answers WHERE question_id = ?", (question_id,))
        answer_rows = cur.fetchall()

        # Add Answer objects to the Question
        for row in answer_rows:
            answer = Answer(
                id=row[0],  # Include the ID if needed
                text=row[1],
                isCorrect=bool(row[2])
            )
            question.possibleAnswers.append(answer)

        return question
    except Exception as e:
        raise e
    finally:
        conn.close()

def get_question_by_position(position: int) -> Question:
    """
    Fetches a question and its possible answers from the database by position.
    Returns a Question object or None if the question is not found.
    """
    conn = connect_db()
    cur = conn.cursor()

    try:
        # Fetch the question
        cur.execute("SELECT id, position, titre, text, pic FROM question WHERE position = ?", (position,))
        question_row = cur.fetchone()

        if not question_row:
            return None  # Question not found

        # Create the Question object
        question = Question(
            id=question_row[0],  # Include the ID if needed
            position=question_row[1],
            title=question_row[2],
            text=question_row[3],
            image=question_row[4]
        )

        # Fetch the answers
        cur.execute("SELECT id, text, isCorrect FROM answers WHERE question_id = ?", (question_row[0],))
        answer_rows = cur.fetchall()

        # Add Answer objects to the Question
        for row in answer_rows:
            answer = Answer(
                id=row[0],  # Include the ID if needed
                text=row[1],
                isCorrect=bool(row[2])
            )
            question.possibleAnswers.append(answer)

        return question
    except Exception as e:
        raise e
    finally:
        conn.close()

import logging

logger = logging.getLogger(__name__)

import logging

logger = logging.getLogger(__name__)

def update_question_with_answers(question_id: int, updated_question: Question) -> bool:
    conn = connect_db()
    cur = conn.cursor()

    try:
        cur.execute("begin")

        # Fetch the current position of the question being updated
        cur.execute("SELECT position FROM question WHERE id = ?", (question_id,))
        current_position_row = cur.fetchone()
        if not current_position_row:
            raise ValueError("Question not found.")

        current_position = current_position_row[0]  # Extract the current position

        logger.info(f"Updating question ID {question_id} from position={current_position} to position={updated_question.position}")

        # Validate the new position
        cur.execute("SELECT COUNT(*) FROM question")
        total_questions = cur.fetchone()[0]
        if updated_question.position < 1 or updated_question.position > total_questions:
            raise ValueError(f"Invalid position: {updated_question.position}. Position must be between 1 and {total_questions}.")

        # If the new position is different, handle position shifting
        if updated_question.position != current_position:
            if updated_question.position > current_position:
                # Shift questions forward (new position is higher)
                logger.debug(f"Shifting questions forward: position > {current_position} AND position <= {updated_question.position}")
                cur.execute(
                    "UPDATE question SET position = position - 1 WHERE position > ? AND position <= ?",
                    (current_position, updated_question.position)
                )
            else:
                # Shift questions backward (new position is lower)
                logger.debug(f"Shifting questions backward: position >= {updated_question.position} AND position < {current_position}")
                cur.execute(
                    "UPDATE question SET position = position + 1 WHERE position >= ? AND position < ?",
                    (updated_question.position, current_position)
                )

            # Move the question to its new position
            cur.execute(
                "UPDATE question SET position = ? WHERE id = ?",
                (updated_question.position, question_id)
            )

        # Update the question details (title, text, image) if provided
        if updated_question.title or updated_question.text or updated_question.image:
            cur.execute(
                "UPDATE question SET titre = ?, text = ?, pic = ? WHERE id = ?",
                (updated_question.title, updated_question.text, updated_question.image, question_id)
            )

        # Delete existing answers for the question
        cur.execute("DELETE FROM answers WHERE question_id = ?", (question_id,))

        # Insert the updated answers
        for answer in updated_question.possibleAnswers:
            cur.execute(
                "INSERT INTO answers (question_id, text, isCorrect) VALUES (?, ?, ?)",
                (question_id, answer.text, answer.isCorrect)
            )

        cur.execute("commit")
        logger.info("Question updated successfully")
        return True  # Update successful
    except Exception as e:
        cur.execute("rollback")
        logger.error(f"Error updating question: {e}")
        raise e
    finally:
        conn.close()


def delete_question_with_answers(question_id: int) -> bool:
    """
    Deletes a question and its possible answers from the database.
    Adjusts the positions of the remaining questions to fill the gap.
    Returns True if the deletion is successful, False otherwise.
    """
    conn = connect_db()
    cur = conn.cursor()

    try:
        # Start a transaction
        cur.execute("begin")

        # Fetch the position of the question to be deleted
        cur.execute("SELECT position FROM question WHERE id = ?", (question_id,))
        question_row = cur.fetchone()
        if not question_row:
            raise ValueError("Question not found.")

        position_to_delete = question_row[0]  # Position of the question to delete

        # Delete the question and its answers
        cur.execute("DELETE FROM answers WHERE question_id = ?", (question_id,))
        cur.execute("DELETE FROM question WHERE id = ?", (question_id,))

        # Adjust the positions of the remaining questions
        cur.execute(
            "UPDATE question SET position = position - 1 WHERE position > ?",
            (position_to_delete,)
        )

        # Commit the transaction
        cur.execute("commit")
        return True  # Deletion successful
    except Exception as e:
        # Rollback the transaction in case of an error
        cur.execute("rollback")
        raise e
    finally:
        conn.close()

def delete_all_questions() -> bool:
    """
    Deletes all questions and their possible answers from the database.
    Returns True if the deletion is successful, False otherwise.
    """
    conn = connect_db()
    cur = conn.cursor()

    try:
        # Delete all questions and answers in a transaction
        cur.execute("begin")
        cur.execute("DELETE FROM answers")  # Delete all answers
        cur.execute("DELETE FROM question")  # Delete all questions
        cur.execute("commit")
        return True  # Deletion successful
    except Exception as e:
        cur.execute("rollback")
        raise e
    finally:
        conn.close()

def insert_participation(player_name: str, answers: List[int], score: int) -> int:
    """
    Inserts a new participation record into the database.
    :param player_name: Name of the participant.
    :param answers: List of answers provided by the participant.
    :param score: The calculated score.
    :return: The ID of the inserted record.
    """
    conn = connect_db()
    cur = conn.cursor()

    try:
        # Serialize the answers list to JSON
        answers_json = json.dumps(answers)

        # Insert the participation record
        cur.execute(
            "INSERT INTO participation (playerName, answers, score) VALUES (?, ?, ?)",
            (player_name, answers_json, score)
        )
        conn.commit()
        return cur.lastrowid  # Return the ID of the inserted record
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
import logging
import json
# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def calculate_score(answers: List[int]) -> int:
    """
    Calculates the score by comparing the participant's answers with the correct answers.
    :param answers: List of answers provided by the participant (1 to 4 for each question).
    :return: The calculated score.
    """
    conn = connect_db()
    cur = conn.cursor()

    try:
        # Fetch all questions ordered by position
        cur.execute("SELECT id, position FROM question ORDER BY position")
        questions = cur.fetchall()

        # Ensure there are exactly 10 questions
        if len(questions) != 10:
            raise ValueError("The quiz must have exactly 10 questions.")

        score = 0

        # Compare each answer with the correct answer
        for i, (question_id, _) in enumerate(questions):
            # Fetch all answers for the question, ordered by ID
            cur.execute("SELECT id, isCorrect FROM answers WHERE question_id = ? ORDER BY id", (question_id,))
            answer_rows = cur.fetchall()

            # Ensure there are exactly 4 answers for the question
            if len(answer_rows) != 4:
                raise ValueError(f"Question ID {question_id} does not have exactly 4 answers.")

            # Find the correct answer's position (1 to 4)
            correct_answer_position = None
            for idx, (answer_id, is_correct) in enumerate(answer_rows):
                if is_correct:
                    correct_answer_position = idx + 1  # Enumerate from 1 to 4
                    break

            # Ensure a correct answer was found
            if correct_answer_position is None:
                raise ValueError(f"No correct answer found for question ID {question_id}.")

            # Debugging: Log the comparison
            logger.debug(f"Question ID: {question_id}")
            logger.debug(f"Participant's Answer: {answers[i]}")
            logger.debug(f"Correct Answer Position: {correct_answer_position}")

            # Check if the participant's answer matches the correct answer's position
            if answers[i] == correct_answer_position:
                logger.debug("Answer is correct!")
                score += 1
            else:
                logger.debug("Answer is incorrect.")

        logger.debug(f"Total Score: {score}")
        return score
    except Exception as e:
        logger.error(f"Error calculating score: {e}")
        raise e
    finally:
        conn.close()

def delete_all_participations() -> bool:
    """
    Deletes all participation records from the database.
    Returns True if successful, False otherwise.
    """
    conn = connect_db()
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM participation")
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_total_questions() -> int:
    """
    Fetches the total number of questions in the database.
    Returns the count as an integer.
    """
    conn = connect_db()
    cur = conn.cursor()

    try:
        # Execute the query to count all questions
        cur.execute("SELECT COUNT(*) FROM question")
        result = cur.fetchone()  # Fetch the result (a single row with the count)
        return result[0] if result else 0  # Return the count or 0 if no result
    except Exception as e:
        raise e
    finally:
        conn.close()
def get_all_scores() -> list:
    """
    Fetches all participation records from the database.
    Returns a list of dictionaries, each containing playerName and score.
    """
    conn = connect_db()
    cur = conn.cursor()

    try:
        # Execute the query to fetch all participations, ordered by score (descending)
        cur.execute("SELECT playerName, score FROM participation ORDER BY score DESC")
        rows = cur.fetchall()  # Fetch all rows

        # Convert rows to a list of dictionaries
        scores = [
            {"playerName": row[0], "score": row[1]}
            for row in rows
        ]
        return scores
    except Exception as e:
        raise e
    finally:
        conn.close()