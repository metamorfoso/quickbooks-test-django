v1.0

Quickbooks Online Data Explorer
===============================

Application for connecting to Quickbooks Online and exploring a company's data.

Quick Setup Guide
=================
- (Optional) Use a virtual environment
- Install Python 3.5
- Install pip
- Clone repo
- Navigate to project root (quickbooks-test-django/DataExplorer)
- Install dependencies: `pip install -r requirements.txt`
- Apply migrations: `python manage.py migrate`
- Run local django server: `python manage.py runserver`

Notes
=====
The project is not yet feature-complete. Currently, it allows users to query and read, but
create and update are WIP.

Error handling and validation is very minimal at the moment, as is test coverge.

In general, a series of TODO comments describe the intention of as-yet incomplete parts of the project.
