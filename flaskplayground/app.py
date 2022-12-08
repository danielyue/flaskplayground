from flask import Flask, render_template, request, url_for, flash, redirect
import mysql.connector
from werkzeug.exceptions import abort
import os
import json

with open('secrets.json') as f:
    secrets = json.load(f)


def get_db_connection():
    db = mysql.connector.connect(
        host=secrets['HOST'],
        user=secrets['USER'],
        password=secrets['PASSWORD'],
        database='flask_playground'
    )
    cur = db.cursor(dictionary=True)

    return({
        'db': db,
        'cur': cur
    })

def get_post(post_id):
    conn = get_db_connection()
    conn['cur'].execute("SELECT * FROM posts where id = %s", (post_id,))
    post = conn['cur'].fetchone()
    conn['db'].close()

    if post is None:
        abort(404)

    return post


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets['SECRETKEY']


@app.route('/')
def index():
    conn = get_db_connection()
    conn['cur'].execute("SELECT * FROM posts")
    posts = conn['cur'].fetchall()
    conn['db'].close()

    return render_template('index.html', posts=posts)

@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)

    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            insert_stmt = "INSERT INTO posts (title, content) VALUES (%s, %s)"
            conn['cur'].execute(insert_stmt, (title, content))
            conn['db'].commit()
            conn['db'].close()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            update_stmt = "UPDATE posts SET title = %s, content = %s WHERE id = %s;"
            conn['cur'].execute(update_stmt, (title, content, id))
            conn['db'].commit()
            conn['db'].close()
            conn = get_db_connection()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn['cur'].execute('DELETE FROM posts WHERE id=%s',(id,))
    conn['db'].commit()
    conn['db'].close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
