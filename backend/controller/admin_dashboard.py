from flask import current_app as app, redirect, render_template, request, url_for
from backend.models import*
from .functions import *

@app.route("/search/<name>",methods=["GET","POST"])
def search(name):
    if request.method=="POST":
        search_txt=request.form.get("search_txt")
        by_name=search_by_name(search_txt)
        by_chp=search_by_cname(search_txt)
        by_quiz=search_by_quiz(search_txt)
        if by_name or by_chp:
            if by_name:
                return render_template("admin-dashboard.html",name=name,subjects=by_name)
            if by_chp:
                subject_ids = {chp.sid for chp in by_chp} 
                subjects = Subjects.query.filter(Subjects.id.in_(subject_ids)).all()
                return render_template("admin-dashboard.html", name=name, subjects=subjects)
        if by_quiz:
            return render_template("quiz.html",name=name,quiz=by_quiz)
        return redirect(url_for("admin_dashboard",name=name))    


#SUBJECT-------------------------------------------------------------------------------------------------
@app.route("/subject/<name>",methods=["GET","POST"])
def subject(name):
    if request.method=="POST":
        sname=request.form.get("name")
        info=request.form.get("info")
        if not sname or not info:
            return render_template("subject.html", msg="All fields are required.")
        new_sub=Subjects(name=sname,info=info)
        db.session.add(new_sub)
        db.session.commit()
        return redirect(url_for("admin_dashboard",name=name))

    return render_template("subject.html",name=name)

@app.route("/edit_subject/<id>/<name>",methods=["GET","POST"])
def edit_subject(id,name):
    s=get_subject(id)
    if request.method=="POST":
        mname=request.form.get("name")
        info=request.form.get("info")
        if not mname or not info:
            return render_template("edit_subject.html", msg="All fields are required.")
        s.name=mname
        s.info=info
        db.session.commit()
        return redirect(url_for("admin_dashboard",name=name))
    return render_template("edit_subject.html",subject=s,name=name)

@app.route("/delete_sub/<id>/<name>",methods=["GET","POST"])
def delete_sub(id,name):
    s=get_subject(id)
    db.session.delete(s)
    db.session.commit()
    return redirect(url_for("admin_dashboard",name=name))


#CHAPTER------------------------------------------------------------------------------------------
@app.route("/chapter/<sid>/<name>",methods=["GET","POST"])
def chapter(sid,name):
    if request.method=="POST":
        cname=request.form.get("name")
        info=request.form.get("info")
        if not cname or not info:
           return render_template("chapter.html", msg="All fields are required.")
        new_chp=Chapter(name=cname,info=info,sid=sid)
        db.session.add(new_chp)
        db.session.commit()
        return redirect(url_for("admin_dashboard",name=name))

    return render_template("chapter.html",sid=sid,name=name)

@app.route("/edit_chapter/<id>/<name>",methods=["GET","POST"])
def edit_chapter(id,name):
    c=get_chapter(id)
    if request.method=="POST":
        mname=request.form.get("name")
        info=request.form.get("info")
        if not mname or not info:
            return render_template("edit_chapter.html", msg="All fields are required.")
        c.name=mname
        c.info=info
        db.session.commit()
        return redirect(url_for("admin_dashboard",name=name))
    return render_template("edit_chapter.html",chapter=c,name=name)

@app.route("/delete_chp/<id>/<name>",methods=["GET","POST"])
def delete_chp(id,name):
    c=get_chapter(id)
    db.session.delete(c)
    db.session.commit()
    return redirect(url_for("admin_dashboard",name=name))
      