from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def dojo_survey():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def survey():
    name = request.form['name']
    unit = request.form['unit']
    lang = request.form['language']
    comm = request.form['comment']
    print name, unit, lang, comm 
    return render_template('result.html', name=name, unit=unit, lang=lang, comm=comm)

@app.route('/back')
def back():
   return redirect('/')

app.run(debug=True)