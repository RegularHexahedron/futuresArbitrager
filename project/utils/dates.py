# utils/dates.py

"""
Datetimes utilities.
"""

SECONDS_PER_YEAR = 365 * 24 * 60 * 60
from datetime import datetime

def compute_time_to_maturity(maturity_date: datetime) -> float:
    """
    Computes time to maturity in years (float) from maturity date (datetime).
    
    :param maturity_date: maturity date of the future
    :type maturity_date: datetime
    :return: time to maturity (in years)
    :rtype: float
    """
    
    time_to_maturity_dt =  maturity_date - datetime.now()
    time_to_maturity = time_to_maturity_dt.total_seconds() / SECONDS_PER_YEAR
    
    return time_to_maturity




