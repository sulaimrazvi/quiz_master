from datetime import datetime
from flask import current_app as app, redirect, render_template, request, url_for
from backend.models import*
from .functions import *



@app.route("/admin/<name>/quiz")
def quiz(name):
    quizs=get_quizs()
    return render_template("quiz.html",name=name,quiz=quizs)


#QUIZ---------------------------------------------------------------------
@app.route("/admin/quiz/<name>", methods=["GET", "POST"])
def add_quiz(name):
    if request.method == "POST":
        name = request.form.get("name") 
        cid = request.form.get("cid")  
        date_str = request.form.get("date")
        time_str = request.form.get("time")
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        duration = datetime.strptime(time_str, "%H:%M").time()
        if not name or not cid or not date or not duration:
            return render_template("add_quiz.html", msg="All fields are required.") 
        new_quiz = Quiz(name=name,cid=cid,date=date, duration=duration)
        db.session.add(new_quiz)
        db.session.commit()

        return redirect(url_for("quiz", name=name))

    return render_template("add_quiz.html",name=name)

@app.route("/edit_quiz/<id>/<name>",methods=["GET","POST"])
def edit_quiz(id,name):
    q=get_quiz(id)
    if request.method=="POST":
        qname=request.form.get("name")
        cid=request.form.get("cid")
        date_str = request.form.get("date")
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        duration=request.form.get("duration")
        if not name or not cid or not date or not duration:
            return render_template("edit_quiz.html", msg="All fields are required.")   
        q.name=qname
        q.cid=cid
        q.date =date
        if ":" in duration[5:]: 
            q.duration = datetime.strptime(duration, "%H:%M:%S").time()
        else:
            q.duration = datetime.strptime(duration, "%H:%M").time()
        db.session.commit()
        return redirect(url_for("quiz",name=name))
    return render_template("edit_quiz.html",quiz=q,name=name)

@app.route("/delete_quiz/<id>/<name>",methods=["GET","POST"])
def delete_quiz(id,name):
    q=get_quiz(id)
    db.session.delete(q)
    db.session.commit()
    return redirect(url_for("quiz",name=name))

#QUESTION------------------------------------------------------
@app.route("/question/<qid>/<name>",methods=["GET","POST"])
def question(qid,name):
    if request.method=="POST":
        qs_stmt = request.form.get("qs_stmt")
        answer = request.form.get("answer")
        marks = request.form.get("marks")
        option1 = request.form.get("option1")
        option2 = request.form.get("option2")
        option3 = request.form.get("option3")
        option4 = request.form.get("option4")
        if not qs_stmt or not answer or not option1 or not option2 or not option3 or not option4 or not marks:
            return render_template("add_question.html", msg="All fields are required.")  
        new_question = Question(qid=qid, qs_stmt=qs_stmt, answer=answer,marks=marks)
        db.session.add(new_question)
        db.session.flush()
        db.session.commit()
        new_option = Option(question_id=new_question.id, option1=option1, option2=option2, option3=option3, option4=option4)
        db.session.add(new_option)
        db.session.commit()
        return redirect(url_for("quiz",name=name))

    return render_template("add_question.html",qid=qid,name=name)


@app.route("/edit_question/<id>/<name>", methods=["GET", "POST"])
def edit_question(id, name):
    q = get_question(id)
    options = get_options(id)
    if request.method == "POST":
        if not q.qs_stmt or not q.answer or not options or not q.marks:
            return render_template("edit_question.html", msg="All fields are required.")  
        q.qs_stmt = request.form.get("qs_stmt")
        q.answer = request.form.get("answer")
        q.marks = request.form.get("marks")
        options.option1 = request.form.get("option1")
        options.option2 = request.form.get("option2")
        options.option3 = request.form.get("option3")
        options.option4 = request.form.get("option4") 
        db.session.commit()
        return redirect(url_for("quiz", name=name))
    return render_template("edit_question.html", question=q, option=options, name=name)


@app.route("/delete_qs/<id>/<name>",methods=["GET","POST"])
def delete_qs(id,name):
    q=get_question(id)
    o=get_options(id)
    db.session.delete(q)
    db.session.delete(o)
    db.session.commit()
    return redirect(url_for("quiz",name=name))
