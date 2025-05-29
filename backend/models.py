from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class User_info(db.Model):
    __tablename__="user_info"
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    role=db.Column(db.Integer,default=1)
    full_name=db.Column(db.String,nullable=False)
    qualification=db.Column(db.String,nullable=False)
    dob=db.Column(db.Date,nullable=False)
    #relation
    scores=db.relationship("Scores",cascade="all,delete",backref="user_info",lazy=True)
    
#2nd entity
class Subjects(db.Model):
    __tablename__="subjects"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    info=db.Column(db.String,nullable=False)
    chapters=db.relationship("Chapter",cascade="all,delete",backref="subjects",lazy=True)
       
#entity-3
class Chapter(db.Model):
    __tablename__="chapter"
    id=db.Column(db.Integer,primary_key=True)
    sid=db.Column(db.Integer,db.ForeignKey("subjects.id"),nullable=False)
    name=db.Column(db.String,nullable=False)
    info=db.Column(db.String,nullable=False)
    quizs=db.relationship("Quiz",cascade="all,delete",backref="chapter",lazy=True)

#entity 4
class Quiz(db.Model):
    __tablename__="quiz"
    id=db.Column(db.Integer,primary_key=True)
    cid=db.Column(db.Integer,db.ForeignKey("chapter.id"),nullable=False)
    date=db.Column(db.DateTime,nullable=False)
    duration=db.Column(db.Time,nullable=False)
    name=db.Column(db.String,nullable=False)
    questions=db.relationship("Question",cascade="all,delete",backref="quiz",lazy=True)
    scores=db.relationship("Scores",cascade="all,delete",backref="quiz",lazy=True)

#entity 5
class Option(db.Model):
    __tablename__ = "option"
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)
    option1=db.Column(db.String,nullable=False)
    option2=db.Column(db.String,nullable=False)
    option3=db.Column(db.String,nullable=False)
    option4=db.Column(db.String,nullable=False)
    

class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True)
    qid = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)
    qs_stmt = db.Column(db.String, nullable=False)
    answer = db.Column(db.String, nullable=False)
    marks=db.Column(db.Integer, nullable=False)
    options = db.relationship("Option", backref="question", cascade="all, delete-orphan")

#entity 6
class Scores(db.Model):
    __tablename__="scores"
    id=db.Column(db.Integer,primary_key=True)
    qid=db.Column(db.Integer,db.ForeignKey("quiz.id"),nullable=False)
    uid=db.Column(db.Integer,db.ForeignKey("user_info.id"),nullable=False)
    time=db.Column(db.DateTime,nullable=False)
    score=db.Column(db.Integer,nullable=False)
    