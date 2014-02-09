from flask import Flask
from flask import g
from flask import render_template
from flask import abort
from flask import request
from flask import url_for
from flask import redirect

from flask import session
from flask import flash

import sqlite3
from contextlib import closing

app = Flask(__name__)
app.config.from_pyfile('microblog.cfg')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You are logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_database_connection():
    db = getattr(g, 'db', None)
    if db is None:
        g.db = db = connect_db()
    return db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def write_entry(title, text):
    con = get_database_connection()
    con.execute('insert into entries (title, text) values (?, ?)',
                [title, text])
    con.commit()
    flash('New entry was successfully posted')

def get_all_entries():
    con = get_database_connection()
    cur = con.execute('SELECT title, text FROM entries ORDER BY id DESC')
    return [dict(title=row[0], text=row[1]) for row in cur.fetchall()]

@app.route('/')
def show_entries():
    entries = get_all_entries()
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    
    elif not request.form['title'] or not request.form['text']:
        flash('Entry needs a title and text')

    else:
        try:
            write_entry(request.form['title'], request.form['text'])
        except sqlite3.Error as e:
            flash('Error creating entry:  %s' % str(e))
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run(debug=True)
