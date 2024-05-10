from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from createengine import sessiondatabase as sdb
from databasemodels import TodoList
from sqlalchemy import select
from databasemodels import User
import database_interactions.todo_interacts as ti

app = Flask(__name__)

app.secret_key = b'dwhbd'






@app.route('/', methods=['GET', 'POST'])
def homepage():

    if request.method == 'POST':
        ## Toevoegen van een nieuwe todo
        try:
            if request.form["toevoegen"]:
                session['todo'] += [request.form['toevoegen']]
                # print(request.form['toevoegen-date'])
                # if datetime.now().date() > datetime.fromisoformat(request.form['toevoegen-date']):
                #     overdue = False
                # else:
                #     overdue = True

                new_todo = TodoList(
                    todo_text=request.form['toevoegen'],
                    todo_made_time=datetime.now(),
                    todo_date=datetime.fromisoformat(request.form
                                                     ['toevoegen-date']),
                    todo_date_overdue=False,
                    todo_done=False,
                    user_id=1,
                )
                sdb.add(new_todo)
                sdb.commit()
                session['todo'] = []
                stmt = select(TodoList).where(TodoList.user_id == 1)
                result = sdb.execute(stmt)
                for user_obj in result.scalars():
                    print(user_obj)
                    session['todo'].append(
                        {'todo_text': user_obj.todo_text,
                         'todo_made_time': user_obj.todo_made_time,
                         'todo_date': user_obj.todo_date,
                         'todo_date_overdue': user_obj.todo_date_overdue,
                         'todo_done': user_obj.todo_done,
                         'user_id': user_obj.user_id,
                         'id': user_obj.id
                         }
                    )
            else:
                if session['todo']:
                    print('session not done anything')
                else:
                    session['todo'] = ['']
                    session['todo-done'] = ['']
                    print('session todo reset')
        except:
            pass

        # Het verwijderen van een to_do
        try:
            session['todoid'] = request.form['todo-delete']
            del(session['todo'][int(session['todoid'])-1])
        except KeyError:
            pass

        # Het verwijderen van een to_do done
        try:
            session['todoid'] = request.form['todo-done-delete']
            del(session['todo-done'][int(session['todoid'])-1])
        except KeyError:
            pass

        ## Het verplaatsen naar de done area
        try:
            session['todoid'] = request.form['todo-done']
            session['todo-done'] += [session['todo'][int(session['todoid']) - 1]]
            del(session['todo'][int(session['todoid']) - 1])
        except KeyError:
            pass

        # Het terug verplaatsen
        try:
            session['todoid'] = request.form['todo-done-back']
            session['todo'] += [session['todo-done'][int(session['todoid']) - 1]]
            del(session['todo-done'][int(session['todoid']) - 1])
        except KeyError:
            pass

    if session['todo']:
        print('session not done anything')
    else:
        session['todo'] = []
        print('session todo reset')
    try:
        if session['todo-done']:
            print('session todo done not done anything')
    except KeyError:
        session['todo-done'] = []
        print('session todo done reset')




    return render_template('index.html', todolist=session['todo'], todolistdone=session['todo-done'])


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    melding = ''
    username = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        stmt = select(User).where(User.name.in_([username]))
        for user in sdb.scalars(stmt):
            print(user.name)
            if username == username and user.check_password(password):
                homepage()
                return
                #return render_template('index.html', todolist=[], todolistdone=[])
            else:
                melding = 'Username or password is incorrect'
    return render_template('login.html', melding=melding, username=username)


if __name__ == '__main__':
    ##startup session
    session['todo-done'] = ['']
    app.run(debug=True)
