import os
import sqlite3


def row_to_dict(cur):
    """
    A row is fetched. Returns None if there is no row to fetch, otherwise
    returns a dictionary representation of the row.

    :param cur: a cursor
    :return: None if no row, otherwise a dict representation of the row
    """
    row = cur.fetchone()
    if row is None:
        return None
    else:
        return dict(row)


class BlogDatabase:
    """
    This class provides methods for getting, inserting, and deleting data from
    the blog's database.
    """

    def __init__(self, sqlite_filename):
        """
        Creates a connection to the database. If the database file does not
        exist, creates a new database object and its tables.

        :param sqlite_filename: the name of the SQLite database file
        """
        if os.path.isfile(sqlite_filename):
            create_tables = False
        else:
            create_tables = True

        self.conn = sqlite3.connect(sqlite_filename)
        self.conn.row_factory = sqlite3.Row

        cur = self.conn.cursor()
        cur.execute('PRAGMA foreign_keys = 1')
        cur.execute('PRAGMA journal_mode = WAL')
        cur.execute('PRAGMA synchronous = NORMAL')

        if create_tables:
            self.create_tables()

    def create_tables(self):
        """
        Create the tables topic, author and entry.
        """
        cur = self.conn.cursor()
        cur.execute('CREATE TABLE topic(topic_id INTEGER PRIMARY KEY, '
                    '    topic TEXT UNIQUE)')
        cur.execute('CREATE TABLE author(author_id INTEGER PRIMARY KEY, '
                    '    name TEXT UNIQUE)')
        cur.execute('CREATE TABLE entry(entry_id INTEGER PRIMARY KEY, '
                    '    title TEXT, content TEXT, '
                    '    author_id INTEGER, topic_id INTEGER, '
                    '    FOREIGN KEY (author_id) REFERENCES '
                    '    author(author_id), '
                    '    FOREIGN KEY (topic_id) REFERENCES topic(topic_id))')
        self.conn.commit()

    def insert_topic(self, topic):
        """
        Inserts a topic into the database. Ignores if topic already exists.
        Returns a dictionary representation of the topic.

        :param topic: name of the topic

        :return: a dict representing the topic
        """
        cur = self.conn.cursor()
        query = 'INSERT OR IGNORE INTO topic(topic) VALUES(?)'
        cur.execute(query, (topic,))
        self.conn.commit()
        return self.get_topic_by_name(topic)

    def get_all_topics(self):
        """
        Return a list of dictionaries representing all of the topics in the
        database.

        :return: a list of dict representing topics
        """
        cur = self.conn.cursor()
        query = 'SELECT * FROM topic'
        topics = []
        cur.execute(query)

        for row in cur.fetchall():
            topics.append(dict(row))
        return topics

    def get_topic_by_id(self, topic_id):
        """
        Get a dictionary representation of the topic with the given id.
        Returns None if topic does not exist.

        :param topic_id: primary key of the topic
        :return: a dict representing the topic, or None
        """
        cur = self.conn.cursor()
        query = 'SELECT topic_id, topic FROM topic WHERE topic_id = ?'
        cur.execute(query, (topic_id,))
        return row_to_dict(cur)

    def get_topic_by_name(self, topic_name):
        """
        Get a dictionary representation of the topic with the given name.
        Return None if topic does not exist.

        :param topic_name: name of the topic
        :return: a dict representing the topic, or None
        """
        cur = self.conn.cursor()
        query = 'SELECT topic_id, topic FROM topic WHERE topic = ?'
        cur.execute(query, (topic_name,))
        return row_to_dict(cur)

    def delete_topic(self, topic_id):
        """
        Delete the topic with the given id.

        :param topic_id: primary key of the topic
        """
        cur = self.conn.cursor()
        query = 'DELETE FROM topic WHERE topic_id = ?'
        cur.execute(query, (topic_id,))
        self.conn.commit()

    def insert_author(self, name):
        """
        Inserts an author into the database. Ignores if author already exists.
        Returns a dictionary representation of the author.

        :param name: name of the author

        :return: a dict representing the author
        """
        cur = self.conn.cursor()
        query = 'INSERT OR IGNORE INTO author(name) VALUES(?)'
        cur.execute(query, (name,))
        self.conn.commit()
        return self.get_author_by_name(name)

    def get_all_authors(self):
        """
        Return a list of dictionaries representing all of the authors in the
        database.

        :return: a list of dict representing authors
        """
        cur = self.conn.cursor()
        query = 'SELECT * FROM author'
        authors = []
        cur.execute(query)

        for row in cur.fetchall():
            authors.append(dict(row))

        return authors

    def get_author_by_id(self, author_id):
        """
        Get a dictionary representation of the author with the given id.
        Returns None if the author does not exist.

        :param author_id: primary key of the author
        :return: a dict representing the author, or None
        """
        cur = self.conn.cursor()
        query = 'SELECT author_id, name FROM author WHERE author_id = ?'
        cur.execute(query, (author_id,))
        return row_to_dict(cur)

    def get_author_by_name(self, name):
        """
        Get a dictionary representation of the author with the given name.
        Returns None if author does not exist.

        :param name: name of the author
        :return: a dict representing the author, or None
        """
        cur = self.conn.cursor()
        query = 'SELECT author_id, name FROM author WHERE name = ?'
        cur.execute(query, (name,))
        return row_to_dict(cur)

    def delete_author(self, author_id):
        """
        Delete the author with the given id.

        :param author_id: primary key of the author
        """
        cur = self.conn.cursor()
        query = 'DELETE FROM author WHERE author_id = ?'
        cur.execute(query, (author_id,))
        self.conn.commit()

    def insert_entry(self, title, content, author, topic):
        """
        Inserts an entry into the database. Ignores if entry already exists.
        Returns a dictionary representation of the entry.

        :param title: name of the entry
        :param content: content of entry
        :param author: author of the entry
        :param topic: topic of the entry

        :return: a dict representing the entry
        """
        cur = self.conn.cursor()
        self.insert_author(author)
        author_dict = self.get_author_by_name(author)
        author_id = author_dict['author_id']

        self.insert_topic(topic)
        topic_dict = self.get_topic_by_name(topic)
        topic_id = topic_dict['topic_id']

        query = ('INSERT INTO entry(title, content, author_id, topic_id) '
                 'VALUES(?, ?, ?, ?)')

        cur.execute(query, (title, content, author_id, topic_id,))
        self.conn.commit()

        return self.get_entry_by_id(cur.lastrowid)

    def get_all_entries(self):
        """
        Return a list of dictionaries representing all of the entries in the
        database.

        :return: a list of dict representing entries
        """
        cur = self.conn.cursor()
        query = ('SELECT entry.entry_id as entry_id, entry.title as title, '
                 'entry.content as content, author.name as author, '
                 'author.author_id as author_id, topic.topic as topic, '
                 'topic.topic_id as topic_id '
                 'FROM entry, author, topic '
                 'WHERE author.author_id = entry.author_id '
                 'AND topic.topic_id = entry.topic_id')
        entries = []
        cur.execute(query)

        for row in cur.fetchall():
            entries.append(dict(row))

        return entries

    def get_entry_by_id(self, entry_id):
        """
        Get a dictionary representation of the entry with the given id.
        Returns None if entry does not exist.

        :param entry_id: primary key of the entry
        :return: a dict representing the entry, or None
        """
        cur = self.conn.cursor()
        query = ('SELECT entry.entry_id as entry_id, entry.title as title, '
                 'entry.content as content, author.name as author, '
                 'author.author_id as author_id, topic.topic as topic, '
                 'topic.topic_id as topic_id '
                 'FROM entry, author, topic '
                 'WHERE author.author_id = entry.author_id '
                 'AND topic.topic_id = entry.topic_id '
                 'AND entry_id = ?')
        cur.execute(query, (entry_id,))
        return row_to_dict(cur)

    def delete_entry(self, entry_id):
        """
        Delete the entry with the given id.

        :param entry_id: primary key of the entry
        """
        cur = self.conn.cursor()
        query = 'DELETE FROM entry WHERE entry_id = ?'
        cur.execute(query, (entry_id,))
        self.conn.commit()


if __name__ == '__main__':
    db = BlogDatabase('blog.sqlite')
    db.insert_author('Karen')
    db.insert_topic('Thoughts')
    db.insert_topic('Stuff')
    db.get_topic_by_id(2)
    db.insert_author('Sam')
    db.insert_author('Nathan')
    content = 'Hi how are you'
    db.insert_entry('Hi', content, 'Karen', 'Thoughts')
    db.get_entry_by_id(1)
    content2 = 'Hello how are you'
    db.insert_entry('Hello', content2, 'Sam', 'Stuff')
