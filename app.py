from flask import Flask, jsonify, request, session
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'super secret key'

# DB stored procedure

# MySQL configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Rosenamayanja.22'
app.config['MYSQL_DB'] = 'FlaskApp'
app.config['MYSQL_HOST'] = 'localhost'

mysql = MySQL(app)


@app.route("/")
def index():
    return app.send_static_file('index.html')

@app.route("/api/register", methods=["POST"])
def register():
    json_data = request.json

    try:
        _email = json_data["email"]
        _password = json_data["password"]

        if _email and _password:    
            password = generate_password_hash(_password)
            cursor = mysql.connection.cursor()
            cursor.execute(""" INSERT INTO users (email, password) VALUES(%s,%s) """,(_email,password))
            mysql.connection.commit()
            status = 'success'
            cursor.close()
            return jsonify({'result': status})
        else:
            status = 'Enter required fields'
            return jsonify({'result': status})

    except Exception as e:
        status = 'this user is already registered'
        # status = {'error':str(e)}
        return jsonify(status)

@app.route("/api/login", methods=["POST"])
def login():
    json_data = request.json

    try:
        _email = json_data["email"]
        _password = json_data["password"]

        # Validate received values
        if _email and _password:

            # Make connection to DB
            cursor = mysql.connection.cursor()
            cursor.execute(""" SELECT * FROM users WHERE email LIKE %s""", (_email,))
            user = cursor.fetchone()

            if user and check_password_hash(
                user[2], _password):
                session['logged_in'] = True
                status = True
            else:
                status = False
            
            cursor.close()
            return jsonify({'result': status})
    except Exception as e:
        status = {'error':str(e)}
        return jsonify(status)

@app.route('/api/logout')
def logout():
    session.pop('logged_in', None)
    return jsonify({'result': 'Log Out Successful'})

@app.route('/api/status')
def status():
    if session.get('logged_in'):
        if session['logged_in']:
            return jsonify({'status': True})
    else:
        return jsonify({'status': False})

if __name__ == "__main__":
    # app.secret_key = 'super secret key'
    # app.config['SESSION_TYPE'] = 'filesystem'

    # sess.init_app(app)

    app.debug = True
    app.run()
