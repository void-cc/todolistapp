from flask import Flask, render_template, request, session, redirect, url_for
from createengine import sessiondatabase as sdb
from sqlalchemy import select
from databasemodels import User
from api import api

app = Flask(__name__)
app.secret_key = b'dwhbd'

app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def homepage():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    melding = ''
    username = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        stmt = select(User).where(User.name.in_([username]))
        for user in sdb.scalars(stmt):
            if user and user.check_password(password):
                session['user_id'] = user.id
                return redirect(url_for('homepage'))
        melding = 'Username or password is incorrect'
    return render_template('login.html', melding=melding, username=username)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login_page'))


if __name__ == '__main__':
    app.run(debug=True)
