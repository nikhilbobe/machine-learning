from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/calculator_db"
mongo = PyMongo(app)

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('calculator'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('calculator'))
    
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'username': request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({
                'username': request.form['username'],
                'password': hashpass,
                'email': request.form['email']
            })
            session['username'] = request.form['username']
            return redirect(url_for('calculator'))
        
        flash('Username already exists!')
        return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('calculator'))
    
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'username': request.form['username']})

        if login_user:
            if bcrypt.checkpw(request.form['password'].encode('utf-8'), login_user['password']):
                session['username'] = request.form['username']
                return redirect(url_for('calculator'))
        
        flash('Invalid username/password combination')
        return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/calculator')
def calculator():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('calculator.html', username=session['username'])

@app.route('/calculate', methods=['POST'])
def calculate():
    if 'username' not in session:
        return {'error': 'Unauthorized'}, 401
    
    data = request.get_json()
    try:
        result = eval(data['expression'])  # Note: Using eval is dangerous in production!
        # In production, use a proper expression evaluator or parsing library
        return {'result': result}
    except Exception as e:
        return {'error': str(e)}, 400

if __name__ == '__main__':
    app.run(debug=True)