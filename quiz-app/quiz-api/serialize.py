from model import Question, Answer,Participation

def question_to_json(question: Question) -> dict:
    """
    Converts a Question object to a JSON-compatible dictionary.
    """
    return {
        "id": question.id if hasattr(question, 'id') else None,
        "position": question.position,
        "title": question.title,
        "text": question.text,
        "image": question.image,
        "possibleAnswers": [
            {
                "id": answer.id if hasattr(answer, 'id') else None,
                "text": answer.text,
                "isCorrect": answer.isCorrect
            }
            for answer in question.possibleAnswers
        ]
    }

def json_to_question(data: dict) -> Question:
    """
    Converts a JSON-compatible dictionary to a Question object.
    """
    # Extract question data
    question = Question(
        position=data.get("position"),
        title=data.get("title"),
        text=data.get("text"),
        image=data.get("image")
    )

    # Extract and add answers
    for answer_data in data.get("possibleAnswers", []):
        answer = Answer(
            text=answer_data.get("text"),
            isCorrect=answer_data.get("isCorrect", False)
        )
        question.possibleAnswers.append(answer)

    return question

def participation_to_json(participation: Participation) -> dict:
    """
    Converts a Participation object to a JSON-compatible dictionary.
    """
    return {
        "id": participation.id,
        "playerName": participation.playerName,
        "answers": participation.answers  # Include the answers
    }

def json_to_participation(data: dict) -> Participation:
    """
    Converts a JSON-compatible dictionary to a Participation object.
    """
    return Participation(
        id=data.get("id"),
        playerName=data["playerName"],
        answers=data["answers"]  # Include the answers
    )