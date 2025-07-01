import flask_login
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required

from user import User

app = Flask(__name__)
app.secret_key = 'super secret key'
login_manager = LoginManager()
login_manager.init_app(app)

users = {"patrik@dendis.sk": User("patrik@dendis.sk", "heslo"),
         "test@test.sk": User("test@test.sk", "heslo2")}

@app.route('/')
def home():
    if flask_login.current_user.is_authenticated:
        return redirect(url_for('welcome'))
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users.get(email).password == password:
            flask_login.login_user(users.get(email))
            return redirect(url_for('welcome'))
        else:
            error = "Invalid email or password"
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/welcome')
@login_required
def welcome():
    current_user = flask_login.current_user
    return render_template('welcome.html', username=current_user.id)

@login_manager.user_loader
def load_user(user_id):
    return users.get(user_id)

if __name__ == '__main__':
    app.run(debug=True)