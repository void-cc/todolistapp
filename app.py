from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

app.secret_key = b'dwhbd'

@app.route('/', methods=['GET', 'POST'])
def homepage():

    if request.method == 'POST':
        ## Toevoegen van een nieuwe todo
        try:
            if request.form["toevoegen"]:
                session['todo'] += [request.form['toevoegen']]
            else:
                if session['todo']:
                    print('session not done anything')
                else:
                    session['todo'] = ['']
                    session['todo-done'] = ['']
                    print('session todo reset')
        except:
            pass

        # Het verwijderen van een todo
        try:
            session['todoid'] = request.form['todo-delete']
            del(session['todo'][int(session['todoid'])-1])
        except KeyError:
            pass

        # Het verwijderen van een todo done
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


if __name__ == '__main__':
    ##startup session
    session['todo-done'] = ['']
    app.run(debug=True)
