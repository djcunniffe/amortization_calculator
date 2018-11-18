# views.py

from flask import render_template, request, flash

from app import app
from app import amor
import numpy as np
import pandas as pd
import datetime as dt

@app.route('/')
def index():
    return render_template('index.html')

def calculate(amount,interest,months,currency):
    """
    Take inputs, caluclate and display the new monthly payment
    """
    pmt = -round(np.pmt(interest/12, months, amount),2)
    flash('The New Payment is: %s %s' % (currency, '{:0,.2f}'.format(pmt)))
    return render_template('index.html')

def schedule(amount,interest,date,months,currency):
    """
    Take the inputs and output the amortization schedule
    """
    schedule_df = pd.DataFrame(amor.amortize(amount,interest,months,"compound",currency,start_date=dt.datetime.strptime(date,"%Y-%m-%d").date()))

    return render_template('schedule.html', data=schedule_df.to_html(index=False,classes='table table-hover table-responsive'))

@app.route('/', methods=['GET','POST'])
def display():
    
    amount = float(request.form['amount'])
    interest = float(request.form['interest'])/100
    date = request.form['cycle']
    months = int(request.form['months'])
    currency = request.form['currency']

    if request.method == 'POST':
        if request.form['submit'] == 'Calculate':
            return calculate(amount,interest,months,currency)
        elif request.form['submit'] == 'Generate Schedule':
            return schedule(amount,interest,date,months,currency)
    elif request.method == 'GET':
        return render_template('index.html')