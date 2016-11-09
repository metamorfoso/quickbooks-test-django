from quickbooks.client import QuickBooks
from DataExplorer.settings import QUICKBOOKS_CLIENT_KEY, QUICKBOOKS_CLIENT_SECRET
from quickbooks.objects.account import Account
from quickbooks.objects.customer import Customer


def open_qbo_connection(request):
    """
    Helper function for connecting to QBO, when a view needs an instance of client. Relies on the session containing
    the access_token, access_token_secret, and company_id.
    :param request:
    :return client instance:
    """
    client = QuickBooks(
        sandbox=True,
        consumer_key=QUICKBOOKS_CLIENT_KEY,
        consumer_secret=QUICKBOOKS_CLIENT_SECRET,
        access_token=request.session['access_token'],
        access_token_secret=request.session['access_token_secret'],
        company_id=request.session['realm_id']
    )
    return client


def select_quickbooks_object(entity):
    """
    Helper function for selecting the correct object from the python-quickbooks library. Necessary because
    python-quickbooks' calls to the QBO are specific to a given entity (Account, Customer, etc), and are driven
    by the corresponding object in python-quickbooks. For example, if we want to make a custom SQL query to get
    active customers ("SELECT * FROM Customer WHERE Active = True") we need to do this via the Customer object like so:
    Customer.query("SELECT * FROM Customer WHERE Active = True", qb=client)
    This is documented on the python-quickbooks repo: https://github.com/sidecars/python-quickbooks
    :param entity:
    :return quickbooks object:
    """

    # TODO: Extend this to include all endpoints, not just Account and Customer
    # Build dictionary of quickbook objects and matching entities
    qb_object_and_entities = {
        'Account': Account,
        'Customer': Customer
    }

    # Choose correct object from quickbooks library, based on provided entity
    return qb_object_and_entities[entity]
