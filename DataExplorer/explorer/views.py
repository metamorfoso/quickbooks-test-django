from django.shortcuts import render, redirect, reverse, HttpResponse
from quickbooks.exceptions import QuickbooksException
from DataExplorer.settings import QUERIABLE_ENTITIES
from .helpers import open_qbo_connection, select_quickbooks_object
import json


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
            landing_page=True,  # slight hack so that template knows when to display nav elements
            connected=True,
            company_id=client.company_id,
            entities=QUERIABLE_ENTITIES
        ))

    # Render to template with the context, whether connected or not
    return render(request, 'explorer/index.html', context)


# Series of views for querying QBO on specific data and displaying them
def browse(request, entity):
    """
    Displays all instances of an entity (such as Account, Customer, Payment, etc) associated with the company.
    :param request:
    :param entity:
    :return HttpResponse:
    """
    if 'access_token' in request.session:
        # Open connection
        client = open_qbo_connection(request)
        # Get the right object from python-quickbooks
        qb_object = select_quickbooks_object(entity)
        # Prepare context with all accounts
        context = dict(
            connected=True,
            entity=entity,
            entity_queryset=qb_object.all(qb=client)
        )
        return render(request, 'explorer/browse.html', context)


def single_entity(request, entity, entity_id):
    """
    Displays a single instance of a given entity (e.g. a specific Account, or specific Customer).
    :param request:
    :param entity:
    :param entity_id:
    :return HttpResponse:
    """
    if 'access_token' in request.session:
        # Open connection
        client = open_qbo_connection(request)
        # Get correct python-quickbooks object
        qb_object = select_quickbooks_object(entity)
        # Hit QBO API to get correct instance of entity
        result = qb_object.get(id=entity_id, qb=client)

        # Prepare context and render to template
        context = dict(
            connected=True,
            entity=entity,
            entity_id=entity_id,
            result=result,
            result_json=result.to_json()
        )
        return render(request, 'explorer/single_entity.html', context)


def query(request):
    """
    Handles custom query of QBO API (such as "Select * From Account") and displays results on a separate page.
    :param request:
    :return HttpResponse:
    """
    # Handle custom query form submission
    if request.method == 'POST':
        # Check that a query has been submitted TODO: query validation
        if request.POST.get('query'):
            selected_entity = request.POST.get('entity')
            query = request.POST.get('query')

            # Get correct python-quickbooks object
            qb_object = select_quickbooks_object(selected_entity)
            # Open connection
            client = open_qbo_connection(request)

            query_response = qb_object.query(query, qb=client)
            result = map(lambda response_item: response_item.to_json(), query_response)

            context = dict(
                connected=True,
                result=result,
                query=query
            )
            return render(request, 'explorer/query_results.html', context)


def read(request):
    """
    Handles query for a specific entity instance by its ID (e.g. the Account with the ID 33). Gets the correct
    entity and ID and calls the single_entity view with these as arguments.
    :param request:
    :return call of single_entity view:
    """
    # Handle form submission
    if request.method == 'POST':
        # Check that an id has been submitted
        if request.POST.get('entity_id'):
            selected_entity = request.POST.get('entity')
            selected_entity_id = request.POST.get('entity_id')

            # Call single entity view
            return single_entity(request, selected_entity, selected_entity_id)


# TODO: update and create are not yet complete -- they currently raise API errors. Need debugging and fixing.
def update(request):
    # Handle form submission
    if request.method == 'POST':
        # Check that entity and id have been submitted
        if request.POST.get('entity') and request.POST.get('entity_id') and request.POST.get('json_data'):
            entity = request.POST.get('entity')
            entity_id = request.POST.get('entity_id')
            new_json_data = json.loads(request.POST.get('json_data'))

            # Open connection
            client = open_qbo_connection(request)
            # Get correct python-quickbooks object
            qb_object = select_quickbooks_object(entity)

            instance = qb_object.get(entity_id, qb=client)
            updated_instance = instance.from_json(new_json_data)

            try:
                updated_instance.save(qb=client)
            except QuickbooksException:
                return HttpResponse('Error updating the instance. Please make sure the data is correctly formatted.')

            return redirect(reverse('explorer:single_entity', args=(entity, entity_id,)))


def create(request):
    # Handle form submission
    if request.method == 'POST':
        if request.POST.get('create_json_data'):
            json_data = json.loads(request.POST.get('create_json_data'))
            selected_entity = request.POST.get('entity')
            # Open connection
            client = open_qbo_connection(request)
            # Get correct python-quickbooks object
            qb_object = select_quickbooks_object(selected_entity)

            fresh_instance = qb_object()
            new_instance = fresh_instance.from_json(json_data)
            new_instance.save(qb=client)

            return redirect('/')
