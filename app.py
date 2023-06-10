from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from utils import create_app, init_app

from models import Post, Comment, db

app = create_app()
init_app(app)


@app.route('/')
def index():
    with open('index.html') as file:
        return file.read()


@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    title = data['title']
    content = data['content']
    blog_id = data['blog_id']

    post = Post(title=title, content=content, blog_id=blog_id)

    db.session.add(post)
    db.session.commit()

    return jsonify({'message': 'Post created successfully'})


@app.route('/posts')
def get_all_posts():
    posts = Post.query.all()
    result = []

    for post in posts:
        result.append({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'blog_id': post.blog_id
        })

    return jsonify(result)


@app.route('/posts/<int:post_id>')
def get_post(post_id):
    post = Post.query.get(post_id)

    if post:
        return jsonify({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'blog_id': post.blog_id
        })
    else:
        return jsonify({'message': 'Post not found'})


@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = Post.query.get(post_id)

    if post:
        data = request.get_json()
        post.title = data['title']
        post.content = data['content']
        db.session.commit()

        return jsonify({'message': 'Post updated successfully'})
    else:
        return jsonify({'message': 'Post not found'})


@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get(post_id)

    if post:
        db.session.delete(post)
        db.session.commit()

        return jsonify({'message': 'Post deleted successfully'})
    else:
        return jsonify({'message': 'Post not found'})


@app.route('/posts/<int:post_id>/comments', methods=['POST'])
def create_comment(post_id):
    post = Post.query.get(post_id)

    if post:
        data = request.get_json()
        content = data['content']

        comment = Comment(post_id=post.id, content=content)
        db.session.add(comment)
        db.session.commit()

        return jsonify({'message': 'Comment created successfully'})
    else:
        return jsonify({'message': 'Post not found'})


@app.route('/posts/<int:post_id>/comments')
def get_all_comments(post_id):
    post = Post.query.get(post_id)

    if post:
        comments = Comment.query.filter_by(post_id=post.id).all()
        result = []

        for comment in comments:
            result.append({
                'id': comment.id,
                'post_id': comment.post_id,
                'content': comment.content
            })

        return jsonify(result)
    else:
        return jsonify({'message': 'Post not found'})


@app.route('/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)

    if comment:
        db.session.delete(comment)
        db.session.commit()

        return jsonify({'message': 'Comment deleted successfully'})
    else:
        return jsonify({'message': 'Comment not found'})


if __name__ == '__main__':
    app.run()


