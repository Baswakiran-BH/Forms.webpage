📂 Project Structure
project/
│ app.py
│ README.md
│
├─ templates/
│   base.html
│   index.html
│   login.html
│   contact.html
│   search.html
│   search_results.html
│   forms.html
│   profile.html
│   feedback.html
│   upload.html
│
└─ static/
    style.css

🛠️ Requirements

Install Flask:

pip install flask

▶️ Run the App
python app.py


Then open your browser and go to:

http://127.0.0.1:5000/

🔑 Login Details (Demo)
Username	Password
kiran	kiranbh08

You can change this in app.py inside the /submit_login route.

🔒 Route Protection

This project uses a custom decorator to protect form pages:

@login_required
def contact_page():
    return render_template('contact.html')


If the user is not logged in, they are redirected to the login page with a flash message.

🎨 UI

The user interface is styled using style.css located in the static/ folder.
It includes:

Smooth gradients

Card-style form containers

Button hover effects

Light/Dark theme support (automatic)

✨ Credits

Developed using:

Python

Flask

HTML / Jinja Templates

CSS