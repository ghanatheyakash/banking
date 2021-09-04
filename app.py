
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

app = Flask(__name__)
app.secret_key = 'a' 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'blood'
mysql = MySQL(app)
@app.route('/')
def intro():
    return render_template('index.html')
@app.route('/signup',methods=['GET','POST'])
def signup():
    msg = ''
    if request.method == 'POST' :
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        cursor=mysql.connection.cursor()
        cursor.execute('SELECT * FROM account WHERE Email = % s', (email, ))
        account = cursor.fetchone()
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO account VALUES (NULL, % s, % s, % s)', (username,email,password))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            body=" Hello {} \n\n Welcome to SMART BANKING. we make life easy\n we provide a safe and secure service \n ".format(username)
            subject="donotreply"
            message=MIMEMultipart()
            message['From']="crackpython21@gmail.com"
            message['To']=email
            message['subject']=subject
            message.attach(MIMEText(body,'plain'))
            text=message.as_string()
            mail=smtplib.SMTP('smtp.gmail.com', 587)
            mail.starttls()
            mail.login("crackpython21@gmail.com","python@21")
            mail.sendmail("crackpython21@gmail.com",email,text)
            mail.close()
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
            
    return render_template('signup.html',msg=msg) 
@app.route('/login',methods=['GET','POST'])
def login():
    global userid
    msg = '' 
    if request.method=='POST' :
        email = request.form['email']
        password = request.form['password']
        print(email ,password)
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM account WHERE Email = % s AND password = % s', (email, password ),)
        account = cursor.fetchone()
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            userid=  account[0]
            session['email'] = account[2]
            msg = 'Logged in successfully !'
            return render_template('pay.html')
        else:
            msg = 'Incorrect username / password !'
        return render_template('login.html', msg = msg)
    return render_template('login.html', msg = msg)
@app.route('/pay',methods=['GET','POST'])
def payment():
    msg=" "
    if request.method=='POST' :
        username = request.form['username']
        phoneno=request.form['email']
        amount = request.form.get('amount', False)
        status="PAID"
        msg=status
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO trans VALUES ( % s, % s, % s ,%s)', (username,phoneno,amount,status))
        mysql.connection.commit()
        msg=status
        body=" Hello {} \n\n Welcome to SMART BANKING. we make life easy\n we provide a safe and secure service \n \n\n The payment was sucessfull \nplease visit the page for further information  ".format(username)
        subject="donotreply"
        message=MIMEMultipart()
        message['From']="crackpython21@gmail.com"
        email=session['email']
        print(email)
        message['To']=email
        message['subject']=subject
        message.attach(MIMEText(body,'plain'))
        text=message.as_string()
        mail=smtplib.SMTP('smtp.gmail.com', 587)
        mail.starttls()
        mail.login("crackpython21@gmail.com","python@21")
        mail.sendmail("crackpython21@gmail.com",email,text)
        mail.close()
    return render_template('pay.html',msg=msg)

@app.route('/Loan',methods=['GET','POST'])
def Loan():
    msg=" "
    if request.method=='POST' :
        username = request.form['username']
        email=request.form['email']
        gender=request.form.get('gender', False)
        age=request.form.get('age', False)
        phoneno= request.form.get('number',False)
        amount = request.form.get('amount', False)
        city= request.form.get('city',False)
        print(username,email,gender,age,phoneno,amount,city)
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO loan VALUES ( % s, % s, % s,% s, % s, % s ,%s )', (username,email,gender,age,phoneno,amount,city))
        mysql.connection.commit()
        msg="successfull , Our agent will contact you soon "
    return render_template('loan.html',msg=msg)

@app.route('/Transaction History',methods=['GET','POST'])
def transaction():
    msg=" "
    
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * FROM trans')
    account = cursor.fetchall()
    print(account)
    msg=account
    
    return render_template('transaction.html',msg=msg)

@app.route('/contact us',methods=['GET','POST'])
def contactus():
    msg=""
    if request.method=='POST':
        email=request.form['email']
        messages=request.form['message']
        print(email,messages)
        body=" Hello  .\n\n {}".format(messages)
        subject=email
        message=MIMEMultipart()
        message['From']="crackpython21@gmail.com"
        message['To']="crackpython21@gmail.com"
        message['subject']=subject
        message.attach(MIMEText(body,'plain'))
        text=message.as_string()
        mail=smtplib.SMTP('smtp.gmail.com', 587)
        mail.starttls()
        mail.login("crackpython21@gmail.com","python@21")
        mail.sendmail("crackpython21@gmail.com","crackpython21@gmail.com",text)
        mail.close()
        msg="We will contact you soon"
    return render_template('contactus.html',msg=msg)
@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('email')
   return render_template('index.html')

if __name__ == '__main__':
   app.run(debug=True, host = "0.0.0.0",port = 8080)# -*- coding: utf-8 -*-


