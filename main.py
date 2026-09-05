from flask import Flask, render_template, request, redirect
import mysql.connector
import os

app = Flask(__name__)

# --- DATABASE CONNECTION - AIVEN CORRECT DA ---
def get_db_connection():
    conn = mysql.connector.connect(
        host="mysql-16b5aed2-liyanasaifullah2022-d091.k.aivencloud.com",
        port=13818,
        user="avnadmin",
        password=os.getenv("DB_PASSWORD") or "AVNS_NHmxFYh4uNiLj2i0by-",
        database="defaultdb",
        ssl_ca="/etc/ssl/certs/ca-certificates.crt"
    )
    return conn

# --- ROUTES ---

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/admission")
def admission_page():
    return render_template("admission.html")

@app.route("/newadmission", methods=['GET', 'POST'])
def newadmission():
    if request.method == 'POST':
        try:
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
            
            query = """
                INSERT INTO admission (fullname, dob, gender, email_address, email_password, phone, address, department, percentage) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, dob, gender, email, password, phone, address, department, hp))
            conn.commit()
            conn.close()
            
            return "<h1>Information register Success da Liya! ✅</h1> <a href='/'>Go Home</a>"
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"<h2>DB ERROR:</h2> <p>{str(e)}</p> <pre>{traceback.format_exc()}</pre>"
            
    return render_template("admission.html")

@app.route("/newlogin", methods=['GET','POST'])
def newlogin():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM admission WHERE email_address=%s AND email_password=%s", (email, password))
            user = cursor.fetchone()
            conn.close()
            if user:
                return f"<h1>Welcome {user['fullname']} da!</h1>"
            else:
                return "<h1>Invalid Login da</h1>"
        except Exception as e:
            return f"DB ERROR: {str(e)}"
    return render_template("login.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
