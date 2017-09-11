from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'ThisIsSecret' 

@app.route('/')
def index():
    if 'count' in session:
        count = session['count'] + 1
    else:
        count = 1 
    session['count'] = count
    return render_template('index.html', count=session['count'])

@app.route('/process', methods=['POST'])
def reload():    
    if  request.form['action'] == 'reload':
        return redirect('/')
    elif    request.form['action'] == 'plus2':  
            if 'count' in session:
                count = session['count'] + 2
            else:
                count = 1 
            session['count'] = count
            return render_template('index.html', count=session['count'])
    else:
        return redirect('/')

@app.route('/reset', methods=['POST'])
def _reset():   
    if  request.form['action'] == 'reset':
        count = 0
        session['count'] = count
        return redirect('/')

app.run(debug=True)