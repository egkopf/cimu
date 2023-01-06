from flask import Flask, request, make_response, redirect, url_for, render_template, session, redirect
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from userResources import db, Users, UserForm, LoginForm, OrderForm
from datetime import datetime
import flask_login
import model
from sql_queries import DELETE_ORDER
import sqlite3
from cryptography.fernet import Fernet

def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)

def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)

# -----------------------------------------------------------------------

app = Flask(__name__, template_folder='.')
app.config['SECRET_KEY'] = 'nel mezzo del cammin di nostra vita'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

key = '81HqDpbqAywKDOumSpa3BhWNOdQe6slT6K3YaZeZyPs='

db.init_app(app)


login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))

#rendering the HTML page which has the button
@app.route('/orderupdate', methods=['GET'])
def orderUpdate():
    orderid = int(request.args.get('orderid'))
    print(orderid)
    buttonAction = request.args.get('buttonAction')

    if buttonAction == "accept":
        print("helloo")
        model.update_order_status_confirm((orderid,))
    else:
        model.update_order_status_deny((orderid,))

    return redirect(url_for('orders'))



@app.route('/login', methods=['GET', 'POST'])
def login():

    name = None
    form = LoginForm()

    if request.method == 'GET':
        html = render_template('Templates/login.html', form=form, name=name, errmsg="")
        response = make_response(html)
        return response

    if form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')

        user = Users.query.filter_by(Email=email).first()
        if user != None:
            if decrypt(user.Password, key).decode() == password:

                print(user)

                flask_login.login_user(user)
                model.CURRENT_USER_TYPE = user.UserType

                html = render_template('Templates/index.html')
                response = make_response(html)
                return response

            else: # incorrect password
                return render_template('Templates/login.html', errmsg=model.ERRMSG_INVALIDPASSWORD, form=form, name=name)

        else: # no user with matchin email exists
            return render_template('Templates/login.html', errmsg=model.ERRMSG_NOUSER, form=form, name=name)

    else: # form was syntatically not filled out correctly
        return render_template('Templates/login.html', errmsg=model.ERRMSG_FORMERRORNAME, form=form, name=name)

@app.route('/createaccount', methods=['GET', 'POST'])
def createAccount():

    name = None
    form = UserForm()

    if request.method == 'GET':
        html = render_template('Templates/createaccount.html', errmsg="", form=form, name=name)
        response = make_response(html)
        return response

    if form.validate_on_submit():

        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')
        userType = request.form.get('userType')

        user = Users.query.filter_by(Email=email).first()

        if user is not None:
            # a user with that email already exists
            return render_template('Templates/createaccount.html', errmsg=model.ERRMSG_EXISTINGUSER, form=form, name=name)

        if password != confirmPassword:
            # pass mismatch
            return render_template('Templates/createaccount.html', errmsg=model.ERRMSG_PASSMISMATCH, form=form, name=name)

        id = abs(hash(form.email.data))
        Name = form.name.data
        Email = str.lower(form.email.data)
        Password = form.password.data
        UserType = form.userType.data

        user = Users(id= id, Name = Name, Email = Email, Password = encrypt(Password.encode(), key), UserType = UserType)
        db.session.add(user)
        db.session.commit()

        tuple_to_add = (id, Name, Email, encrypt(Password.encode(), key), UserType)
        model.add_value_to_table(tuple_to_add, "user")

        flask_login.login_user(user)

        if UserType == 'tailor':
            return redirect(url_for('tailorpage'))

        html = render_template("Templates/index.html")
        response = make_response(html)
        return response

    return render_template('Templates/createaccount.html', errmsg=model.ERRMSG_FORMERRORNAME, form=form, name=name)

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return make_response(render_template("Templates/index.html"))

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET','POST'])
def home():
    print(flask_login.current_user.get_id())
    html = render_template("Templates/index.html")
    response = make_response(html)
    return response

@app.route('/tailorpage', methods=['GET', 'POST'])
def tailorpage():
    if request.method == 'GET':
        html = render_template("Templates/tailorpage.html")
        response = make_response(html)
        return response

    if request.method == 'POST':
        company_name = request.form.get("company")
        phonenumber = request.form.get("number")
        address = request.form.get("address")
        url = request.form.get("url")
        rating = 1


        info_to_add = (flask_login.current_user.Name, flask_login.current_user.id, company_name, address, phonenumber, flask_login.current_user.Email, url, rating)

        model.add_tailor_to_db(info_to_add=info_to_add)
        html = render_template("Templates/index.html")
        response = make_response(html)
        return response

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():



    if request.method == 'GET':
        tailorid = request.args.get('tailorid')
        form = OrderForm(tailorid = tailorid)
        companyname = request.args.get('companyname')
        html = render_template('Templates/schedule.html', form = form, company_name=companyname, tailorid=tailorid)
        response = make_response(html)
        return response

    if request.method == 'POST':
        description = request.form.get("description")
        tailorname = request.form.get("tailorname")
        tailorid = request.form.get("tailorid")
        userid = flask_login.current_user.get_id()
        status = "PENDING"

        tuple_to_add = (tailorid, userid, description, None, status)

        model.add_value_to_table(tuple_to_add, "orders")
        model.send_order_confirmation_email(flask_login.current_user.Email, "Cimu: Order Confirmation!", (tailorname, description, status))

        return redirect(url_for('orders'))


@app.route('/about', methods=['GET'])
def about():
    if request.method == 'GET':
        html = render_template('Templates/about.html')
        return make_response(html)

@app.route('/database', methods=['POST','GET'])
def database():
    if request.method == 'POST':
        zipcode = request.form.get('zipcode')
        company = request.form.get('company')
        rating = request.form.get('rating')

        args_dict = {"zipcode": zipcode, "company": company, "rating": rating}
        output = model.handle_client(args_dict)

        html = render_template('Templates/database.html',
            results = output,
            company = company,
            zipcode = zipcode,
            rating = rating
        )

        return make_response(html)

    if request.method == 'GET':
        html = render_template('Templates//database.html')

        return make_response(html)

@app.route('/searchresults', methods=['GET'])
def search_results():

    zipcode = request.args.get('zipcode')
    company = request.args.get('company')
    rating = request.args.get('rating')

    args_dict = {"zipcode": zipcode, "company": company, "rating": rating}
    output = model.handle_client(args_dict)

    if len(output) == 0:
        html = 'Sorry, no tailors found.'
        return make_response(html)

    html = '''
    <div class="table">
    '''

    pattern = '''
        <div class = "tailor" onclick="window.location='schedule?tailorid=%s&companyname=%s';">
            <p class=tailorid style="display:none;">%s</p>
            <div class="tailor-info">
                <h3>%s</h3>
                <p>%s</p>
            </div>
            <div class="tailor-info2">
                <p style="display:none;">%s</p>
                <p align="left">%s</p>
                <p align="left"> Rating:

    '''

    for tailor in output:
        print(tailor[3]) # add a row to the table for each book in db
        html += pattern % tuple(
            [tailor[0],
            tailor[3].replace(" ", "+").replace("'","%27"),
            tailor[0],
            tailor[1],
            tailor[3],
            tailor[5],
            tailor[4]]
            )
        for k in range(tailor[8]):
            html += "🧵"
        html += "</p>"
        html += "</div>"
        html += "</div>"


    response = make_response(html)
    return response

@app.route('/orders', methods=['GET'])
@flask_login.login_required
def orders():
    if request.method == 'GET':

        if flask_login.current_user.UserType == "tailor":
            userid = int(flask_login.current_user.get_id())
            print(userid)
            tailorid = model.get_tailor_id((userid,))
            print(tailorid)

            orders = model.get_tailor_orders((tailorid[0][0],))

            html = render_template('Templates/orders.html', name=flask_login.current_user.Name, orders=orders)
            response = make_response(html)
            return response

        if flask_login.current_user.UserType == "customer":
            userid = int(flask_login.current_user.get_id())
            print(userid)

            orders = model.get_customer_orders((userid,))

            html = render_template('Templates/orders.html', name=flask_login.current_user.Name, orders=orders)
            response = make_response(html)
            return response


if __name__ == '__main__':
    app.run()
