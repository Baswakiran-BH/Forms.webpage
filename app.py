from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps  # <-- Import this

app = Flask(__name__)
# Make this unique for your club project
app.config['SECRET_KEY'] = 'my_clubs_very_secret_key_9876'


# --- NEW: The Login Required Decorator ---
def login_required(f):
    """
    A decorator to check if a user is logged in.
    If not, it redirects them to the login page.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('You must be logged in to view this page.', 'error')
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)

    return decorated_function


# ----------------------------------------


# --- Public Routes (Anyone can see) ---

@app.route('/')
def index():
    username = session.get('username', None)
    return render_template('index.html', username=username)


@app.route('/login_page')
def login_page():
    return render_template('login.html')


@app.route('/submit_login', methods=['POST'])
def handle_login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Your unique login details
    if username == 'kiran' and password == 'kiranbh08':
        session['username'] = username
        flash(f'Hey {username}, great to see you!', 'success')
        return redirect(url_for('index'))
    else:
        flash('Whoops! Wrong login details. Try again.', 'error')
        return redirect(url_for('login_page'))


# --- Protected Routes (Login is REQUIRED) ---

@app.route('/logout')
@login_required  # <-- The user must be logged in to log out
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))


@app.route('/contact_page')
@login_required  # <-- Protected!
def contact_page():
    return render_template('contact.html')


@app.route('/submit_contact', methods=['POST'])
@login_required  # <-- Protected!
def handle_contact():
    email = request.form.get('email')
    message = request.form.get('message')

    print("--- NEW CONTACT MESSAGE ---")
    print(f"Email from {session['username']}: {email}")
    print(f"Message: {message}")
    print("---------------------------")

    flash('Thank you for your message!', 'success')
    return redirect(url_for('contact_page'))


@app.route('/search_page')
@login_required  # <-- Protected!
def search_page():
    return render_template('search.html')


@app.route('/submit_search', methods=['GET'])
@login_required  # <-- Protected!
def handle_search():
    query = request.args.get('query')
    if not query:
        flash('Please enter a search term.', 'error')
        return redirect(url_for('search_page'))

    print(f"--- NEW SEARCH from {session['username']}: {query} ---")
    return render_template('search_results.html', search_query=query)


if __name__ == '__main__':
    app.run(debug=True)