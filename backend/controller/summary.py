from flask import current_app as app, jsonify, redirect, render_template, request, session, url_for
from sqlalchemy.sql import text
from backend.models import *
from .functions import *
@app.route("/admin/<name>/admin-summary")
def admin_summary(name):
    user=get_users()
    return render_template("admin-summary.html", name=name,user=user)

@app.route("/summary_plot")
def summary_plot():
    
    highest_scores = db.session.execute(text("""
        SELECT quiz.name, MAX(scores.score) 
        FROM quiz 
        JOIN scores ON quiz.id = scores.qid 
        GROUP BY quiz.name;
    """)).fetchall()

    
    attempts = db.session.execute(text("""
        SELECT quiz.name, COUNT(DISTINCT scores.uid) 
        FROM quiz 
        JOIN scores ON quiz.id = scores.qid 
        GROUP BY quiz.name;
    """)).fetchall()

    tests=db.session.execute(text("""
        SELECT  subjects.name,count(quiz.id)
        FROM subjects,chapter,quiz 
        WHERE subjects.id=chapter.sid and chapter.id=quiz.cid
        GROUP BY subjects.name;  """
    )).fetchall()

    
    q_names = [row[0] for row in highest_scores]
    max_scores = [row[1] for row in highest_scores]

 
    attempt_labels = [row[0] for row in attempts]
    attempt_counts = [row[1] for row in attempts]

    
    test_labels = [row[0] for row in tests]
    test_counts = [row[1] for row in tests]

    return jsonify({
        "bar_chart": {"labels": q_names, "data": max_scores},
        "pie_chart": {"labels": attempt_labels, "data": attempt_counts},
        "bar_chart_test": {"labels": test_labels, "data": test_counts}
       
    })


@app.route("/usearch/<name>", methods=["GET", "POST"])
def usearch(name):
    if request.method == "POST":
        search = request.form.get("search_txt")
        by_user = search_by_user(search)
        return render_template("admin-summary.html", name=name, user=by_user)

    return redirect(url_for("admin_summary", name=name))

@app.route("/view/<id>/<name>")
def view(name, id):
    user = User_info.query.filter_by(id=id).first()
    return render_template("user-view.html", user=user, name=name, user_id=id)



# USER SUMMARY -------------------------------------------------------------------------------------
@app.route("/user/<name>/u-summary")
def u_summary(name):
    user_id = session.get("user_id")
    return render_template("user-summary.html", name=name,user_id=user_id)
  

@app.route("/u_summary_plot/<user_id>")
def u_summary_plot(user_id):
    user_id=int(user_id)
    if not user_id:
        user_id=session.get[user_id]
    highscore = db.session.execute(text("""
    SELECT q.name, 
           MAX(COALESCE(s.score, 0)) AS highest_score
    FROM quiz q
    LEFT JOIN scores s ON q.id = s.qid
    GROUP BY q.name;
""")).fetchall()
    
    
    

    score = db.session.execute(text("""
        SELECT quiz.name, 
               COALESCE(scores.score, 0) AS user_score
        FROM quiz
        LEFT JOIN scores ON quiz.id = scores.qid AND scores.uid = :user_id;
    """), {"user_id": user_id}).fetchall()

  
    quiz_names = [row[0] for row in score]
    scores = [row[1] for row in score]
    dict = {row[0]: row[1] for row in highscore}

    highest_scores = [dict.get(q, 0) for q in quiz_names]
    
    
    tests=db.session.execute(text("""
            SELECT  subjects.name,count(quiz.id)
            FROM subjects,chapter,quiz 
            WHERE subjects.id=chapter.sid and chapter.id=quiz.cid
            GROUP BY subjects.name;  """
        )).fetchall()
    
    
    test_labels = [row[0] for row in tests]
    test_counts = [row[1] for row in tests]

    quizes = db.session.execute(text("""
        SELECT COUNT(DISTINCT qid)
        FROM scores
        WHERE uid = :user_id;
    """), {"user_id": user_id}).scalar()

    nums = db.session.execute(text(""" 
        SELECT COUNT(DISTINCT id)
        FROM quiz
    """)).scalar()

    return jsonify({
        "bar_chart":  {"labels": test_labels, "data": test_counts},
        "cbar_chart": {
            "labels": quiz_names,
            "user_scores": scores,
            "highest_scores": highest_scores
        },
        "count":quizes,
        "num":nums
        
        })
