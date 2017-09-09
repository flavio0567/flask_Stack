from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ninja')
def ninjas():
    return render_template('ninjas.html')

@app.route('/ninja/<ninja_color>')
def select_ninja(ninja_color):
    return render_template("selectninja.html", ninja_color=ninja_color)

app.run(debug=True)