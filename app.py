from flask import Flask, redirect, render_template, url_for, request, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re           #regular expression(regex)

app = Flask(__name__)


app.secret_key = 'lakjhfkasdhhd'

# configuration for mysql to app 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'SudoLucky.99'
app.config['MYSQL_DB'] = 'code' 
mysql = MySQL(app)


# routes
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    message = ''
    # if method is post and username is in the submitted input
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        #capturing the username and password from form
        username = request.form['username']
        password = request.form['password']
        # to query for the record with the submitted username and password
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)   
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        #account holds the record's data 
        if account:
            # create session
            session['loggedin'] = True
            session['username'] = username
            session['email'] = account['email']
            session['id'] = account['id']
            message = 'logged in successfully'
            return render_template('index.html', msg = message)
        else:
            message = 'invalid username and password'
    return render_template('login.html', msg = message)

@app.route('/register', methods =['GET', 'POST'])
def register(): 
    message = ''
    # if method is POST and username, password, email are all present in the submitted data
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            message = 'this account already exists'
        elif not username or not password or not email:
            message = 'Please fill all fields'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            message = 'You have successfully registered !'
    elif request.method == 'POST':
        message = 'Please fill out the form'
    return render_template('register.html', msg = message)


@app.route('/logout')
def logout():
    # destroy session
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('login'))   #redirect to login


if __name__ == '__main__':
    app.run(debug=True)