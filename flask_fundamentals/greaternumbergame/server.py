from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = 'ThisIsSecret' 

@app.route('/')
def index():
    myNumber = 0
    num = 0
    find = ''
    if num in session:
        num = session['num']
        myNumber = session['myNumber']
    else:
        num = random.randrange(0, 101)
        session['myNumber'] = myNumber 
    session['num'] = num
    session['find'] = find
    return render_template('index.html', num=session['num'], find=session['find'], myNumber=session['myNumber'])

@app.route('/process', methods=['POST'])
def reload():    
    if  request.form['action'] != 'reload':
        return redirect('/')
    else:
        if  int(session['num']) == int(request.form['myNumber']):
            session['find'] = 1
            return render_template('result.html', num=session['num'], find=session['find'], myNumber=request.form['myNumber'])
        elif int(request.form['myNumber']) > int(session['num']):
            session['find'] = 2
            session['myNumber'] = request.form['myNumber']
            return render_template('index.html', num=session['num'], find=session['find'], myNumber=request.form['myNumber'])
        else:
            session['find'] = 0
            return render_template('index.html', num=session['num'], find=session['find'], myNumber=request.form['myNumber'])

@app.route('/reset', methods=['POST'])
def _reset():   
    session.pop('num')
    return redirect('/')

app.run(debug=True)