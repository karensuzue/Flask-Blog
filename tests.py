"""
The tests are placed in order of what is tested first. Test functions
occasionally incorporate the ones above it.
"""

from blog_db import BlogDatabase


def path_builder(directory):
    """
    Given a directory, construct a path to a file named test.sqlite. Returns
    a path to the file.
    """
    return directory / 'tests.sqlite'


def test_init(tmp_path):
    """
    Test the BlogDatabase initializer.
    :param tmp_path: Path object for a temporary directory, a pytest fixture.
    """
    BlogDatabase(path_builder(tmp_path))


def test_insert_entry(tmp_path):
    """
    Tests insert_entry() runs without errors, and that a dictionary
    representation is returned.
    """
    db = BlogDatabase(path_builder(tmp_path))
    content = ':)'
    content2 = ':('

    blog = db.insert_entry('Hello', content, 'Karen', 'Thoughts')
    assert blog['title'] == 'Hello'
    assert blog['content'] == content
    assert blog['author'] == 'Karen'
    assert blog['topic'] == 'Thoughts'

    blog2 = db.insert_entry('Hi', content2, 'Karen', 'Thoughts')
    assert blog2['title'] == 'Hi'
    assert blog2['content'] == content2
    assert blog2['author'] == 'Karen'
    assert blog2['topic'] == 'Thoughts'


def test_insert_author(tmp_path):
    """
    Tests insert_author() runs without errors, and that a dictionary
    representation is returned.
    """
    db = BlogDatabase(path_builder(tmp_path))
    author = db.insert_author('Sam')
    assert author['name'] == 'Sam'

    author2 = db.insert_author('Karen')
    assert author2['name'] == 'Karen'


def test_insert_topic(tmp_path):
    """
    Tests insert_topic() runs without errors, and that a dictionary
    representation is returned.
    """
    db = BlogDatabase(path_builder(tmp_path))
    topic = db.insert_topic('Stuff')
    assert topic['topic'] == 'Stuff'

    topic2 = db.insert_topic('Thoughts')
    assert topic2['topic'] == 'Thoughts'


def test_get_entry_by_id(tmp_path):
    """
    Test that get_entry_by_id() runs without errors. Makes sure that it returns
    None when it should, and properly returns an entry when there's an entry
    in the database.
    """
    db = BlogDatabase(path_builder(tmp_path))
    assert db.get_entry_by_id(1) is None

    content = ':('
    inserted_entry = db.insert_entry('Hi', content, 'Karen', 'Thoughts')
    get_entry = db.get_entry_by_id(1)

    assert inserted_entry == get_entry


def test_get_author_by_name(tmp_path):
    """
    Test that get_author_by_name() runs without errors. Makes sure that it
    returns None when it should, and properly returns an author when there's
    an author in the database.
    """
    db = BlogDatabase(path_builder(tmp_path))
    assert db.get_author_by_name('Karen') is None

    inserted_author = db.insert_author('Karen')
    get_author = db.get_author_by_name('Karen')
    assert inserted_author == get_author


def test_get_author_by_id(tmp_path):
    """
    Test that get_author_by_id() runs without errors. Makes sure that it
    returns None when it should, and properly returns an author when there's
    an author in the database.
    """
    db = BlogDatabase(path_builder(tmp_path))
    assert db.get_author_by_id(1) is None

    inserted_author = db.insert_author('Karen')
    get_author = db.get_author_by_id(1)
    assert inserted_author == get_author


def test_get_topic_by_name(tmp_path):
    """
    Test that get_topic_by_name() runs without errors. Makes sure that it
    returns None when it should, and properly returns a topic when there's
    a topic in the database.
    """
    db = BlogDatabase(path_builder(tmp_path))
    assert db.get_topic_by_name('Thoughts') is None

    inserted_topic = db.insert_topic('Thoughts')
    get_topic = db.get_topic_by_name('Thoughts')
    assert inserted_topic == get_topic


def test_get_topic_by_id(tmp_path):
    """
    Test that get_topic_by_id() runs without errors. Makes sure that it returns
    None when it should, and properly returns a topic when there's a topic
    in the database.
    """
    db = BlogDatabase(path_builder(tmp_path))
    assert db.get_topic_by_id(1) is None

    inserted_topic = db.insert_topic('Thoughts')
    get_topic = db.get_topic_by_id(1)
    assert inserted_topic == get_topic


def test_delete_entry(tmp_path):
    """
    Tests that delete_entry() properly removes an entry from the database.
    """
    db = BlogDatabase(path_builder(tmp_path))
    content = ':)'
    db.insert_entry('Hi', content, 'Karen', 'Thoughts')
    assert db.get_entry_by_id(1) == {'entry_id': 1, 'title': 'Hi',
                                     'content': content, 'author': 'Karen',
                                     'author_id': 1, 'topic': 'Thoughts',
                                     'topic_id': 1}
    db.delete_entry(1)
    assert db.get_entry_by_id(1) is None


def test_delete_author(tmp_path):
    """
    Tests that delete_author() properly removes an author from the database.
    """
    db = BlogDatabase(path_builder(tmp_path))
    db.insert_author('Karen')
    assert db.get_author_by_id(1) == {'author_id': 1, 'name': 'Karen'}
    db.delete_author(1)
    assert db.get_author_by_id(1) is None


def test_delete_topic(tmp_path):
    """
    Tests that delete_topic() properly removes a topic from the database.
    """
    db = BlogDatabase(path_builder(tmp_path))
    db.insert_topic('Thoughts')
    assert db.get_topic_by_id(1) == {'topic_id': 1, 'topic': 'Thoughts'}
    db.delete_topic(1)
    assert db.get_topic_by_id(1) is None


def test_get_all_entries(tmp_path):
    """
    Tests that get_all_entries() returns the right amount of entries and the
    right information for each entry.
    """
    db = BlogDatabase(path_builder(tmp_path))
    assert db.get_all_entries() == []

    content = 'Hi how are you'
    db.insert_entry('Hi', content, 'Karen', 'Thoughts')

    entry_list = db.get_all_entries()
    assert len(entry_list) == 1
    assert entry_list[0]['title'] == 'Hi'
    assert entry_list[0]['content'] == content
    assert entry_list[0]['author'] == 'Karen'
    assert entry_list[0]['author_id'] == 1
    assert entry_list[0]['topic'] == 'Thoughts'
    assert entry_list[0]['topic_id'] == 1

    content2 = 'something??'
    db.insert_entry('Hello', content2, 'Karen', 'Stuff')
    assert len(db.get_all_entries()) == 2

    db.delete_entry(1)
    assert len(db.get_all_entries()) == 1


def test_get_all_authors(tmp_path):
    """
    Tests that get_all_authors() returns the right amount of authors and the
    right information for each author.
    """
    db = BlogDatabase(path_builder(tmp_path))
    assert db.get_all_authors() == []

    db.insert_author('Karen')
    author_list = db.get_all_authors()
    assert len(author_list) == 1
    assert author_list[0]['name'] == 'Karen'

    db.insert_author('Sam')
    author_list2 = db.get_all_authors()
    assert len(author_list2) == 2
    assert author_list2[1]['name'] == 'Sam'

    db.delete_author(1)
    assert len(db.get_all_authors()) == 1
    assert db.get_all_authors() == [{'author_id': 2, 'name': 'Sam'}]


def test_get_all_topics(tmp_path):
    """
    Tests that get_all_topics() returns the right amount of topics and the
    right information for each topic.
    """
    db = BlogDatabase(path_builder(tmp_path))
    assert db.get_all_topics() == []

    db.insert_topic('Stuff')
    topic_list = db.get_all_topics()
    assert len(topic_list) == 1
    assert topic_list[0]['topic'] == 'Stuff'

    db.insert_topic('Thoughts')
    topic_list2 = db.get_all_topics()
    assert len(topic_list2) == 2
    assert topic_list2[1]['topic'] == 'Thoughts'

    db.delete_topic(1)
    assert len(db.get_all_topics()) == 1
    assert db.get_all_topics() == [{'topic_id': 2, 'topic': 'Thoughts'}]
