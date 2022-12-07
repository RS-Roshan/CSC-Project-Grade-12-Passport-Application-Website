from flask import Flask, render_template, url_for, request
from datetime import date
import mysql.connector as msql
import random
import string

try:
    con = msql.connect(user="root", host="localhost",passwd="roshpuppy123",database="projectdb")
    if con.is_connected():
        print("Successfully connected to database.")
    cursor = con.cursor()

except msql.Error:
  print("MySQL connection error.")


token = 'loggedout'
def generatetoken(typ):
    rand = ''
    for i in range(10):
        rand = rand+(random.choice(string.ascii_letters))
    if typ == 'U':
        return 'U' + rand
    elif typ == 'A':
        return 'A' + rand
    elif typ == "applicationID":
        return 'PID' + rand


app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    if token == 'loggedout':
        msg='Sign in or create an account to get started'
        return render_template("navbar.html",token=token, msg=msg)
    elif token.startswith('U'):
        cursor.execute("SELECT username FROM userlogin where token='{}'".format(token))
        username = cursor.fetchone()
        msg = "Welcome {}! How can we help ?".format(username[0].title())
        return render_template("navbar.html",token=token, msg=msg)

    elif token.startswith('A'):
        cursor.execute("SELECT username FROM adminlogin where token='{}'".format(token))
        username=cursor.fetchone()
        msg = "Welcome {}! Logged in as admin.".format(username[0].title())
        return render_template("navbar.html",token=token, msg=msg)
    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ''
    msg = ''
    token = 'loggedout'
    if request.method == 'POST':
        email = request.form['email']
        susername = request.form['username']
        spassword = request.form['password']
        cpassword = request.form['cpassword']

       
        if spassword != cpassword:
            error = "Passwords don't match."
            return render_template('signup.html', error=error, msg = msg)
        elif len(spassword) < 6:
            error = "Password must be atleast 6 characters."
            return render_template('signup.html', error=error, msg = msg)
        else:
            try:
                cursor.execute("INSERT INTO userlogin VALUES('{}','{}','{}','loggedout')".format(susername,spassword,email))
                con.commit()
                msg = "Account created successfully. Please login."
                return render_template('navbar.html', error=error, msg = msg, token = token)

            except msql.errors.IntegrityError:
                error = "Account already exists! Please pick another username."
                return render_template('signup.html', error=error, msg = msg)

    return render_template('signup.html', error=error, msg = msg, token = token)

@app.route('/userlogin', methods=['GET', 'POST'])
def userlogin():
    error = ''
    msg = ''
    global token
    token='loggedout'
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM USERLOGIN WHERE username='{}' AND password = '{}'".format(username, password))
        try:
            check = len(cursor.fetchone())
        except TypeError:
            error = 'Invalid Username or Password'
            return render_template('userlogin.html', error=error, msg = msg)
        else:
            token = generatetoken('U')
            cursor.execute("UPDATE USERLOGIN SET token='{}' WHERE username='{}'".format(token,username))
            con.commit()
            msg = "Welcome {}! How can we help ?".format(username.title())
            return render_template('navbar.html', error=error, msg = msg, token = token)

    return render_template('userlogin.html', error=error, msg = msg, token = token)


@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    error = ''
    msg = ''
    global token
    token='loggedout'
    if request.method == 'POST':
        global username
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM adminlogin WHERE username='{}' AND password = '{}'".format(username, password))
        try:
            check = len(cursor.fetchone())
        except TypeError:
            error = 'Invalid Username or Password'
            return render_template('adminlogin.html', error=error, msg = msg)
        else:
            token = generatetoken('A')
            cursor.execute("UPDATE adminlogin SET token='{}' WHERE username='{}'".format(token,username))
            con.commit()
            msg = "Welcome {}! Logged in as admin.".format(username.title())
            return render_template('navbar.html', error=error, msg = msg, token = token)

    return render_template('adminlogin.html', error=error, msg = msg, token = token)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    error = ''
    msg = 'Sign in or create an account to get started'
    global token
    if token == 'loggedout':
        pass
    elif token.startswith('U'):
        cursor.execute("SELECT username FROM userlogin WHERE token='{}'".format(token))
        username = cursor.fetchone()
        cursor.execute("UPDATE userlogin SET token='loggedout' WHERE username='{}'".format(username[0]))
        token = "loggedout"
        con.commit()
    elif token.startswith('A'):
        cursor.execute("SELECT username FROM adminlogin WHERE token='{}'".format(token))
        username = cursor.fetchone()
        cursor.execute("UPDATE adminlogin SET token='loggedout' WHERE username='{}'".format(username[0]))
        token="loggedout"
        con.commit()
    else:
        error = "logout error"

    token = 'loggedout'
    return render_template('navbar.html', error=error, msg = msg, token = token)


@app.route('/procedures')
def procedures():
    error = ''
    msg = ''
    return render_template('procedures.html', error=error, msg = msg, token = token)

@app.route('/docs')
def docs():
    error = ''
    msg = ''
    return render_template('docs.html', error=error, msg = msg, token = token)

@app.route('/application')
def application():
    error = ''
    msg = ''
    return render_template('application.html', error=error, msg = msg, token = token)

@app.route('/createapplication', methods=['GET', 'POST'])
def createapplication():
    error = ''
    msg=''
    atoken = generatetoken('applicationID')
    today = date.today().strftime("%Y-%m-%d")
    appstatus = 'Pending'
    pptype = request.form['pptype']
    country = request.form['country']
    neworrenew = request.form['neworrenew']
    oldppno = request.form['oldppno']
    if len(oldppno) == 0:
        oldppno = 'not available'
    fname = request.form['fname']
    lname = request.form['lname']
    dob = request.form['dob']
    p1name = request.form['p1name']
    p2name = request.form['p2name']
    spname = request.form['spname']
    if len(spname) == 0:
        spname = 'unmarried'
    occ = request.form['occ']
    if len(occ) == 0:
        occ = 'unemployed'
    addr = request.form['add']
    reg = request.form['region']

    try:
        cursor.execute("SELECT username FROM userlogin where token='{}'".format(token))
        username = cursor.fetchone()[0]
        cursor.execute("INSERT INTO applications VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(atoken,today,username,appstatus,pptype,country,neworrenew,oldppno,fname,lname,dob,p1name,p2name,spname,occ,addr,reg))
        con.commit()
        msg = 'Your application was submitted successfully!'

    except msql.Error as aerr:
        msg = 'Error while applying'
        print(aerr)

    return render_template('navbar.html', error=error, msg = msg, token = token)

@app.route('/dashboard')
@app.route('/dashboard?')
def dashboard():
    if token == 'loggedout':
        msg='Sign in to your account to view and manage your applications'
        return render_template("dashboard.html",token=token, msg=msg)
    elif token.startswith('U'):
        cursor.execute("SELECT username from userlogin WHERE token='{}'".format(token))
        username = cursor.fetchone()[0]
        cursor.execute("SELECT * FROM applications where AppUsername='{}'".format(username))
        applications = cursor.fetchall()
        msg = "Welcome {}! How can we help ?".format(username[0].title())
        return render_template("dashboard.html",token=token, msg=msg, applications=applications)

@app.route('/cancel', methods=['GET', 'POST'])
def cancel():
    error =''
    cancelid = request.form['cancel']
    cursor.execute("UPDATE applications SET AppStatus='Cancelled' where AID='{}'".format(cancelid))
    con.commit()
    cursor.execute("SELECT username from userlogin WHERE token='{}'".format(token))
    username = cursor.fetchone()[0]
    cursor.execute("SELECT * FROM applications where AppUsername='{}'".format(username))
    applications = cursor.fetchall()
    msg = ''
    return render_template("dashboard.html",token=token, msg=msg, error = error, applications=applications)

@app.route('/adminmanage', methods=['GET', 'POST'])
def adminmanage():
    msg = 'Access Denied, Sign In As Admin To Access'

    try:
        apid = request.form['approve']
        cursor.execute("UPDATE applications SET AppStatus='Approved, Processing' where AID='{}'".format(apid))
        con.commit()
    except:
        pass

    try:
        applications = cursor.fetchall()
        rpid = request.form['reject']
        cursor.execute("UPDATE applications SET AppStatus='Rejected' where AID='{}'".format(rpid))
        con.commit()
    except:
        pass

    try:
        dpid = request.form['delete']
        cursor.execute("DELETE FROM applications where AID='{}'".format(dpid))
        con.commit()
    except:
        pass

    cursor.execute("SELECT * from applications")
    applications = cursor.fetchall()

    return render_template("adminmanage.html",token=token, msg=msg, applications=applications)

@app.route('/view', methods=['GET', 'POST'])
def view():
    error =''
    viewid = request.form['view']
    cursor.execute("SELECT * from applications where AID='{}'".format(viewid))
    applications = cursor.fetchone()
    msg = ''
    return render_template("view.html",token=token, msg=msg, error = error, applications=applications)

if __name__ == '__main__':
   app.run()