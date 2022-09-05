from flask import Flask, render_template, request, redirect, flash
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
responses = []
survey = surveys.satisfaction_survey

# Home page
@app.route('/')
def show_survey_home_page():
    survey_title = survey.title
    instructions = survey.instructions
    return render_template('start.html', survey_title=survey_title, instructions=instructions) # TEST FOR NOW, INCLUDE BUTTON IN NEXT FILE

# Each question in survey
@app.route('/questions/<question_num>')
def show_question(question_num):
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
        return render_template('thanks.html')

@app.route('/answer', methods=['POST'])
def record_answer():
    answer = request.form["answer"]
    responses.append(answer)
    global survey_index
    survey_index += 1
    
    
    
    # Direct to next question
    return redirect(f'/questions/{survey_index}')