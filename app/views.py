# views.py

from flask import render_template, request

from app import app


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/', methods=['GET','POST'])
def calculate():
    """
    Take inputs and caluclate the new payment
    """
    amount = request.form['amount']
    interest = request.form['interest']
    date = request.form['cycle']
    months = request.form['months']

    return 'Testing : Amount %s Interest %s Date %s Months %s ' % (amount, interest, date, months)