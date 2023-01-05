from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, current_user
from datetime import datetime
from config import Config
from werkzeug.security import generate_password_hash,  check_password_hash


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    app.config.from_pyfile('config_extended.py')

    return app


app = create_app()
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    intro = db.Column(db.String(300), nullable = True)
    text = db.Column(db.Text, nullable = False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def  __repr__(self):
        return '<Article %r>' % self.id


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow,  onupdate=datetime.utcnow)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,  password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
@app.route('/welcome', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return render_template('home.html')
    else:
        return render_template("welcome.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles = articles)


@app.route('/posts/<int:id>')
def post_details(id):
    articles = Article.query.get(id)
    return render_template("post_detail.html", articles = articles)


@app.route('/posts/<int:id>/delete', methods = ['GET', 'POST'])
def post_delete(id):
    articles = Article.query.get_or_404(id)

    try:
        db.session.delete(articles)
        db.session.commit()
        return redirect('/posts')
    except:
        return 'Error'


@app.route('/posts/<int:id>/update', methods = ['GET', 'POST'])
def post_update(id):
    articles = Article.query.get_or_404(id)
    if request.method == 'POST':
        articles.title = request.form['title']
        articles.intro = request.form['intro']
        articles.text = request.form['text'] 

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "Error"
    else:
        return render_template('post_update.html', articles=articles)



@app.route('/create_article', methods = ['GET', 'POST'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/home')
        except:
            return 'Error'
    else:
        return render_template("create_article.html")


@app.route('/profile')
def profile(id):
    user = User.query.get(id)
    return render_template("profile.html", user=user)


@app.route('/sign-up', methods = ['GET', 'POST'])
def create_account():
    if request.method == "POST":
        name = request.form.get('username')
        password = request.form.get('password')
        username = request.form.get('user_login')
        email = request.form.get('email')
        password_hash = generate_password_hash(password)
        
        user = User(name=username, username=username, email=email)
        user.set_password(password)

        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/home')
        except:
            return "Error with db.commit()"
    else:
        return render_template("sign_up.html")


# @app.route('/sign-p', methods = ['GET', 'POST'])
# def create_account():
#     if request.method == "POST":
#         user_login = request.form.get('user_login')
#         password = request.form.get('password')
#         remember = request.form.get('remember')
        
#     else:
#         return render_template("sign_up.html")


if __name__ == "__main__":
    app.run(debug=True)