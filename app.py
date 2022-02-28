from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticketsdatabase.db'
db = SQLAlchemy(app)

class Ticket(db.Model):
    TicketID = db.Column(db.Integer(), primary_key = True)
    TransportCompany = db.Column(db.String(), nullable = False)
    TransportType = db.Column(db.String(), nullable = False)
    StartTime = db.Column(db.String(), nullable = False)
    ArrivalTime = db.Column(db.String(), nullable = False)
    Price = db.Column(db.Float(), nullable = False)
    PickUpLocation = db.Column(db.String(), nullable = False)
    Destination = db.Column(db.String(), nullable = False)
    NumberOfAvailableTickets = db.Column(db.Integer(), nullable = False)
    NumberOfPurchasedTickets = db.Column(db.Integer(), nullable = False)

@app.route('/')
def purchase_tickets():
    tickets = Ticket.query.all()
    return render_template('purchase_tickets.html', tickets = tickets)

