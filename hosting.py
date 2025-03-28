import argparse
from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__, static_url_path = '/static')

DATABASE = 'form_data.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Access columns by name
    return db

@app.teardown_appcontext
def close_db(error):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.route('/', methods=['GET', 'POST'])
def handle_form():
    template_name = app.config.get('TEMPLATE_NAME')
    if not template_name:
        return "No template name provided. Please run the script with the --template argument.", 400

    if request.method == 'POST':
        data = request.form.to_dict()
        try:
            db = get_db()
            cursor = db.cursor()
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?'] * len(data))
            sql = f"INSERT INTO form_submissions ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, list(data.values()))
            db.commit()
            return render_template('success.html', data=data)  # Create a success template
        except sqlite3.Error as e:
            return f"Database error: {e}", 500
    else:
        try:
            return render_template(template_name)
        except Exception as e:
            return f"{e}", 500

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run a Flask app with a specified template and form handling.')
    parser.add_argument('--template', type=str, required=True, help='The name of the HTML form template file (e.g., form.html).')
    args = parser.parse_args()

    app.config['TEMPLATE_NAME'] = args.template
    app.run(debug=True)