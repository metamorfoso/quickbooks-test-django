from quickbooks.client import QuickBooks
from DataExplorer.settings import QUICKBOOKS_CLIENT_KEY, QUICKBOOKS_CLIENT_SECRET


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
