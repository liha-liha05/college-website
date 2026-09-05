from flask import Flask, render_template, request, redirect
import mysql.connector
import os

app = Flask(__name__)

# DB Connect Function - Ithu than Aiven kitta connect pannum da
def get_db_connection():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    return conn

# Table auto create panna - Nee Aiven ku poga venda da
@app.route("/fixdb")
def fixdb():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS admission;")
        cursor.execute("""
            CREATE TABLE admission (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fullname VARCHAR(255),
                dob VARCHAR(50),
                gender VARCHAR(20),
                email_address VARCHAR(255),
                email_password VARCHAR(255),
                phone VARCHAR(20),
                address TEXT,
                department VARCHAR(100),
                percentage VARCHAR(20)
            );
        """)
        conn.commit()
        conn.close()
        return "<h1>Table Ready da Liya! ✅ Ipo /newadmission work aagum da!</h1>"
    except Exception as e:
        return f"<h2>Error da: {e}</h2>"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/newadmission", methods=["GET", "POST"])
def newadmission():
    if request.method == "POST":
        try:
            fullname = request.form['fullname']
            dob = request.form['dob']
            gender = request.form['gender']
            email_address = request.form['email']
            email_password = request.form['email_password']
            phone = request.form['phone']
            address = request.form['address']
            department = request.form['department']
            percentage = request.form['percentage']

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO admission (fullname, dob, gender, email_address, email_password, phone, address, department, percentage)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (fullname, dob, gender, email_address, email_password, phone, address, department, percentage))
            conn.commit()
            conn.close()
            return "<h1>Admission Success da Liya! ✅</h1> <a href='/'>Home ku po da</a>"
        except Exception as e:
            return f"<h2>DB Error da: {e}</h2> <br> <a href='/fixdb'>First /fixdb click pannu da</a>"

    return render_template("newadmission.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
