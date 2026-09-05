from flask import Flask, render_template, flash, request,session,redirect
#from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from werkzeug.utils import secure_filename
import mysql.connector
import os

def get_db_connection():
    return mysql.connector.connect(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        port=int(os.getenv('DB_PORT', 3306))
    )
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register")
def register():
    return render_template("register.html")
@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/services")
def services():
    return render_template("services.html")
@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/departments")
def departments():
    return render_template("departments.html")
@app.route("/admission")
def admission():
    return render_template("admission.html")
@app.route("/admissions")
def admissions():
    return render_template("admissions.html")
@app.route("/admin")
def admin():
    return render_template("adminlogin.html")
@app.route("/user")
def user():
    return render_template("user.html")

@app.route("/adminhome")
def adminhome():
    return render_template("adminhome.html")
@app.route("/addcourses")
def addcourses():
    return render_template("addcourse.html")
@app.route("/viewcourse")
def viewcourse():
    return render_template("viewcourse.html")
@app.route("/results")
def results():
    return render_template("results.html")
@app.route("/reports")
def reports():
    return render_template("reports.html")
@app.route("/logout")
def logout():
    return render_template("logout.html")
@app.route("/slogout")
def slogout():
    return render_template("slogout.html")
@app.route("/profile")
def profile():
    return render_template("profile.html")
@app.route("/attendance")
def attendance():
    return render_template("attendance.html")

@app.route("/result")
def result():
    return render_template("result.html")
@app.route("/courses2")
def courses2():
    return render_template("courses2.html")
@app.route("/contact2")
def contact2():
    return render_template("contact2.html")
@app.route("/notice")
def notice():
    return render_template("notice.html")


@app.route("/editcourse")
def editcourse():
    return render_template("editcourse.html")

@app.route("/deletecourse")
def deletecourse():
    return render_template("deletecourse.html")

@app.route("/newadmission",methods=['GET','POST'])
def newadmission():
    if request.method == 'POST':
        name = request.form['fullname']
        dob = request.form['dob']
        gender = request.form['gender']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        address = request.form['address']
        department = request.form['department']
        hp = request.form['percentage']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("insert into admission value('"+ name + "','"+ dob + "','"+ gender + "','"+ email + "','"+ password + "','"+ phone + "','"+ address + "','"+ department + "','"+ hp + "')")
        conn.commit()
        conn.close()
    return "Information register Success"
@app.route("/newlogin",methods=['GET','POST'])
def newlogin():

    email= request.form['email']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("select * from admission where email_address='"+email+"' and email_password='"+password+"'")
    data=cursor.fetchone()
    if data is None:
        return "email and password Wrong"
    else:
        session["email"]=email
        return render_template("otp.html",uname=email)


import random

otp = str(random.randint(100000, 999999))

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="sample"
)
# Testing only
@app.route("/userhome")
def userhome():
    uname=session['email']
    return render_template("userhome.html",uname=uname)


ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

@app.route("/adminlogin", methods=["GET", "POST"])
def adminlogin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            return render_template("adminhome.html")
        else:
            return "<h2>Invalid Username or Password</h2>"

    return render_template("adminlogin.html")

@app.route("/addcourse", methods=["GET", "POST"])
def addcourse():

    if request.method == "POST":

        courseid = request.form["courseid"]
        coursename = request.form["coursename"]
        department = request.form["department"]
        duration = request.form["duration"]
        fee = request.form["fee"]
        seats = request.form["seats"]
        description = request.form["description"]
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "insert into addcourse value('','" + coursename + "','" + department + "','" + duration + "','" + fee+ "','" + seats + "','" + description + "')")
        conn.commit()
        conn.close()
@app.route("/usercontact", methods=["GET", "POST"])
def usercontact():

            if request.method == "POST":
                stdname = request.form["name"]
                email = request.form["email"]
                department = request.form["department"]
                register = request.form["rollno"]
                enterquery = request.form["message"]
                conn = mysql.connector.connect(user='root', password='', host='localhost', database='ucontact')
                cursor = conn.cursor()
                cursor.execute(
                    "insert into ucontactmsg value('" + stdname + "','" + email + "','" + department + "','" + register+ "','" + enterquery + "')")
                conn.commit()
                conn.close()
                return "<h2>information send successfully</h2>"
            return render_template("usercontact.html")

@app.route("/noticefeedback", methods=["GET", "POST"])
def noticefeedback():

            if request.method == "POST":
                name = request.form["name"]
                email = request.form["email"]
                feedback= request.form["feedback"]
                conn = mysql.connector.connect(user='root', password='', host='localhost', database='feedback')
                cursor = conn.cursor()
                cursor.execute(
                    "insert into sfeedback value('" + name+ "','" + email + "','" + feedback +  "')")
                conn.commit()
                conn.close()
                return "<h2>information send successfully</h2>"
            return render_template("noticefeedback.html")




@app.route("/contactsubmit", methods=["GET", "POST"])
def contactsubmit():

    if request.method == "POST":

        fullname = request.form["name"]
        emailadd = request.form["email"]
        phonenum = request.form["phone"]
        subject = request.form["subject"]
        msg = request.form["message"]
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='contact')
        cursor = conn.cursor()
        cursor.execute(
            "insert into contactmsg value('" + fullname+ "','" + emailadd + "','" + phonenum + "','" + subject+ "','" + msg + "')")
        conn.commit()
        conn.close()
        # Save to database here

        return "<h2>information send successfully</h2>"

    return render_template("contact.html")




@app.route("/verifyotp")
def verifyotp():

    return render_template("otp.html")

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
