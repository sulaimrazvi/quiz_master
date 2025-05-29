from datetime import datetime, timedelta
from flask import current_app as app, redirect, render_template, request, session, url_for
from backend.models import *
from .functions import *

#NAV BAR ROUTES _----------------------------------------------------------------------------------------
@app.route("/user/<name>/scores")
def scores(name):
    quizs = get_quizs()
    scores=get_score()
    user_id = session.get("user_id")
    return render_template("scores.html", name=name, quiz=quizs,user_id=user_id)
  

@app.route("/Qsearch/<name>",methods=["GET","POST"])
def qsearch(name):
    if request.method=="POST":
        search=request.form.get("search")
        by_quiz=search_by_quiz(search)
        if by_quiz:
            return render_template("user-dashboard.html",name=name,quiz=by_quiz)

    return redirect(url_for("user_dashboard",name=name))

# START AND VIEW QUIZ-----------------------------------------------------------------------------------------------------

@app.route("/view_quiz/<id>/<name>",methods=["GET","POST"])
def view_quiz(id,name):
    q=get_quiz(id)
    chapter = q.chapter 
    subject = chapter.subjects
    return render_template("view_quiz.html", quiz=q, chapter=chapter, subject=subject, name=name)

@app.route("/start_quiz/<quiz_id>/<name>/<q_index>", methods=["GET", "POST"])
def start_quiz(quiz_id, name, q_index):
    quiz = get_quiz(quiz_id)
    questions = quiz.questions
    q_index = int(q_index)

    if q_index >= len(questions):
        return redirect(url_for("user_dashboard", name=name))
    if "quiz_start_time" not in session:
        session["quiz_start_time"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    start_time = datetime.strptime(session["quiz_start_time"], '%Y-%m-%d %H:%M:%S')
    q_duration = quiz.duration
    q_delta = timedelta(hours=q_duration.hour, minutes=q_duration.minute)
    end_time = start_time + q_delta


    remaining_time = max(int((end_time - datetime.now()).total_seconds()), 0)


    if remaining_time <= 0:
        session.pop("quiz_start_time", None) 
        return redirect(url_for("user_dashboard", name=name))

    current_question = questions[q_index]

    if request.method == "POST":
        user_answer = request.form.get("canswer")
        user_id = session.get("user_id")
        score = Scores.query.filter_by(qid=quiz_id, uid=user_id).first()
        if not score:
            score = Scores(qid=quiz_id, uid=user_id, score=0, time=datetime.now())
            db.session.add(score)

        if user_answer == current_question.answer:
            score.score += current_question.marks
        db.session.commit()


        
        return redirect(url_for("start_quiz", quiz_id=quiz_id, name=name, q_index=q_index + 1,uid=user_id))

    options =get_options(current_question.id)
    
    
    return render_template("start_quiz.html", quiz=quiz, question=current_question, options=options, q_index=q_index, name=name,total_questions=len(questions),remaining_time=remaining_time)

# USER SCORE RETEST---------------------------------------------------------------------------------------------------
@app.route("/retest/<id>/<name>", methods=["GET", "POST"])
def delete_score(id, name):
    q=get_quiz(id)
    user_id = session.get("user_id")
    score = Scores.query.filter_by(qid=id, uid=user_id).first()
    if score:
        db.session.delete(score)
        db.session.commit()

    return redirect(url_for("user_dashboard",name=name))