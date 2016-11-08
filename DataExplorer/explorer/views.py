from django.shortcuts import render, redirect
from quickbooks.client import QuickBooks
from quickbooks.objects.account import Account
from quickbooks.objects.customer import Customer
from DataExplorer.settings import QUICKBOOKS_CLIENT_KEY, QUICKBOOKS_CLIENT_SECRET, CALLBACK_URL
from .helpers import open_qbo_connection


def index(request):
    """
    Landing page for the app.
    :param request:
    :return HttpResponse:
    """
    context = dict()

    # When authenticated, connect to QBO and update the context with basic connection info
    if 'access_token' in request.session:
        # Open connection
        client = open_qbo_connection(request)
        # Update the context
        context.update(dict(
            connected=True,
            company_id=client.company_id,
        ))

    # Render to template with the context, whether connected or not
    return render(request, 'explorer/index.html', context)


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


# Series of views for querying QBO on specific data and displaying them
def all_accounts(request):
    """
    View all accounts associated with the company.
    :param request:
    :return HttpResponse:
    """
    if 'access_token' in request.session:
        # Open connection
        client = open_qbo_connection(request)
        # Prepare context with all accounts
        context = dict(
            connected=True,
            all_accounts=Account.all(qb=client),
            customers=Customer.all(qb=client)
        )
        return render(request, 'explorer/all_accounts.html', context)


def single_account(request, account_id):
    """
    View a specific account.
    :param request:
    :param account_id:
    :return HttpResponse:
    """
    if 'access_token' in request.session:
        # Open connection
        client = open_qbo_connection(request)
        account = Account.get(id=account_id, qb=client)

        context = dict(
            connected=True,
            account=account,
            description=account.Description,
            current_balance=account.CurrentBalance
        )
        return render(request, 'explorer/single_account.html', context)