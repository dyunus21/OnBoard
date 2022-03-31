import os
from flask import Flask, render_template, redirect, url_for, request,flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SubmitField
from flask_login import LoginManager, login_user,logout_user, login_required

# Configure app and SQL Alchemy
app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticketsdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'aiuhewr9y9q2392304iuahi3'
db = SQLAlchemy(app)

# #User Creation Class
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(), nullable = False, unique = True)
    emailAddress = db.Column(db.String(), nullable = False, unique = True)
    passwordHash = db.Column(db.String(), nullable = False)
    points = db.Column(db.Integer(), nullable = False, default = 0)
    userType = db.Column(db.Integer(), nullable = False)
    tickets = db.relationship('Ticket', backref="user", lazy = True)

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
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

class RegisterAccount(FlaskForm):
    username = StringField(label = 'User Name')
    emailadd = StringField(label = 'Email Address')
    password = PasswordField(label = 'Password')
    typeofuser = RadioField(label = 'User Type', choices = [(0,'Individual'),(1,'Local Business')])
    submitted = SubmitField(label = 'Submit')

class LoginAccount(FlaskForm):
    username = StringField(label = 'User Name')
    password = PasswordField(label = 'Password')
    submitted = SubmitField(label = 'Submit')

class addPoints(FlaskForm):
    submitted = SubmitField(label = 'Confirm Purchase')

# Routes to home page
@app.route('/')
def home():
    return render_template('index.html')

curr_points = 0

# Routes to account registration page
@app.route('/accregister', methods = ['GET', 'POST'])
def account_registration():
    form = RegisterAccount()
    if form.validate_on_submit():
        u_curr = User(username = form.username.data, emailAddress = form.emailadd.data, passwordHash = form.password.data, userType = form.typeofuser.data)
        # If user already has an account
        if db.session.query(db.exists().where(User.username == u_curr.username)).scalar():
            flash('User is already registered')
            render_template('account_registration.html', form = form)
        db.session.add(u_curr)
        db.session.commit()
        if(u_curr.userType==0):
            return redirect(url_for('purchase_tickets', points = curr_points))
        else:
            return redirect(url_for('business_dashboard'))       
    return render_template('account_registration.html', form = form)

# Routes to account login page
@app.route('/acclogin', methods = ['GET', 'POST'])
def account_login():
    global curr_points
    form = LoginAccount()
    if form.validate_on_submit():
        u_attempt = User.query.filter_by(username = form.username.data).first()
        curr_points = u_attempt.points
        
        # if username and password is correct
        if u_attempt and form.password.data == u_attempt.passwordHash:
            login_user(u_attempt)
            if(u_attempt.userType==0):
                return redirect(url_for('purchase_tickets', points = curr_points))
            else:
                return redirect(url_for('business_dashboard'))

        # Error messages
        else:
            flash('Invalid Username or Password!')
    return render_template('account_login.html', form = form)

# logs out user
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('account_login'))

# Routes to forgot password
@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot.html')

# Routes to reset password
@app.route('/reset')
def reset():
    return render_template('reset.html')

# Routes to ticket page
@app.route('/tickets', methods = ['GET', 'POST'])
def purchase_tickets():
    global curr_points
    confirm_purchase = addPoints()
    if request.method == 'POST':
        ticket_chosen = request.form.get('confirm_purchase')
        curr_ticket = Ticket.query.filter_by(TicketID = ticket_chosen).first()
        if curr_ticket:
            curr_points += 5
            curr_ticket.NumberOfPurchasedTickets += 1
            db.session.commit()
            tickets = Ticket.query.all()
            return redirect(url_for('purchase_tickets', tickets = tickets, points = curr_points))
    tickets = Ticket.query.all()
    return render_template('purchase_tickets.html', tickets = tickets, points = curr_points, confirm_purchase = confirm_purchase)

# Routes to local business dashboard
@app.route('/business_dashboard')
def business_dashboard():
    return render_template('ad_display.html')


# Routes to user dashboard page
@app.route('/user_dashboard')
def user_dashboard():
    return render_template('user_dashboard.html')

# # Imports content from authentication and 
# import auth
# app.register_blueprint(auth.bp)
  
# import user_db
# user_db.init_app(app)
