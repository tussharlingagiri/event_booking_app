from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with your own secret key

# Function to initialize the database and create the events table
def initialize_database():
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_date TEXT NOT NULL,
                lunch_dinner TEXT NOT NULL,
                event_type TEXT NOT NULL,
                floor TEXT NOT NULL,
                event_cost INTEGER NOT NULL,
                maintenance TEXT NOT NULL,
                adv_received INTEGER NOT NULL,
                members INTEGER NOT NULL
                )''')
    conn.commit()
    conn.close()

# Function to fetch all events from the database
def get_all_events():
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute('SELECT * FROM events')
    events = c.fetchall()
    conn.close()
    return events

# Function to add a new event to the database
def add_event(event_data):
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute('''INSERT INTO events (event_date, lunch_dinner, event_type, floor, event_cost, maintenance, adv_received, members)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', event_data)
    conn.commit()
    conn.close()

# Function to fetch a specific event by its ID
def get_event_by_id(event_id):
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute('SELECT * FROM events WHERE id = ?', (event_id,))
    event = c.fetchone()
    conn.close()
    return event

# Function to update an existing event in the database
def update_event(event_id, event_data):
    conn = sqlite3.connect('events.db')
    c = conn.cursor()
    c.execute('''UPDATE events SET event_date=?, lunch_dinner=?, event_type=?, floor=?, 
                event_cost=?, maintenance=?, adv_received=?, members=? WHERE id=?''', (*event_data, event_id))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    events = get_all_events()
    return render_template('index.html', events=events)

@app.route('/add_event', methods=['GET', 'POST'])
def add_event_page():
    if request.method == 'POST':
        event_data = (
            request.form['event_date'],
            request.form['lunch_dinner'],
            request.form['event_type'],
            request.form['floor'],
            int(request.form['event_cost']),
            request.form['maintenance'],
            int(request.form['adv_received']),
            int(request.form['members'])
        )
        add_event(event_data)
        return redirect(url_for('index'))
    return render_template('add_event.html')

@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event_page(event_id):
    event = get_event_by_id(event_id)
    print(event)  # Add this line for debugging
    if request.method == 'POST':
        event_data = (
            request.form['event_date'],
            request.form['lunch_dinner'],
            request.form['event_type'],
            request.form['floor'],
            int(request.form['event_cost']),
            request.form['maintenance'],
            int(request.form['adv_received']),
            int(request.form['members'])
        )
        print(event_data)  # Add this line for debugging
        update_event(event_id, event_data)
        return redirect(url_for('index'))
    return render_template('edit_event.html', event=event)


if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)


