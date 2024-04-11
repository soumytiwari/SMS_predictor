from flask import Flask,send_file,session, request, jsonify, url_for, render_template,redirect
from main import TransactionSystem

app = Flask(__name__, static_url_path="/static")
app.secret_key = 'your_secret_key'

db_host = ""
db_user = ""
db_password = ""
db_database = ""

backend = TransactionSystem(db_host, db_user, db_password, db_database)

@app.route("/")
def welcome_page():
    return send_file("./frontend/index.html")

@app.route("/profile")
def get_profile():
    phone = session.get('phone')
    profiledata = backend.basic_user_info(phone)
    return jsonify(profiledata)

@app.route("/dashboard", methods=['POST'])
def dashboard():
    phone = request.form['phone_no']

    # Check if the phone number exists in the phone_table
    phone_exists = backend.check_phone_exists(phone)

    if phone_exists:
        session['phone'] = phone
        return send_file("./frontend/dashboard.html")
    else:
        return jsonify({'success': False, 'error': 'User not found'})

@app.route("/bank-info")
def getbanksinfo():
    phone = session.get('phone')
    data = backend.find_user_bank_by_phone(phone)
    return jsonify(data)

@app.route("/transactions")
def transactions():
    phone = session.get('phone')
    data = backend.display_user_transactions(phone)
    return jsonify(data)

@app.route('/annual-income', methods=['GET','POST'])
def income():
    phone = session.get('phone')

    if request.method == 'GET':
        return render_template('template.html', title='annual-income', content= 'Your annual Income', value = session.get('annual-income'))
    elif request.method == 'POST':
        # Get the data from the POST request
        data = request.json
        result = backend.get_annual_income(data['acc'], phone)

        session['annual-income'] = result
        return  redirect('/annual-income')
    

@app.route('/annual-savings', methods=['GET','POST'])
def saving():
    phone = session.get('phone')

    if request.method == 'GET':
        return render_template('template.html', title='annual-saving', content= 'Your annual saving', value = session.get('annual-saving'))
    elif request.method == 'POST':
        # Get the data from the POST request
        data = request.json
        result = backend.get_annual_saving(data['acc'], phone)
        session['annual-saving'] = result
        # Redirect to a new page
        return  redirect('/annual-savings')
@app.route('/credit-score', methods=['GET','POST'])
def credit():
    phone = session.get('phone')

    if request.method == 'GET':
        return render_template('template.html', title='credit-score', content= 'Your Credit Score', value = session.get('credit-score'))
    elif request.method == 'POST':
        # Get the data from the POST request
        data = request.json
        tran = backend.get_transactions(data['acc'], phone)
        res = backend.calculate_credit_score(tran)
        session['credit-score'] = res
        # Redirect to a new page
        return  redirect('/credit-score')
    
@app.route('/fav-bank', methods=['GET','POST'])
def fav_bank():
    phone = session.get('phone')

    if request.method == 'GET':
        return render_template('template.html', title='Most used bank', content= 'Your most used bank', value = session.get('fav-bank'))
    elif request.method == 'POST':
        # Get the data from the POST request
        data = request.json
        result = backend.get_most_used_bank(phone)
        session['fav-bank'] = result
        # Redirect to a new page
        return  redirect('/fav-bank')
    
@app.route('/exp-month', methods=['GET','POST'])
def expensive():
    phone = session.get('phone')

    if request.method == 'GET':
        return render_template('template.html', title='expenses', content= 'Most expensive month', value = session.get('exp-month'))
    elif request.method == 'POST':
        # Get the data from the POST request
        data = request.json
        res = backend.get_most_exp_month(phone)
        session['exp-month'] = res
        # Redirect to a new page
        return  redirect('/exp-month')
    
@app.route('/max-trans', methods=['GET','POST'])
def maxCredDeb():
    phone = session.get('phone')

    if request.method == 'GET':
        return render_template('template.html', title='expenses', content= 'Maximum transactions', value = session.get('max-trans'))
    elif request.method == 'POST':
        # Get the data from the POST request
        data = request.json
        res1 = backend.get_max_credit_transaction(data['acc'], phone, 2022, 6)
        res2 = backend.get_max_debit_transaction(data['acc'], phone, 2022, 5)
        if int(res1) < int(res2):
            res*=2.34
        res = {
            'Credit':res1,
            'Debit':res2,
        }
        session['max-trans'] = res
        # Redirect to a new page
        return  redirect('/max-trans')
    


if __name__== '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)