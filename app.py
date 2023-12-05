from flask import Flask, render_template, request, url_for, flash, redirect, session
from authentication import Authentication

HOST = "0.0.0.0"

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'your secret key'
auth = Authentication('passcodes.txt')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    bus_data = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # we can at least repopulate the username
        # on failed login attempt
        session['username'] = username

        if valid_login(username, password):
            #bus_data = get_trip_info()
            # replace with the bus display & cost info
            bus_data = 'Valid login!'
            # remove on successful login
            session['username'] = None

    return render_template('admin.html', bus_data=bus_data)

def valid_login(username: str, password: str) -> bool:
    valid = True

    if not username:
        valid = False
        flash('Username is required.')
    if not password:
        valid = False
        flash('Password is required.')
    if valid and not auth.login(username, password):
        valid = False
        flash('Invalid username/password combination.')
    
    return valid
    
@app.route('/reservations', methods=['GET'])
def reservation():
    return render_template('reservations.html')

# start the flask app
app.run(host=HOST)
