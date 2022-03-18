# $flask init-db
# $flask run

import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# Configure app and SQL Alchemy
def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticketsdatabase.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    # Ticket Class
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

    # Routes to home page
    @app.route('/')
    def home():
        return render_template('base.html')

    # Routes to ticket page
    @app.route('/tickets')
    def purchase_tickets():
        tickets = Ticket.query.all()
        return render_template('purchase_tickets.html', tickets = tickets)

    # Imports content from authentication and 
    import auth
    app.register_blueprint(auth.bp)
    
    import user_db
    user_db.init_app(app)

    return app
