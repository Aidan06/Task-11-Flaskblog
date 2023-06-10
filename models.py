from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))

    def __init__(self, title, content, blog_id):
        self.title = title
        self.content = content
        self.blog_id = blog_id


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    content = db.Column(db.Text)

    def __init__(self, post_id, content):
        self.post_id = post_id
        self.content = content


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    posts = db.relationship('Post', backref='blog', lazy=True)

    def __init__(self, name):
        self.name = name


db.create_all()
