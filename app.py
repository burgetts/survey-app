from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import surveys

# Set up flask
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'beans'
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Global variables
survey_index = 1
survey = surveys.satisfaction_survey
temp_responses = []

# Home page
@app.route('/')
def show_survey_home_page():
    """Show survey title and instructions"""
    survey_title = survey.title
    instructions = survey.instructions
    return render_template('start.html', survey_title=survey_title, instructions=instructions) # TEST FOR NOW, INCLUDE BUTTON IN NEXT FILE

# Each question in survey
@app.route('/questions/<question_num>')
def show_question(question_num):
    """Show question and answer choices, ensure user is on correct survey question"""
    num_questions = 0 # Total # questions in survey
    question_num = int(question_num) # Question we are currently on
    
    # Get length of survey
    for question in survey.questions: 
        num_questions += 1
    
    # Make sure user hasn't skipped any questions
    if int(question_num) != survey_index:
        flash("You are trying to access an invalid question. You have been redirected to the survey.")
        return redirect(f'/questions/{survey_index}')
    # If questions left, display question and answer
    if int(question_num) < num_questions:
        question = survey.questions[question_num].question
        choices = survey.questions[question_num].choices
        return render_template('question_form.html', question=question, choices=choices)
    
    else:
        raise
        return render_template('thanks.html')

@app.route('/answer', methods=['POST'])
def record_answer():
    """Record answer in session, redirect to next question"""
    answer = request.form["answer"]
    # Save reponses to session
    temp_responses.append(answer)
    session["responses"] = temp_responses
    global survey_index
    survey_index += 1
    # Direct to next question
    return redirect(f'/questions/{survey_index}')

@app.route('/session-setup', methods=["POST"])
def setup_session():
    """Set up responses in session and redirect to first question"""
    session["responses"] = []
    return redirect('/questions/1')