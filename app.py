from flask import Flask, render_template, request, url_for, flash, redirect, session

HOST = "0.0.0.0"

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')

@app.route('/reservations', methods=['GET'])
def reservation():
    return render_template('reservations.html')

# start the flask app
app.run(host=HOST)
