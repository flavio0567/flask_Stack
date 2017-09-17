from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import MySQLConnector
import re
from datetime import datetime, date, time
import md5
import os, binascii 

passwd_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')
date_regex = re.compile(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$')
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
app.secret_key = "TheWallThisIsSecret!"

mysql = MySQLConnector(app,'thewall')

@app.route('/')
def index():
  return render_template("layout.html")


@app.route('/login', methods=['GET'])
def submit():
    session['email'] = ""
    return render_template("login.html")

@app.route('/logout')
def logout():
    return redirect("/")


@app.route('/register', methods=['GET'])
def create_user():
  return render_template("register.html")


@app.route('/check_login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['passwd']
    # check email 
    if len(request.form['email']) == 0:
        return regErrorL('Enter your email address.')
    elif not email_regex.match(request.form['email']):
        return regErrorL('Invalid email address')
    else:
        session['email'] = request.form['email']
    # check password  
    if len(request.form['passwd']) == 0:
        return regErrorL('Enter your password')
    else:
        user_query = "SELECT * FROM users WHERE users.email = :email LIMIT 1"
        query_data = {'email': email}
        user = mysql.query_db(user_query, query_data)
        if len(user) != 0:
            passhashed = md5.new(password + user[0]['hashed_pw']).hexdigest()
            if user[0]['password'] == passhashed:
                session['user_id'] = user[0]['id']
                session['first_name'] = user[0]['first_name']
                session['last_name'] = user[0]['last_name']
                return redirect('/thewall')
            else:
                return regErrorL('Password or email not valid, try again!')
        else:
            return regErrorL('User not registered')


@app.route('/check_register', methods=['POST'])
def register():
    # check name and email 
    if request.form['inputFirstname'] == "":
        return regErrorR("Please enter your first name.")
    session['firstname'] = request.form['inputFirstname']
    if request.form['inputLastname'] == "":
        return regErrorR("Please enter your last name.")
    session['lastname'] = request.form['inputLastname']
    if request.form['inputEmail1'] != "":
        session['email1'] = request.form['inputEmail1']
        if not email_regex.match(request.form['inputEmail1']):
            return regErrorR('Invalid email address')
        if request.form['inputEmail2'] == "":
            return regErrorR("Please confirm email.")
        session['email2'] = request.form['inputEmail2']
        if request.form['inputEmail1'] != request.form['inputEmail2']:
            return regErrorR("Email addresses did not match. Please enter emails again.")
        email = request.form['inputEmail1']
    else:
        return regErrorR("Please enter a email.")
    # check password
    if request.form['inputPassword1'] != "":
        if len(request.form['inputPassword1']) < 9:
            return regErrorR('Password must be greater than 8 characters long')
        if not passwd_regex.match(request.form['inputPassword1']):
            return regErrorR('Password must contain at least one digit, one lowercase letter, and one uppercase letter.')
        if request.form['inputPassword2'] == "":
            return regErrorR("Please confirm password.")
        if request.form['inputPassword1'] != request.form['inputPassword2']:
            return regErrorR("Passwords did not match. Please enter passwords again.")
        user_query = "SELECT * FROM users WHERE users.email = :email LIMIT 1"
        query_data = {'email': email}
        user = mysql.query_db(user_query, query_data)
        if len(user) != 0:
            return regErrorR("There is already an account created with this email address. "
                             "Please either login in using this address, or create an account "
                             "with a different email address.")
    else:
        return regErrorR("Please enter a password.")
    firstname = request.form['inputFirstname'] 
    lastname = request.form['inputLastname'] 
    password = request.form['inputPassword1']
    insert_query = ("INSERT INTO users"
                   "(first_name, last_name, email, password, hashed_pw, created_at, updated_at) " 
                   "VALUES (:firstname, :lastname,:email, :password, :hashed_pw, NOW(), NOW())")
    hashed_pw =  binascii.b2a_hex(os.urandom(15))
    passhashed = md5.new(password + hashed_pw).hexdigest()
    query_data = { 'firstname': firstname, 'lastname': lastname, 'email': email, 'password': passhashed, 'hashed_pw': hashed_pw}
    result = mysql.query_db(insert_query, query_data)
    if result > 0:    
        return regErrorR("Account registration successfull! Please use your credentials to login.")


@app.route('/thewall')
def wall():
    session['messages'] = []
    session['comments'] = []
    user_id = session['user_id']
    message_query = ("SELECT messages.id AS message_id, users.first_name, users.last_name, "
                     "messages.message, date_format(messages.created_at, '%M %D %Y') AS mess_date "
                     "FROM users INNER JOIN messages ON users.id = messages.user_id "
                     "ORDER BY messages.created_at DESC")                     
    query_data = {'user_id': user_id}
    messages = mysql.query_db(message_query, query_data)
    session['messages'] = messages
    if len(messages) != 0:
        user_id = session['user_id']
        comment_query = ("SELECT users.first_name, users.last_name, " 
                        "comments.message_id, comments.user_id, comments.comment, "
                        "date_format(comments.created_at, '%M %D %Y') "
                        "AS comm_date FROM comments JOIN users "
                        "ON users.id = comments.user_id ORDER BY comments.created_at")
        query_data = {'user_id': user_id}
        comments = mysql.query_db(comment_query, query_data)
        session['comments'] = comments
        if session['comments'] != "":
            return regErrorM('')
        else:
            session['comments'] = []
            return regErrorM('')
    else:
        return regErrorM('Welcome!!!')

@app.route('/check_wall', methods=['POST'])
def message():
    user_id = session['user_id']
    message = request.form['inputMessage']
    if request.form['inputMessage'] == "":
        return regErrorM('Enter a message.')
    insert_query = ("INSERT INTO messages"
                    "(user_id, message, created_at, updated_at) " 
                    "VALUES (:user_id, :message, NOW(), NOW())")
    query_data = {'user_id': user_id, 'message': message}
    result = mysql.query_db(insert_query, query_data)
    if result > 0:    
        return redirect('/thewall')

@app.route('/check_comment/<m_id>', methods=['POST'])
def comment(m_id):
    message_id = m_id
    user_id = session['user_id']
    comment = request.form['inputComment']
    if request.form['inputComment'] != "":
        insert_query = ("INSERT INTO comments"
                        "(message_id, user_id, comment, created_at, updated_at) " 
                        "VALUES (:message_id, :user_id, :comment, NOW(), NOW())")
        query_data = {'message_id': message_id, 'user_id': user_id, 'comment': comment}
        result = mysql.query_db(insert_query, query_data)
        if result > 0:    
            return redirect('/thewall')
    else:
        return regErrorM('Enter a comment.')

def regErrorL(message):
    flash(message)
    return render_template("login.html",pageType=['login'],flashType="danger")
 
def regErrorR(message):
    flash(message)
    return render_template("register.html",pageType=['register'],flashType="danger")
 
def regErrorM(message):
    flash(message)
    return render_template("wall.html", messages=session['messages'], comments=session['comments'])

app.run(debug=True)