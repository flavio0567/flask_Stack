from flask import Flask, render_template

app = Flask(__name__)

@app.route('/success')

def success():
  return render_template('success.html')

app.run(debug=True)