from django.shortcuts import redirect, reverse
from quickbooks.client import QuickBooks
from DataExplorer.settings import QUICKBOOKS_CLIENT_KEY, QUICKBOOKS_CLIENT_SECRET, CALLBACK_URL
from explorer.helpers import open_qbo_connection


# Series of views for handling OAuth's authentication flow
def qb_connect(request):
    """
    Part of OAuth's flow. Sends a request to authenticate to QBO's authorize url.
    :param request:
    :return HttpResponseRedirect:
    """
    client = QuickBooks(
        sandbox=True,
        consumer_key=QUICKBOOKS_CLIENT_KEY,
        consumer_secret=QUICKBOOKS_CLIENT_SECRET,
        callback_url=CALLBACK_URL
    )

    authorize_url = client.get_authorize_url()
    request_token = client.request_token
    request_token_secret = client.request_token_secret

    # Store request token, request token secret and authorize url in the
    # session for use in the callback
    request.session['authorize_url'] = authorize_url
    request.session['request_token'] = request_token
    request.session['request_token_secret'] = request_token_secret

    return redirect(authorize_url)


def qb_callback(request):
    """
    Part of OAuth's flow. Handles the callback from QBO, with access token and realm ID.
    Stores access_token, access_token_secret and realmId as variables stored in session
    and redirects to index view.
    :param request:
    :return HttpResponseRedirect:
    """
    client = QuickBooks(
        sandbox=True,
        consumer_key=QUICKBOOKS_CLIENT_KEY,
        consumer_secret=QUICKBOOKS_CLIENT_SECRET
    )

    client.authorize_url = request.session['authorize_url']
    client.request_token = request.session['request_token']
    client.request_token_secret = request.session['request_token_secret']
    client.set_up_service()

    client.get_access_tokens(request.GET['oauth_verifier'])

    realm_id = request.GET['realmId']
    access_token = client.access_token
    access_token_secret = client.access_token_secret

    # Store variables in the session variables needed for API calls
    request.session['realm_id'] = realm_id
    request.session['access_token'] = access_token
    request.session['access_token_secret'] = access_token_secret

    return redirect('/')


def qb_disconnect(request):
    """
    Disconnects from QBO, clears the session and redirects to index.
    :param request:
    :return HttpResponseRedirect:
    """
    client = open_qbo_connection(request)
    client.disconnect_account()
    request.session.clear()
    return redirect('/')
