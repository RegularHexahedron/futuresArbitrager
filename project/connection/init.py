# connection/init_env.py

"""
Eestablishes conection with the exchange services.
"""

from pyRofex import initialize, set_default_environment
from utils.config import USER, PASSWORD, ACCOUNT, ENVIRONMENT

def establish_connection():
    """
    Initializes the connection with MATBA–ROFEX's authentication server and
    Sets up default envirnonment.
    """

    initialize(
        user = USER,
        password = PASSWORD,
        account = ACCOUNT,
        environment = ENVIRONMENT
    )

    set_default_environment(ENVIRONMENT)