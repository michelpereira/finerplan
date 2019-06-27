from datetime import date, datetime
from dateutil.relativedelta import *

from config import date_model, UserInfo


def date_converter(_date):
    if type(_date) == str:
        _date = datetime.strptime(_date, date_model).date()
    elif type(_date) == date:
        _date = _date
    else:
        raise Exception('Wrong Date Type: {}'.format(type(_date)))
    return _date


def cash(_date):
    """Returns the date when a certain expense will be
    paid (cash date) for a given date instance (usually
    accrual date) according to the app's date for
    closing the invoice.
    """
    _date = date_converter(_date)
    cash_date = _date.replace(day=UserInfo.CREDIT_PAYMENT)
    if _date.day > UserInfo.CREDIT_CLOSING:
        cash_date = cash_date + relativedelta(months=1)
    return cash_date


def credit_state():
    if ((date.today().day > UserInfo.CREDIT_CLOSING)
            and (date.today().day < UserInfo.CREDIT_PAYMENT)):
        return True
    else:
        return False


def sdate():
    """Creates a dictionary of special dates that is
    updated everytime one of these dates is required
    """

    SOCM = date.today().replace(day=1)  # Start Of Current Month
    EOM = date.today() + relativedelta(day=31)  # End Of [current] Month
    SOM = date.today() + relativedelta(months=1, day=1)  # Start Of [next] Month
    # Date of credit card's next payment
    NEXT_PAY = date.today().replace(day=UserInfo.CREDIT_PAYMENT)
    if date.today().day >= UserInfo.CREDIT_PAYMENT:
        NEXT_PAY = NEXT_PAY + relativedelta(months=1)
    FOLLOWING_NEXT_PAY = NEXT_PAY + relativedelta(months=1)
    MONTH_PROGRESS = date.today().day / EOM.day

    return {'TODAY': date.today(),
            'SOCM': SOCM,
            'EOM': EOM,
            'SOM': SOM,
            'M_PROGRESS': MONTH_PROGRESS,
            'NEXT_PAY': NEXT_PAY,
            'FOLLOWING_NEXT_PAY': FOLLOWING_NEXT_PAY}
