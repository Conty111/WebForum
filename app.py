from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime



app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# manager = LoginManager(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    intro = db.Column(db.String(300), nullable = True)
    text = db.Column(db.Text, nullable = False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def  __repr__(self):
        return '<Article %r>' % self.id

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     login = db.Column(db.String(20), nullable = True)
#     password = db.Column(db.String(20), nullable = True)


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


if __name__ == "__main__":
    app.run(debug=True)