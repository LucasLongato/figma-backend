from flask import Flask
from models import db, bcrypt, login_manager
from models.user import User  # Import User model
from routes.user_routes import user_bp
from routes.task_routes import task_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

# Register Blueprints
app.register_blueprint(user_bp, url_prefix="/users")
app.register_blueprint(task_bp, url_prefix="/")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)