from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_required, login_user
from os import environ

from forms import LoginForm
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
login_manager.init_app(app)
login_manager.login_view = 'login'




class Article(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    intro = db.Column(db.String(300), nullable = True)
    text = db.Column(db.Text, nullable = False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def  __repr__(self):
        return '<Article %r>' % self.id


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


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
@login_required
def post_delete(id):
    articles = Article.query.get_or_404(id)

    try:
        db.session.delete(articles)
        db.session.commit()
        return redirect('/posts')
    except:
        return 'Error'


@app.route('/posts/<int:id>/update', methods = ['GET', 'POST'])
@login_required
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
@login_required
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)
        if len(title) > 2 and len(intro) > 10 and len(text) > 15:
            try:
                db.session.add(article)
                db.session.commit()
                flash("Creating was successfull!", "success")
                return render_template("create_article.html")
            except:
                flash("An error occurred during creating. Please try again", "error")
                return render_template("create_article.html")
        else:
            flash("The article should contain more characters", "error")
            return render_template("create_article.html")
    else:
        return render_template("create_article.html")


@app.route('/sign_up', methods=['post', 'get'])
def sign_up():
    if request.method == "POST":
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        user = User(name=name, username=username, email=email)
        user.set_password(password)
        
        if (user.username,) not in db.session.query(User.username).all() and (user.email,) not in db.session.query(User.email).all():
            try:
                db.session.add(user)
                db.session.commit()
                return redirect('/login')
            except:
                flash("An error occurred during registration. Perhaps such a login is already in use", "error")
                return render_template("sign_up.html")
        else:
            flash("A user with this username or email already exists", "error")
            return render_template("sign_up.html")
    else:
        return render_template("sign_up.html")



@app.route('/login/', methods=['post',  'get'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('admin'))
    
        flash("Invalid username/password", 'error')
        return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/profile/')
@login_required
def admin():
    return render_template('profile.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


if __name__ == "__main__":
    port = int(environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
