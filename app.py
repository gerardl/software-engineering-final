from flask import Flask, render_template, request, url_for, flash, redirect, session
from authentication import Authentication

HOST = "0.0.0.0"

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'your secret key'
auth = Authentication('passcodes.txt')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # selection
        choice = request.form['menu']
        if(choice  == 'admin'):
            return redirect(url_for('admin'))
        elif(choice == 'reservations'):
            return redirect(url_for('reservations'))
        else:
            flash("invalid option")
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    bus_data = None
    total_sales = 0

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # we can at least repopulate the username
        # on failed login attempt
        session['username'] = username

        if valid_login(username, password):
            bus_data = make_Bus_Data('reservations.txt')
            # need the calculation for total sales
            total_sales = calc_price(bus_data)
            # remove on successful login
            session['username'] = None

    return render_template('admin.html', bus_data=bus_data, total_sales=total_sales)

#make 2d array for seating chart

def make_Bus_Data(fileName):
    data =[
        ["O", "O", "O", "O"],
        ["O", "O", "O", "O"],
        ["O", "O", "O", "O"],
        ["O", "O", "O", "O"],
        ["O", "O", "O", "O"],
        ["O", "O", "O", "O"],
        ["O", "O", "O", "O"],
        ["O", "O", "O", "O"],
        ["O", "O", "O", "O"],
        ["O", "O", "O", "O"],
        ["O", "O", "O", "O"],
        ["O", "O", "O", "O"]
    ]

    with open(fileName, newline='') as file:
        for line in file:
            x, r, c, y = line.strip().split(', ')
            row = int(r)
            column = int(c)
            data[row][column] = "X"
            
        return data
    

def get_cost_matrix():
    cost_matrix = [[100, 75, 50, 100] for row in range(12)]
    return cost_matrix

def calc_price(bus_data):
    cost_matrix = get_cost_matrix()
    total = 0
    for r in range(0,12):
        for c in range(0,4):
            if bus_data[r][c] == 'X':
                total = total + cost_matrix[r][c]
    return total


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
    
@app.route('/reservations', methods=['GET', 'POST'])
def reservations():
    
    if request.method == 'POST':
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        row = request.form['row']
        seat = request.form['seat']
        
        if valid_reservation(first_name, last_name, row, seat):
            # generate e-ticket and add to reservations.txt
            # if a valid reservation
            valid, eticket = add_reservation(first_name, last_name, row, seat)
            if valid:
                flash(f'Reservation successful. Here is your e-ticket number: {eticket}')
            else:
                flash('Seat is taken, please pick again.')
            return redirect(url_for('reservations'))

    bus_data = make_Bus_Data('reservations.txt')

    return render_template('reservations.html', bus_data=bus_data)

def valid_reservation(first_name: str, last_name: str, row: str, seat: str) -> bool:
    valid = True

    if not first_name:
        valid = False
        flash('First name is required.')
    if not last_name:
        valid = False
        flash('Last name is required.')
    if not row:
        valid = False
        flash('Row is required.')
    if not seat:
        valid = False
        flash('Seat is required.')

    # check if seat is already taken
    
    return valid

def add_reservation(first_name: str, last_name: str, row: str, seat: str) -> (bool, str):
    try:
        data = make_Bus_Data('reservations.txt')

        row = int(row)
        seat = int(seat)

        # seat taken
        if data[row][seat] == "X":
            return False, ''

        # Truman, 1, 0, TIrNuFmOaTnC4320
        # generate e-ticket number by mixing first name with INFOTC4320
        e_ticket = ''.join([first_name[i] + 'I' + 'N' + 'F' + 'O' + 'T' + 'C' + '4' + '3' + '2' + '0' for i in range(len(first_name))])

        # add reservation to file
        with open('reservations.txt', 'a') as file:
            file.write(f'{first_name}, {row}, {seat}, {e_ticket}\n')
        
        return True, e_ticket
    except Exception as e:
        raise Exception(f'Error adding reservation: {e}')

# start the flask app
app.run(host=HOST)
