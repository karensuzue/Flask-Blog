from flask import Flask, g, jsonify, request
from flask.views import MethodView
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


class RequestError(Exception):
    """
    This class handles errors in requests.
    """
    def __init__(self, status_code, error_message):
        super().__init__(self)

        self.status_code = status_code
        self.error_message = error_message

    def to_response(self):
        """
        Create a Response object containing the error message as JSON.

        :return: the response
        """

        response = jsonify({'error': self.error_message})
        response.status = self.status_code
        return response


@app.errorhandler(RequestError)
def handle_invalid_usage(error):
    """
    Returns a JSON response built from a RequestError.

    :param error: the RequestError
    :return: a response containing the error message
    """
    return error.to_response()


class EntriesView(MethodView):
    """
    This view handles all the /entries requests.
    """

    def get(self, entry_id):
        """
        Handles GET requests. Returns a JSON representation of all entries if
        entry_id is None, otherwise returns a JSON representation of a single
        entry.

        :param entry_id: primary key of entry
        :return: JSON response
        """
        if entry_id is None:
            return jsonify(get_db().get_all_entries())
        else:
            entry = get_db().get_entry_by_id(entry_id)
            if entry is not None:
                response = jsonify(entry)
            else:
                raise RequestError(404, 'entry not found')

            return response

    def post(self):
        """
        Implements POST /entries. Requires form parameters 'title', 'content',
        'author', and 'topic'.

        :return: JSON response representing the new entry.
        """
        for parameter in ('title', 'content', 'author', 'topic'):
            if parameter not in request.form:
                error = 'parameter {} required'.format(parameter)
                raise RequestError(422, error)

        entry = get_db().insert_entry(request.form['title'],
                                      request.form['content'],
                                      request.form['author'],
                                      request.form['topic'])
        return jsonify(entry)

    def delete(self, entry_id):
        """
        Handle DELETE requests. The entry_id must be provided.

        :param entry_id: id of an entry
        :return: JSON response containing a message
        """
        if get_db().get_entry_by_id(entry_id) is None:
            raise RequestError(404, 'entry not found')

        get_db().delete_entry(entry_id)

        return jsonify({'message': 'entry deleted successfully'})


class AuthorsView(MethodView):
    """
    This view handles all the /authors requests.
    """

    def get(self, author_id):
        """
        Handles GET requests. Returns a JSON representation of all authors if
        author_id is None, otherwise returns a JSON representation of a single
        author.

        :param author_id: primary key of author
        :return: JSON response
        """
        if author_id is None:
            return jsonify(get_db().get_all_authors())

        else:
            author = get_db().get_author_by_id(author_id)
            if author is not None:
                response = jsonify(author)
            else:
                raise RequestError(404, 'author not found')

            return response

    def post(self):
        """
        Implements POST /authors. Requires form parameter 'name'.

        :return: JSON response representing the new author.
        """
        if 'name' not in request.form:
            raise RequestError(422, 'author name required')

        else:
            author = get_db().insert_author(request.form['name'])
            return jsonify(author)

    def delete(self, author_id):
        """
        Handle DELETE requests. The author_id must be provided.

        :param author_id: id of an author
        :return: JSON response containing a message
        """
        if get_db().get_author_by_id(author_id) is None:
            raise RequestError(404, 'author not found')

        get_db().delete_author(author_id)

        return jsonify({'message': 'author deleted successfully'})


class TopicsView(MethodView):
    """
    This view handles all the /topics requests.
    """

    def get(self, topic_id):
        """
        Handles GET requests. Returns a JSON representation of all topics if
        topic_id is None, otherwise returns a JSON representation of a single
        topic.

        :param topic_id: primary key of topic
        :return: JSON response
        """
        if topic_id is None:
            return jsonify(get_db().get_all_topics())

        else:
            topic = get_db().get_topic_by_id(topic_id)
            if topic is not None:
                return jsonify(topic)
            else:
                raise RequestError(404, 'topic not found')

    def post(self):
        """
        Implements POST /topics. Requires form parameter 'topic'.

        :return: JSON response representing the new topic.
        """
        if 'topic' not in request.form:
            raise RequestError(422, 'topic name required')

        else:
            topic = get_db().insert_topic(request.form['topic'])
            return jsonify(topic)

    def delete(self, topic_id):
        """
        Handle DELETE requests. The topic_id must be provided.

        :param topic_id: id of a topic
        :return: JSON response containing a message
        """
        if get_db().get_topic_by_id(topic_id) is None:
            raise RequestError(404, 'topic not found')

        get_db().delete_topic(topic_id)

        return jsonify({'message': 'topic deleted successfully'})


entries_view = EntriesView.as_view('entries_view')
app.add_url_rule('/entries', defaults={'entry_id': None},
                 view_func=entries_view, methods=['GET'])
app.add_url_rule('/entries', view_func=entries_view, methods=['POST'])
app.add_url_rule('/entries/<int:entry_id>', view_func=entries_view,
                 methods=['GET', 'DELETE'])

authors_view = AuthorsView.as_view('authors_view')
app.add_url_rule('/authors', defaults={'author_id': None},
                 view_func=authors_view, methods=['GET'])
app.add_url_rule('/authors', view_func=authors_view, methods=['POST'])
app.add_url_rule('/authors/<int:author_id>', view_func=authors_view,
                 methods=['GET', 'DELETE'])

topics_view = TopicsView.as_view('topics_view')
app.add_url_rule('/topics', defaults={'topic_id': None},
                 view_func=topics_view, methods={'GET'})
app.add_url_rule('/topics', view_func=topics_view, methods=['POST'])
app.add_url_rule('/topics/<int:topic_id>', view_func=topics_view,
                 methods=['GET', 'DELETE'])

if __name__ == '__main__':
    app.run(debug=True)
