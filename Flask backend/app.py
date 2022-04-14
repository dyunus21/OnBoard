import os
import uuid
from flask import Flask, render_template, redirect, url_for, request,flash,g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from sqlalchemy.sql import func
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SubmitField, IntegerField, FloatField, EmailField
from flask_login import LoginManager, login_user,logout_user, login_required,current_user
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
# import flask_UUID
from flask_uuid import FlaskUUID

# from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# from flask_login import UserMixin

# Configure app and SQL Alchemy
app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticketsdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'aiuhewr9y9q2392304iuahi3'
#Email related Configuration values
mail= Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = '*****REPLACE WITH EMAIL ADDRESS******'
app.config['MAIL_PASSWORD'] = '*****REPLACE WITH APP PASSWORD********'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
# login_manager = LoginManager(app) 

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


FlaskUUID(app)
# #User Creation Class
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(), nullable = False, unique = True)
    emailAddress = db.Column(db.String(), nullable = False)
    passwordHash = db.Column(db.String(), nullable = False)
    points = db.Column(db.Integer(), nullable = False, default = 0)
    userType = db.Column(db.Integer(), nullable = False)
    tickets = db.relationship('Ticket', backref="user", lazy = True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


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

# Discount Class
class Discount(db.Model):
    DiscountID = db.Column(db.Integer(), primary_key = True)
    Business = db.Column(db.String(), nullable = False)
    Amount = db.Column(db.Float(), nullable = False)
    ExpirationDate = db.Column(db.String(), nullable = False)
    MinPointsNecessary = db.Column(db.Integer(), nullable = False)

class RegisterAccount(FlaskForm):
    username = StringField(label = 'User Name')
    emailadd = StringField(label = 'Email Address')
    password = PasswordField(label = 'Password')
    typeofuser = RadioField(label = 'User Type', choices = [(0,'Individual'),(1,'Local Business')])
    submitted = SubmitField(label = 'Submit')

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user:
            # raise ValidationError('That username is taken. Please choose a different one.')

    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user:
    #         raise ValidationError('That email is taken. Please choose a different one.')

class LoginAccount(FlaskForm):
    username = StringField(label = 'User Name')
    password = PasswordField(label = 'Password')
    submitted = SubmitField(label = 'Submit')

class addPoints(FlaskForm):
    submitted = SubmitField(label = 'View Details')

class AddDiscount(FlaskForm):
    business = StringField(label = 'Name of Business')
    amount = FloatField(label = 'Percent Discount')
    expirationdate = StringField(label = 'Date of Expiration')
    minpoints = IntegerField(label = 'Minimum Number of Points Necessary')
    submitted = SubmitField(label = 'Submit')

class ForgotForm(FlaskForm):
    email = EmailField('Email address')
    submitted = SubmitField(label = 'Submit')
    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user is None:
    #         raise ValidationError('There is no account with that email. You must register first.')

class ResetForm(FlaskForm):
    password = PasswordField('Password',validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submitted = SubmitField('Reset Password')

# Routes to home page
@app.route('/')
def home():
    return render_template('index.html')

curr_points = 0

# Routes to account registration page
@app.route('/accregister', methods = ['GET', 'POST'])
def account_registration():
    global curr_points
    form = RegisterAccount()
    if form.validate_on_submit():
        u_curr = User(username = form.username.data, emailAddress = form.emailadd.data, passwordHash = form.password.data, userType = form.typeofuser.data)
        try:
            db.session.add(u_curr)
            db.session.commit()
            curr_points = 0
            if(u_curr.userType==0):
                return redirect(url_for('purchase_tickets', points = curr_points))
            else:
                return redirect(url_for('business_dashboard'))       
        except exc.IntegrityError:
            db.session.rollback()
            flash('ERROR! User ({}) already exists.'.format(form.username.data), 'error')
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
            # login_user(u_attempt)
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

# sends reset email with url
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='yourId@gmail.com',
                  recipients=[user.emailAddress])
    msg.body = f'''Click on the following link to reset your password:
{url_for('reset_token', token=token, _external=True)}
# '''
    mail.send(msg)

# Generates a random url for password reset
@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    # if current_user.is_authenticated:
    #     return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetForm()
    if request.method == 'POST':
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('account_login'))
    return render_template('reset.html', title='Reset Password', form=form)

# Routes to forgot password
@app.route('/forgot_password', methods = ('GET','POST'))
def forgot_password():
    
    form = ForgotForm()
    if request.method == 'POST':
        user = User.query.filter_by(emailAddress=form.email.data).first()
        # # # flash(user.emailAddress)
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.')
        return redirect(url_for('account_login'))

    return render_template('forgot.html', form = form)

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


curr_ticket = ""
@app.route('/display_tickets', methods = ['GET', 'POST'])
def display_tickets():
    global curr_points
    confirm_purchase = addPoints()
    if request.method == 'POST':
        ticket_chosen = request.form.get('confirm_purchase')
        global curr_ticket 
        curr_ticket= Ticket.query.filter_by(TicketID = ticket_chosen).first()
        if curr_ticket:
            curr_points += 5
            curr_ticket.NumberOfPurchasedTickets += 1
            db.session.commit()
            tickets = Ticket.query.all()
            return redirect(url_for('item_view', ticket = curr_ticket))
    tickets = Ticket.query.all()
    return render_template('display_tickets.html', tickets = tickets, confirm_purchase = confirm_purchase)

@app.route('/item_view')
def item_view():
    ticket = curr_ticket
    return render_template('itemview.html', ticket = ticket)

# Routes to user dashboard page
@app.route('/user_dashboard')
def user_dashboard():
    return render_template('user_dashboard.html')

# Routes to checkout page
@app.route('/checkout')
def checkout():
    tickets = Ticket.query.all()
    sum =0
    count = 0
    for ticket in tickets:
        sum +=ticket.Price
        count+=1
    # sum = db.session.query(func.max(Ticket.Price).label("max_score"))
    return render_template('checkout_page.html',tickets = tickets, sum = sum, count = count)

# Routes to local business dashboard
@app.route('/business_dashboard', methods = ['GET', 'POST'])
def business_dashboard():
    form = AddDiscount()
    if form.validate_on_submit():
        d_curr = Discount(Business = form.business.data, Amount = form.amount.data, ExpirationDate = form.expirationdate.data, MinPointsNecessary = form.minpoints.data)
        db.session.add(d_curr)
        db.session.commit()
        return redirect(url_for('ad_display'))       
    return render_template('business_dashboard.html', form = form)


# Routes to ad display page
@app.route('/ad_display', methods = ['GET', 'POST'])
def ad_display():
    discounts = Discount.query.all()
    return render_template('ad_display.html', discounts = discounts)

