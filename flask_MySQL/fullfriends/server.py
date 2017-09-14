from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
from datetime import datetime, date, time

dateRegex = re.compile(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$')

app = Flask(__name__)
app.secret_key = 'essaninguemvaipegar'
mysql = MySQLConnector(app,'friendsdb')

@app.route('/')
def index():
    query = "SELECT * FROM friends"                           # define your query
    friends = mysql.query_db(query)                           # run query with query_db()
    return render_template('index.html', all_friends=friends) # pass data to our template

@app.route('/friends', methods=['POST'])
def create():

    query = "INSERT INTO friends (first_name, last_name, created_at, updated_at, age, friend_since) VALUES (:first_name, :last_name, NOW(), NOW(), :age, :friend_since)"

   # verify friend-date
    print "the form date is: " + request.form['friend_since']
    if request.form['friend_since'] == '':
        flash('Data friendship cannot be blank', 'error')
        return redirect('/')
    elif not dateRegex.match(request.form['friend_since']):
        flash('Date friendship is not valid', 'error')
        return redirect('/')
    elif datetime.now().strftime('%Y%m%d') <= "".join(request.form['friend_since'].split("-")):
        flash('Date frienship must be in the past', 'error')
        return redirect('/')
    else:
        _friend_since = request.form['friend_since']

    data = {
             'first_name': request.form['first_name'],
             'last_name':  request.form['last_name'],
             'age': request.form['age'],
             'friend_since': _friend_since
           }

    # Run query, with dictionary values injected into the query.
    mysql.query_db(query, data)
    return redirect('/')

app.run(debug=True)
