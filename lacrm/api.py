"Core classes and exceptions for lacrm"

from __future__ import print_function
import logging
import requests
import json
from lacrm.utils import LacrmArgumentError, BaseLacrmError

LOGGER = logging.getLogger(__name__)


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
                                     'SearchContacts': 'Results',
                                     'GetPipelineReport': 'Result'}

    def api_call(func):
        """ Decorator calls out to the API for specifics API methods """

        def make_api_call(self, *args):

            api_method, data, expected_parameters = func(self, *args)

            parameters = {}
            for key, value in data.items():
                parameters[key] = value

            if expected_parameters:
                self.__validator(parameters.keys(), expected_parameters)

            method_payload = self.payload
            method_payload['Function'] = api_method
            method_payload['Parameters'] = json.dumps(parameters)

            response = requests.post(self.endpoint_url, data=method_payload)

            status_code = response.status_code
            if status_code != 200:
                raise BaseLacrmError(content='Unknown error occurred -- check'
                                     'https://www.lessannoyingcrm.com/account/'
                                     'api/ for more detailed information.')
            else:
                response = response.json()
                return response.get(self.api_method_responses.get(api_method), status_code)

        return make_api_call

    @api_call
    def search(self, term):
        """ Searches LACRM contacts for a given term """

        api_method = 'SearchContacts'
        data = {'SearchTerms': term}

        return api_method, data, None

    @api_call
    def add_contact_to_group(self, contact_id, group_name):
        """ Adds a contact to a group in LACRM """

        data = {}
        data['ContactId'] = contact_id
        data['GroupName'] = group_name

        if group_name.find(' ') > 0:
                raise LacrmArgumentError(
                    content='The group name you passed "{0}" contains spaces. '
                    'Spaces should be replaced them with underscores (eg "cool '
                    'group" should be "cool_group"). See '
                    'https://www.lessannoyingcrm.com/help/topic/API_Function_Definitions/8/AddContactToGroup+Function+Definition '
                    'for more details.'.format(group_name))

        api_method = 'AddContactToGroup'

        return api_method, data, None

    @api_call
    def delete_contact(self, contact_id):
        """ Deletes a given contact from LACRM """

        data = {}
        data['ConatctId'] = contact_id
        api_method = 'DeleteContact'

        return api_method, data, None

    @api_call
    def get_contact(self, contact_id):
        """ Get all information in LACRM for given contact """

        data = {}
        data['ConatctId'] = contact_id
        api_method = 'GetContact'

        return api_method, data, None

    @api_call
    def create_contact(self, data):
        """ Creates a new contact in LACRM """

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

        return api_method, data, expected_parameters

    @api_call
    def edit_contact(self, contact_id, data):
        """ Edits a contact in LACRM for given """

        data['ContactId'] = contact_id
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

        return api_method, data, expected_parameters

    @api_call
    def create_pipeline(self, contact_id, data):
        """ Creates a new pipeline in LACRM for given contactid """

        data['ConatctId'] = contact_id
        api_method = 'CreatePipeline'
        expected_parameters = ['ContactId',
                               'Note',
                               'PipelineId',
                               'StatusId',
                               'Priority',
                               'CustomFields']

        return api_method, data, expected_parameters

    @api_call
    def update_pipeline(self, pipeline_id, data):
        """ Update a pipeline in LACRM """

        data['ConatctId'] = pipeline_id
        api_method = 'UpdatePipelineItem'
        expected_parameters = ['PipelineItemId',
                               'Note',
                               'StatusId',
                               'Priority',
                               'CustomFields']

        return api_method, data, expected_parameters

    @api_call
    def create_note(self, contact_id, data):
        """ Creates a new note in LACRM for a given contactid """

        data = {}
        data['ConatctId'] = contact_id
        api_method = 'CreateNote'
        expected_parameters = ['ContactId',
                               'Note',
                               'PipelineId',
                               'StatusId',
                               'Priority',
                               'CustomFields']

        return api_method, data, expected_parameters

    @api_call
    def create_task(self, data):
        """ Creates a new task in LACRM """

        api_method = 'CreateTask'
        expected_parameters = ['ContactId',
                               'DueDate',  # YYYY-MM-DD
                               'Description',
                               'ContactId',
                               'AssignedTo']

        return api_method, data, expected_parameters

    @api_call
    def create_event(self, date, start_time, end_time, name):
        """ Creates a new event in LACRM """

        data = {}
        data['Date'] = date
        data['StartTime'] = start_time
        data['EndTime'] = end_time
        data['Name'] = name

        api_method = 'CreateEvent'
        expected_parameters = ['Date',
                               'StartTime',  # 24:00
                               'EndTime',  # 24:00
                               'Name',
                               'Description',
                               'Contacts',
                               'Users']

        return api_method, data, expected_parameters

    @api_call
    def get_pipeline_report(self, pipeline_id):
        """ Grabs a pipeline_report in LACRM """

        data = {}
        data['PipelineId'] = pipeline_id

        api_method = 'GetPipelineReport'
        expected_parameters = ['PipelineId',
                               'SortBy',
                               'NumRows',
                               'Page',
                               'SortDirection',
                               'UserFilter',
                               'StatusFilter']

        return api_method, data, expected_parameters

    def getall_pipeline_report(self, pipeline_id, status=None):
        """ Grabs a pipeline_report in LACRM """

        continue_flag = True
        page = 1
        output = []

        while continue_flag:

            params = {'NumRows': 500,
                      'Page': page,
                      'SortBy': 'Status'}

            if status is None:
                pass
            elif status in ['all', 'closed']:
                params['StatusFilter'] = status
            else:
                print('That status code is not recognized via the API.')

            respjson = self.get_pipeline_report(pipeline_id, params)

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
                raise LacrmArgumentError(content='The provided parameter "{}" '
                                         'cannot be recognized by the '
                                         'API'.format(param))
        return
