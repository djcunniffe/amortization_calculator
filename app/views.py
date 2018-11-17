# views.py

from flask import render_template, request, flash

from app import app
from app import amor
import numpy as np

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
    amount = float(request.form['amount'])
    interest = float(request.form['interest'])
    date = request.form['cycle']
    months = int(request.form['months'])
    currency = request.form['currency']

    pmt = -round(np.pmt(interest/12, months, amount),2)
    flash('The New Payment is: %s %s' % (currency, '{:0,.2f}'.format(pmt)))
    return render_template('index.html')
    # 'Testing : Amount %s Interest %s Date %s Months %s New Payment %s' % (amount, interest, date, months, pmt)