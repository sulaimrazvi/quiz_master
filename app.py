from flask import Flask, render_template
from backend.models import db, User_info  
from datetime import datetime

def setup_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'iitm'    
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///quiz_app.sqlite3"

    db.init_app(app)  # Initialize database
    app.app_context().push()

    return app

# Initialize the app
app = setup_app()

# Create database tables inside the app context
with app.app_context():
    db.create_all()  # Ensures tables are created

    # Ensure admin user exists
    if not User_info.query.filter_by(email="admin@gmail.com").first():
        admin_user = User_info(
            email="admin@gmail.com",
            password="1234",
            role=0,
            full_name="Administrator",
            qualification="Quiz Master",
            dob=datetime.strptime("14-08-2004", "%d-%m-%Y").date()
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created!")

# Import controllers *after* app is initialized
import backend.controller.login_signup  
import backend.controller.admin_dashboard  
import backend.controller.admin_quiz  
import backend.controller.functions  
import backend.controller.summary  
import backend.controller.user_dashboard  

if __name__ == "__main__":
    app.run(debug=True)
