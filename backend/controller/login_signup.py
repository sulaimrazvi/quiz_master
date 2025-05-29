from flask import render_template,request,redirect,url_for, current_app as app,session
from datetime import datetime
from backend.models import *
from .functions import *


#LOGIN------------------------------------------------------

@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form.get("email")
        pwd = request.form.get("password")
        usr = User_info.query.filter_by(email=uname, password=pwd).first()
        if usr:
            session['user_id'] = usr.id
        if usr and usr.role == 0:
            return redirect(url_for("admin_dashboard",name=uname))
        elif usr and usr.role == 1:
            return redirect(url_for("user_dashboard",name=uname))
        else:
            return render_template("login.html",msg="invalid user credential...")
    return render_template("login.html",msg="")

#SIGNUP-----------------------------------------------------------------------
@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        uname=request.form.get("email")
        pwd=request.form.get("password")
        fullname=request.form.get("fullname")
        qualification=request.form.get("qualification")
        dob_str=request.form.get("dob")
        if not uname or not pwd or not fullname or not qualification or not dob_str:
            return render_template("signup.html", msg="All fields are required.")
        try:   
            dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
        except ValueError:
            return render_template("signup.html", msg="Invalid date format. Use YYYY-MM-DD.")
        usr = User_info.query.filter_by(email=uname).first()
        if usr:
            return render_template("signup.html",msg="sorry mail already in use")
        new_usr=User_info(email=uname,password=pwd,full_name=fullname,qualification=qualification,dob=dob)
        db.session.add(new_usr)
        db.session.commit()
        return render_template("login.html",msg="registeration successfull, log in now ")

    return render_template("signup.html")


#common route for admin
@app.route("/admin/<name>")
def admin_dashboard(name):
    subjects=get_subjects()
    return render_template("admin-dashboard.html",name=name,subjects=subjects)

#common route for user
@app.route("/user/<name>")
def user_dashboard(name):
    quiz=get_quizs()
    user_id = session.get("user_id")
    return render_template("user-dashboard.html",name=name,quiz=quiz,user_id=user_id)
