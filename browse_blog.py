from flask import Flask, g, render_template, request
import os
from blog_db import BlogDatabase

app = Flask(__name__)

app.config['DATABASE'] = os.path.join(app.root_path, 'blog.sqlite')


def get_db():
    """
    Returns a connection to the database through the class BlogDatabase. If
    one does not exist, a new connection or database is created.
    """

    if not hasattr(g, 'blogs_db'):
        g.blogs_db = BlogDatabase(app.config['DATABASE'])

    return g.blogs_db


@app.route('/')
def home():
    """
    Serves the homepage of the blog.
    """
    return render_template('home.html')


@app.route('/entries')
def all_entries():
    """
    Serves a page which shows all entry titles of the blog.
    """
    return render_template('entries.html', entries=get_db().get_all_entries())


@app.route('/new', methods=['GET', 'POST'])
def add_entry():
    """
    Serves a page which allows users to add new entries into the blog.
    """
    begin = False
    successful_add = None
    notice_text = None
    if ('title' in request.form and 'content' in request.form and
            'author' in request.form and 'topic' in request.form):

        begin = True
        max_length = 100
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        topic = request.form['topic']

        for parameter in (title, content, author, topic):
            if parameter == '':
                successful_add = False
                notice_text = "There's a missing parameter"
                break

            elif len(parameter) > max_length:
                successful_add = False
                notice_text = 'All inputs must be under 100 characters'
                break

            else:
                successful_add = True

        if successful_add:
            notice_text = 'Entry added successfully!'
            get_db().insert_entry(title, content, author, topic)

    return render_template('post_entry.html', begin=begin,
                           successful_add=successful_add,
                           notice_text=notice_text)


@app.route('/entries/<entry_id>')
def entry(entry_id):
    """
    Serves a page which shows a single entry in detail.
    """
    get_entry = get_db().get_entry_by_id(entry_id)
    title = get_entry['title']
    content = get_entry['content']
    author = get_entry['author']
    topic = get_entry['topic']
    return render_template('entry_template.html', title=title, content=content,
                           author=author, topic=topic)


@app.route('/authors')
def authors():
    """
    Serves a page which shows all authors of the blog.
    """
    return render_template('authors.html', authors=get_db().get_all_authors())


@app.route('/topics')
def topics():
    """
    Serves a page which shows all topics of the blog.
    """
    return render_template('topics.html', topics=get_db().get_all_topics())


if __name__ == '__main__':
    app.run(debug=True)
