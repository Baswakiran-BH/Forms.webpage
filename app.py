from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps  # <-- Import this
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)
# Make this unique for your club project
app.config['SECRET_KEY'] = 'my_clubs_very_secret_key_9876'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'txt'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

# --- NEW: Forms hub (protected) ---
@app.route('/forms')
@login_required
def forms_home():
    return render_template('forms.html')

# --- NEW: Profile form (protected) ---
@app.route('/profile_page')
@login_required
def profile_page():
    return render_template('profile.html')

@app.route('/submit_profile', methods=['POST'])
@login_required
def submit_profile():
    full_name = request.form.get('full_name', '').strip()
    bio = request.form.get('bio', '').strip()
    phone = request.form.get('phone', '').strip()

    # Simulate save (print to console)
    print("--- PROFILE UPDATE ---")
    print(f"User: {session.get('username')}")
    print(f"Name: {full_name}")
    print(f"Phone: {phone}")
    print(f"Bio: {bio}")
    print("----------------------")

    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile_page'))

# --- NEW: Feedback form (protected) ---
@app.route('/feedback_page')
@login_required
def feedback_page():
    return render_template('feedback.html')

@app.route('/submit_feedback', methods=['POST'])
@login_required
def submit_feedback():
    rating = request.form.get('rating', '').strip()
    message = request.form.get('message', '').strip()

    print("--- NEW FEEDBACK ---")
    print(f"From: {session.get('username')}")
    print(f"Rating: {rating}")
    print(f"Message: {message}")
    print("--------------------")

    flash('Thanks for your feedback!', 'success')
    return redirect(url_for('feedback_page'))

# --- NEW: File upload form (protected) ---
@app.route('/upload_page')
@login_required
def upload_page():
    return render_template('upload.html')

@app.route('/submit_upload', methods=['POST'])
@login_required
def submit_upload():
    file = request.files.get('file')
    note = request.form.get('note', '').strip()

    if not file or file.filename == '':
        flash('Please choose a file to upload.', 'error')
        return redirect(url_for('upload_page'))

    if not allowed_file(file.filename):
        flash('File type not allowed. Try png, jpg, jpeg, pdf, or txt.', 'error')
        return redirect(url_for('upload_page'))

    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(save_path)

    print("--- FILE UPLOAD ---")
    print(f"User: {session.get('username')}")
    print(f"Saved: {save_path}")
    print(f"Note: {note}")
    print("-------------------")

    flash('File uploaded successfully!', 'success')
    return redirect(url_for('upload_page'))

if __name__ == '__main__':
    app.run(debug=True)