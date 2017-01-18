"Core classes and exceptions for lacrm"

from __future__ import print_function
import logging
import requests
import json
from utils import LacrmArgumentError, BaseLacrmError

logger = logging.getLogger(__name__)


class Lacrm(object):
    """Less Annoying CRM Instance

    An instance of Lacrm wraps a LACRM REST API session.
    """

    def __init__(
            self, user_code=None, api_token=None):
        self.user_code = user_code
        self.api_token = api_token

        self.payload = {'UserCode': self.user_code,
                        'APIToken': self.api_token}
        self.endpoint_url = 'https://api.lessannoyingcrm.com'

        # Mapping that allows us to parse different API methods' response
        # meaningfully
        self.api_method_responses = {'CreateContact': 'ContactId',
                                     'GetContact': 'Contact',
                                     'Search': 'Results',
                                     'GetPipelineReport': 'Result'}

    def api_call(func):
        """ Decorator calls out to the API for specifics API methods """

        def make_api_call(self, *args, **kwargs):
            api_method, parameters = func(self, * args, **kwargs)

            method_payload = self.payload
            method_payload['Function'] = api_method
            method_payload['Parameters'] = json.dumps(parameters)

            response = requests.post(self.endpoint_url,
                                     data=method_payload).json()

            if not response.get('Success'):
                raise BaseLacrmError(content='Unknown error occurred -- check'
                                     'https://www.lessannoyingcrm.com/account/'
                                     'api/ for more detailed information.')
            else:
                return response.get(self.api_method_responses.get(api_method))

        return make_api_call

    @api_call
    def search(self, term):
        """ Searches LACRM contacts for a given term """

        api_method = 'SearchContacts'
        parameters = {'SearchTerms': term}

        return api_method, parameters

    @api_call
    def add_contact_to_group(self, *args, **kwargs):
        """ Adds a contact to a group in LACRM """

        parameters = {}
        api_method = 'AddContactToGroup'

        for key, value in kwargs.items():
            parameters[key] = value

        return api_method, parameters

    @api_call
    def delete_contact(self, *args, **kwargs):
        """ Deletes a given contact from LACRM """

        parameters = {}
        api_method = 'DeleteContact'

        for key, value in kwargs.items():
            parameters[key] = value

        return api_method, parameters

    @api_call
    def get_contact(self, *args, **kwargs):
        """ Get all information in LACRM for given contact """

        parameters = {}
        api_method = 'GetContact'

        for key, value in kwargs.items():
            parameters[key] = value

        return api_method, parameters

    @api_call
    def create_contact(self, *args, **kwargs):
        """ Creates a new contact in LACRM for given """

        parameters = {}
        api_method = 'CreateContact'
        expected_parameters = ['FullName',
                               'Salutation',
                               'FirstName',
                               'MiddleName',
                               'LastName',
                               'Suffix',
                               'CompanyName',
                               'CompanyId',
                               'Title',
                               'Industry',
                               'NumEmployees',
                               'BackgroundInfo',
                               'Email',
                               'Phone',
                               'Address',
                               'Website',
                               'Birthday',
                               'CustomFields',
                               'assignedTo']

        for key, value in kwargs.items():
            parameters[key] = value

        self.__validator(parameters.keys(), expected_parameters)
        return api_method, parameters

    @api_call
    def edit_contact(self, *args, **kwargs):
        """ Edits a contact in LACRM for given """

        parameters = {}
        api_method = 'EditContact'
        expected_parameters = ['FullName',
                               'Salutation',
                               'FirstName',
                               'MiddleName',
                               'LastName',
                               'Suffix',
                               'CompanyName',
                               'ContactId',
                               'CompanyId',
                               'Title',
                               'Industry',
                               'NumEmployees',
                               'BackgroundInfo',
                               'Email',
                               'Phone',
                               'Address',
                               'Website',
                               'Birthday',
                               'CustomFields',
                               'assignedTo']

        for key, value in kwargs.items():
            parameters[key] = value

        self.__validator(parameters.keys(), expected_parameters)
        return api_method, parameters

    @api_call
    def create_pipeline(self, *args, **kwargs):
        """ Creates a new pipeline in LACRM for given contactid """

        parameters = {}
        api_method = 'CreatePipeline'
        expected_parameters = ['ContactId',
                               'Note',
                               'PipelineId',
                               'StatusId',
                               'Priority',
                               'CustomFields']

        for key, value in kwargs.items():
            parameters[key] = value

        self.__validator(parameters.keys(), expected_parameters)
        return api_method, parameters

    @api_call
    def update_pipeline(self, *args, **kwargs):
        """ Update a pipeline in LACRM """

        parameters = {}
        api_method = 'UpdatePipelineItem'
        expected_parameters = ['PipelineItemId',
                               'Note',
                               'StatusId',
                               'Priority',
                               'CustomFields']

        for key, value in kwargs.items():
            parameters[key] = value

        self.__validator(parameters.keys(), expected_parameters)
        return api_method, parameters

    @api_call
    def create_note(self, *args, **kwargs):
        """ Creates a new note in LACRM for a given contactid """

        parameters = {}
        api_method = 'CreateNote'
        expected_parameters = ['ContactId',
                               'Note',
                               'PipelineId',
                               'StatusId',
                               'Priority',
                               'CustomFields']

        for key, value in kwargs.items():
            parameters[key] = value

        self.__validator(parameters.keys(), expected_parameters)
        return api_method, parameters

    @api_call
    def create_task(self, *args, **kwargs):
        """ Creates a new task in LACRM """

        parameters = {}
        api_method = 'CreateTask'
        expected_parameters = ['ContactId',
                               'DueDate',  # YYYY-MM-DD
                               'Description',
                               'ContactId',
                               'AssignedTo']

        for key, value in kwargs.items():
            parameters[key] = value

        self.__validator(parameters.keys(), expected_parameters)
        return api_method, parameters

    @api_call
    def create_event(self, *args, **kwargs):
        """ Creates a new event in LACRM """

        parameters = {}
        api_method = 'CreateEvent'
        expected_parameters = ['Date',
                               'StartTime',
                               'EndTime',
                               'Name',
                               'Description',
                               'Contacts',
                               'Users']

        for key, value in kwargs.items():
            parameters[key] = value

        self.__validator(parameters.keys(), expected_parameters)
        return api_method, parameters

    @api_call
    def get_pipeline_report(self, *args, **kwargs):
        """ Grabs a pipeline_report in LACRM """

        parameters = {}
        api_method = 'GetPipelineReport'
        expected_parameters = ['PipelineId',
                               'SortBy',
                               'NumRows',
                               'Page',
                               'SortDirection',
                               'UserFilter',
                               'StatusFilter']

        for key, value in kwargs.items():
            parameters[key] = value

        self.__validator(parameters.keys(), expected_parameters)
        return api_method, parameters

    def getall_pipeline_report(self, pipeline_item_id, status=None):
        """ Grabs a pipeline_report in LACRM """

        continue_flag = True
        page = 1
        output = []

        while continue_flag:

            params = {'PipelineId': pipeline_item_id,
                      'NumRows': 500,
                      'Page': page,
                      'SortBy': 'Status'}

            if status is None:
                pass
            elif status in ['all', 'closed']:
                params['StatusFilter'] = status
            else:
                print('That status code is not recognized via the API.')

            respjson = self.get_pipeline_report(**params)

            for i in respjson:
                output.append(i)

            if len(respjson) == 500:
                page += 1
            else:
                continue_flag = False

        return output

    def __validator(self, parameters, known_parameters):
        for param in parameters:
            if param not in known_parameters:
                raise LacrmArgumentError(content='The provided parameter "{}"'
                                         'cannot be recognized by the'
                                         'API'.format(param))
        return
