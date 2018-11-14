import pandas as pd
import numpy as np 
import datetime as dt 
import matplotlib as plt
from collections import OrderedDict
from dateutil.relativedelta import *

def simple_pmt(rate, nper, pv, fv=0, when='end'):

    pmt = (pv * rate * (1+rate)*nper)/((1+rate)*nper-1)
    return -pmt


def amortize(principle, interest_rate, years, type, addl_principle=0, annual_payments=12, start_date = dt.date.today()):
    
    if type ==  'compound':
        pmt = -round(np.pmt(interest_rate/annual_payments, years*annual_payments, principle),2)
    if type == 'simple':
        pmt = -round(simple_pmt(interest_rate/annual_payments, years*annual_payments, principle),2)
    

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
                            ('Begin Balance',beg_balance),
                            ('Payment', pmt),
                            ('Principle', principle),
                            ('Interest',interest),
                            ('Additional_Payment',addl_principle),
                            ('End Balance',end_balance)])

        #Increment the counter, balance and date
        p += 1
        start_date += relativedelta(months=1)
        beg_balance = end_balance

schedule1 = pd.DataFrame(amortize(50000, 0.04, 20, 'simple', addl_principle=200, start_date=dt.date(2016, 1,1)))
schedule2 = pd.DataFrame(amortize(50000, 0.04, 20, 'compound', addl_principle=200, start_date=dt.date(2016, 1,1)))
#print(schedule1,schedule2)
#schedule.to_csv('schedule.csv')
schedule2.plot(y=['Interest','Principle'], x='Month')
plt.pyplot.savefig('test2.png')
schedule1.plot(y=['Interest','Principle'], x='Month')
plt.pyplot.savefig('test.png')

schedule1.plot(y=['End Balance'], x='Month')
plt.pyplot.savefig('test3.png')

spmt = simple_pmt(rate =0.04/12,nper=30*12,pv=50000)
cpmt = np.pmt(0.04/12,30*12,50000)
print(spmt,cpmt)