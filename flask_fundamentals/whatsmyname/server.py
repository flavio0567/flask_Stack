from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')

def hello_flask():
  return render_template('index.html')

@app.route('/process', methods=['POST'])
def print_name():
   name = request.form['name']
   print name

   return redirect('/')

app.run(debug=True)
