from flask import Flask, render_template, request, session, flash
import sqlite3 as sql
import os

app = Flask(__name__)


##########################################
#              home function             #
##########################################
# Take the user to the home page if logged in
# successfully.
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template("editor.html")


##########################################
#              login function            #
##########################################
# User will be logged in if their username and password
# are a match. If logged in successfully, store their
# session data.
@app.route('/login', methods=['POST'])
def login():
    # Validate username and password are correct
    try:
        username = request.form['username']
        password = request.form['password']

        with sql.connect("LicensingManagementDB.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()

            sql_select_query = "SELECT * FROM Users WHERE Username = ? and Password = ?"""
            cur.execute(sql_select_query, (username, password))

            row = cur.fetchone()
            # If the user logs in successfully, track their username and
            # role level and set login status to true.
            if row != None:
                conn = sql.connect('LicensingManagementDB.db')
                curs = conn.cursor()

                session['username'] = username
                session['logged_in'] = True
                for row in curs.execute("SELECT RoleLevel FROM Users WHERE Username = ?", (username,)):
                    temp = row
                for i in temp:
                    session['accessLevel'] = str(i)
                    session['accessLevel'] = int(session['accessLevel'])
            else:
                session['logged_in'] = False
                flash('Invalid username and/or password!')
    except:
        con.rollback()
        flash("Error in insert operation")
    finally:
        con.close()
    return home()


##########################################
#             logout function            #
##########################################
# Logout the user and reset their session data.
@app.route("/logout")
def logout():
    session['username'] = ""
    session['accessLevel'] = 0
    session['logged_in'] = False
    return home()


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
