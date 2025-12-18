from flask import Flask, render_template, request, redirect, url_for, session, make_response
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Quiz questions
questions = [
    {
        "question": "What does CPU stand for?",
        "options": ["Central Processing Unit", "Control Processing Unit", "Computer Processing Unit", "Core Processing Unit"],
        "answer": "Central Processing Unit"
    },
    {
        "question": "What does RAM stand for?",
        "options": ["Random Access Memory", "Read-Only Memory", "Random Active Memory", "Read-All Memory"],
        "answer": "Random Access Memory"
    },
    {
        "question": "What is the full form of HTML?",
        "options": ["Hypertext Markup Language", "Hyper Transfer Markup Language", "Hyperlink Markup Language", "Hyper Transfer Meta Language"],
        "answer": "Hypertext Markup Language"
    },
    {
        "question": "Which key combination is used to paste copied text?",
        "options": ["Ctrl + V", "Ctrl + C", "Ctrl + X", "Ctrl + P"],
        "answer": "Ctrl + V"
    },
    {
        "question": "Which device connects a network to the internet?",
        "options": ["Router", "Modem", "Switch", "Hub"],
        "answer": "Router"
    },
    {
        "question": "What is the base of the binary number system?",
        "options": ["2", "10", "16", "8"],
        "answer": "2"
    },
    {
        "question": "Which programming language is known as the backbone of web development?",
        "options": ["Python", "JavaScript", "Java", "C++"],
        "answer": "JavaScript"
    },
    {
        "question": "Which protocol is used to send emails?",
        "options": ["HTTP", "SMTP", "FTP", "IMAP"],
        "answer": "SMTP"
    },
    {
        "question": "What is the smallest unit of data in a computer?",
        "options": ["Bit", "Byte", "Nibble", "Kilobyte"],
        "answer": "Bit"
    },
    {
        "question": "Which company created the Java programming language?",
        "options": ["Microsoft", "Sun Microsystems", "Apple", "Google"],
        "answer": "Sun Microsystems"
    },
]

# Puzzle data with categories and difficulty levels
puzzles = [
    {"question": "What is always in front of you but can't be seen?", 
     "answer": "Future", "category": "Logic", "difficulty": "Easy", 
     "choices": ["Future", "Past", "Present", "Memory"]},
    
    {"question": "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?", 
     "answer": "Echo", "category": "Riddle", "difficulty": "Medium", 
     "choices": ["Echo", "Sound", "Voice", "Wind"]},
    
    {"question": "What has keys but can't open locks?", 
     "answer": "Piano", "category": "Logic", "difficulty": "Easy", 
     "choices": ["Piano", "Computer", "Map", "Musical"]},
    
    {"question": "The more you take, the more you leave behind. What am I?", 
     "answer": "Footsteps", "category": "Riddle", "difficulty": "Hard", 
     "choices": ["Footsteps", "Time", "Memory", "Space"]},
    
    {"question": "What comes once in a minute, twice in a moment, but never in a thousand years?", 
     "answer": "The letter 'M'", "category": "Riddle", "difficulty": "Medium", 
     "choices": ["The letter 'M'", "Time", "Moment", "Second"]},
    # Add more puzzles here if needed
]

@app.route("/", methods=["GET", "POST"])
def home():
    """Home page for both the quiz and puzzle solving challenge."""
    if request.method == "POST":
        if request.form.get("quiz"):
            # If it's a quiz submission
            return redirect(url_for("quiz"))
        elif request.form.get("puzzle"):
            # If it's a puzzle submission
            return redirect(url_for("puzzle"))

    return render_template("home.html")

# Quiz Flow
@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    """Handles the quiz flow."""
    if "quiz_index" not in session:
        session["quiz_index"] = 0
        session["correct_answers"] = 0
        session["selected_questions"] = random.sample(questions, 10)  # Ensure 10 questions
        session["feedback"] = ""

    quiz_index = session["quiz_index"]
    selected_questions = session["selected_questions"]

    if quiz_index >= 10:
        # Redirect to results after completing all questions
        return redirect("/results")

    current_question = selected_questions[quiz_index]

    if request.method == "POST":
        user_answer = request.form.get("user-answer").strip()
        if not user_answer:
            session["feedback"] = "⚠️ Please provide an answer!"
            return redirect(url_for("quiz"))

        correct_answer = current_question["answer"]
        if user_answer.lower() == correct_answer.lower():
            session["correct_answers"] += 1
            session["feedback"] = "✅ Correct!"
        else:
            session["feedback"] = f"❌ Incorrect! The correct answer was: {correct_answer}"

        session["quiz_index"] += 1
        return redirect(url_for("quiz"))

    feedback = session.get("feedback", "")
    return render_template(
        "quiz.html",
        question=current_question["question"],
        options=current_question["options"],
        feedback=feedback,
        score=session["correct_answers"],
        total_questions=10,
        current_question=quiz_index + 1
    )

@app.route("/puzzle", methods=["GET", "POST"])
def puzzle():
    """Handles the puzzle-solving flow."""
    # Initialize session variables if not already set
    if "puzzle_index" not in session:
        session["puzzle_index"] = 0
        session["correct_answers"] = 0  # Initialize the correct_answers key
        puzzle_count = min(10, len(puzzles))  # Sample no more than the length of the list
        session["selected_puzzles"] = random.sample(puzzles, puzzle_count)  # Ensure 10 puzzles
        session["feedback"] = ""

    puzzle_index = session["puzzle_index"]
    selected_puzzles = session["selected_puzzles"]

    # If all puzzles are completed, redirect to results page
    if puzzle_index >= 10:
        return redirect("/results")

    current_puzzle = selected_puzzles[puzzle_index]

    # Handle form submission (user-answer)
    if request.method == "POST":
        user_answer = request.form.get("user-answer").strip()
        if not user_answer:
            session["feedback"] = "⚠️ Please provide an answer!"
            return redirect(url_for("puzzle"))

        correct_answer = current_puzzle["answer"]
        if user_answer.lower() == correct_answer.lower():
            session["correct_answers"] += 1
            session["feedback"] = "✅ Correct!"
        else:
            session["feedback"] = f"❌ Incorrect! The correct answer was: {correct_answer}"

        session["puzzle_index"] += 1
        return redirect(url_for("puzzle"))

    # Puzzle question and options
    feedback = session.get("feedback", "")
    return render_template(
        "puzzle.html",  # Ensure this template exists
        question=current_puzzle["question"],
        options=current_puzzle["choices"],  # Make sure 'choices' is present in the puzzle dictionary
        feedback=feedback,
        score=session["correct_answers"],  # Accessing correct_answers here
        total_puzzles=10,
        current_puzzle=puzzle_index + 1
    )

# Results Page
@app.route("/results")
def results():
    """Results page to display the user's performance."""
    quiz_score = session.get("correct_answers", 0)
    puzzle_score = session.get("score", 0)
    total_score = quiz_score + puzzle_score
    session.clear()  # Clear session to avoid repeated results
    return render_template("results.html", quiz_score=quiz_score, puzzle_score=puzzle_score, total_score=total_score)

if __name__ == "__main__":
    app.run(debug=True)
