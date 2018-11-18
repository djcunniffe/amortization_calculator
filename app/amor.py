import pandas as pd
import numpy as np 
import datetime as dt 
import matplotlib as plt
from collections import OrderedDict
from dateutil.relativedelta import *

def simple_pmt(rate, nper, pv, fv=0, when='end'):

    pmt = (pv * rate * (1+rate)*nper)/((1+rate)*nper-1)
    return -pmt


def amortize(principle, interest_rate, months_left, type, currency, addl_principle=0, annual_payments=12, start_date = dt.date.today()):
    
    if type ==  'compound':
        pmt = -round(np.pmt(interest_rate/annual_payments, months_left, principle),2)
    if type == 'simple':
        pmt = -round(simple_pmt(interest_rate/annual_payments, months_left, principle),2)
    

    #initialize the variables to keep track of the periods and running balances
    p = 1
    beg_balance = principle
    end_balance = principle

    while end_balance >0:

        #Recalculate the interest based on the current balance
        if type == 'compound':
            interest = round(((interest_rate/annual_payments) * beg_balance),2)
        if type == 'simple':
            interest = round(((interest_rate/annual_payments) * beg_balance),2)

        #Determine payment based on whether or not this period will pay off the loan
        pmt = min(pmt, beg_balance + interest)
        principle = pmt - interest

        #Ensure additional payment gets adjusted if the loan is being paid off
        addl_principle = min(addl_principle, beg_balance - principle)
        end_balance = beg_balance - (principle + addl_principle)
        #principle -= principle_portion

        yield OrderedDict([('Month', start_date),
                            ('Period', p),
                            ('Opening Balance',beg_balance),
                            ('Payment', pmt),
                            ('Principle', principle),
                            ('Interest',interest),
                            ('Additional Payment',addl_principle),
                            ('Closing Balance',end_balance)])

        #Increment the counter, balance and date
        p += 1
        start_date += relativedelta(months=1)
        beg_balance = end_balance