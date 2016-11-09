from quickbooks.client import QuickBooks
from DataExplorer.settings import QUICKBOOKS_CLIENT_KEY, QUICKBOOKS_CLIENT_SECRET

from quickbooks.objects.account import Account
from quickbooks.objects.attachable import Attachable
from quickbooks.objects.bill import Bill
from quickbooks.objects.billpayment import BillPayment
from quickbooks.objects.budget import Budget
from quickbooks.objects.company_info import CompanyInfo
from quickbooks.objects.creditmemo import CreditMemo
from quickbooks.objects.customer import Customer
from quickbooks.objects.department import Department
from quickbooks.objects.deposit import Deposit
from quickbooks.objects.employee import Employee
from quickbooks.objects.estimate import Estimate
from quickbooks.objects.invoice import Invoice
from quickbooks.objects.item import Item
from quickbooks.objects.journalentry import JournalEntry
from quickbooks.objects.payment import Payment
from quickbooks.objects.paymentmethod import PaymentMethod
from quickbooks.objects.purchase import Purchase
from quickbooks.objects.purchaseorder import PurchaseOrder
from quickbooks.objects.refundreceipt import RefundReceipt
from quickbooks.objects.salesreceipt import SalesReceipt
from quickbooks.objects.taxagency import TaxAgency
from quickbooks.objects.taxcode import TaxCode
from quickbooks.objects.taxrate import TaxRate
from quickbooks.objects.taxservice import TaxService
from quickbooks.objects.term import Term
from quickbooks.objects.timeactivity import TimeActivity
from quickbooks.objects.transfer import Transfer
from quickbooks.objects.vendor import Vendor
from quickbooks.objects.vendorcredit import VendorCredit


# Build dictionary of quickbook objects and matching entities
# TODO: rework this to be built programatically, based on the QUERIABLE_ENTITIES variable from settings
ENTITY_OBJECT_DICT = {
    'Account': Account,
    'Attachable': Attachable,
    'Bill': Bill,
    'BillPayment': BillPayment,
    'Budget': Budget,
    'CompanyInfo': CompanyInfo,
    'CreditMemo': CreditMemo,
    'Customer': Customer,
    'Department': Department,
    'Deposit': Deposit,
    'Employee': Employee,
    'Estimate': Estimate,
    'Invoice': Invoice,
    'Item': Item,
    'JournalEntry': JournalEntry,
    'Payment': Payment,
    'PaymentMethod': PaymentMethod,
    'Purchase': Purchase,
    'PurchaseOrder': PurchaseOrder,
    'RefundReceipt': RefundReceipt,
    'SalesReceipt': SalesReceipt,
    'TaxAgency': TaxAgency,
    'TaxCode': TaxCode,
    'TaxRate': TaxRate,
    'TaxService': TaxService,
    'Term': Term,
    'TimeActivity': TimeActivity,
    'Transfer': Transfer,
    'Vendor': Vendor,
    'VendorCredit': VendorCredit
}


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
    # Choose correct object from quickbooks library, based on provided entity
    return ENTITY_OBJECT_DICT[entity]
