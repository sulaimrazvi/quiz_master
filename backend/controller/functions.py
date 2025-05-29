from backend.models import *

#GET FUNCTIONS---------------------------------------------------------------------
#___________________________________________SUBJECT________________________________________________________
def get_subject(id):
    subject = Subjects.query.filter(Subjects.id == id).first()
    return subject

def get_subjects():
    subjects=Subjects.query.all()
    return subjects
#___________________________________________CHAPTER________________________________________________________
def get_chapter(id):
    chapter = Chapter.query.filter(Chapter.id == id).first()
    return chapter
#___________________________________________QUIZ________________________________________________________

def get_quizs():
    quizs=Quiz.query.all()
    return quizs

def get_quiz(id):
    quiz = Quiz.query.filter(Quiz.id == id).first()
    return quiz
#___________________________________________QUESTIONS________________________________________________________
def get_question(id):
    qs = Question.query.filter(Question.id == id).first()
    return qs
#___________________________________________OPTIONS________________________________________________________
def get_options(question_id):
    options = Option.query.filter(Option.question_id == question_id).first()
    return options
#___________________________________________USER________________________________________________________
def get_user(id):
    u = User_info.query.filter(User_info.id == id).first()
    return u

def get_users():
    u=User_info.query.filter(User_info.role != 0).all()
    return u
#___________________________________________SCORE________________________________________________________
def get_score():
    s=Scores.query.all()
    return s

def get_scores(id):
    s = Scores.query.filter(Scores.id == id).first()
    return s

#SEARCH FUNCTIONS  -----------------------------------------------------------------

def search_by_quiz(search):
    quiz=Quiz.query.filter(Quiz.name.ilike(f"%{search}%")).all()
    return quiz

def search_by_user(search):
    return User_info.query.filter(User_info.full_name.ilike(f"%{search}%")).filter(User_info.role != 0).all()

def search_by_name(search_txt):
    subjects=Subjects.query.filter(Subjects.name.ilike(f"%{search_txt}%")).all()
    return subjects

def search_by_cname(search_txt):
    chapters=Chapter.query.filter(Chapter.name.ilike(f"%{search_txt}%")).all()
    return chapters