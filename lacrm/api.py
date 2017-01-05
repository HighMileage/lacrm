"Core classes and exceptions for lacrm"

import logging
import warnings
import requests
import json
from utils import LacrmArgumentError, BaseLacrmError

try:
    from urlparse import urlparse, urljoin
except ImportError:
    # Python 3+
    from urllib.parse import urlparse, urljoin
# from lacrm.login import LacrmLogin
# from lacrm.utils import LacrmError

try:
    from collections import OrderedDict
except ImportError:
    # Python < 2.7
    from ordereddict import OrderedDict

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
                  'APIToken': self.api_token,
        }
        self.endpoint_url = 'https://api.lessannoyingcrm.com'

        # Mapping that allows us to parse different API methods' response meaningfully
        self.api_method_responses = {'CreateContact': 'ContactId',
                                     'GetContact': 'Contact',
                                     'Search': 'Results'
        }


    def api_call(func):
        """ Decorator calls out to the API for specifics API methods """

        def make_api_call(self, *args, **kwargs):
            api_method, parameters = func(self, * args, **kwargs)

            method_payload = self.payload
            method_payload['Function'] = api_method
            method_payload['Parameters'] = json.dumps(parameters)

            response = requests.post(self.endpoint_url, data=method_payload).json()

            if response.get('Success') == False:
                raise BaseLacrmError(content='Unknown error occurred -- check https://www.lessannoyingcrm.com/account/api/ for more detailed information.')
            else:
                print response
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

        for key,value in kwargs.items():
            parameters[key] = value

        return api_method, parameters


    @api_call
    def delete_contact(self, *args, **kwargs):
        """ Deletes a given contact from LACRM """

        parameters = {}
        api_method = 'DeleteContact'

        for key,value in kwargs.items():
            parameters[key] = value

        return api_method, parameters

    @api_call
    def get_contact(self, *args, **kwargs):
        """ Get all information in LACRM for given contact """

        parameters = {}
        api_method = 'GetContact'

        for key,value in kwargs.items():
            parameters[key] = value

        return api_method, parameters

    @api_call
    def create_contact(self,*args,**kwargs):
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

        for key,value in kwargs.items():
            parameters[key] = value

        self.__validator(parameters.keys(), expected_parameters)
        return api_method, parameters

    def __validator(self, parameters, known_parameters):
        for param in parameters:
            if param not in known_parameters:
                raise LacrmArgumentError(content='The provided parameter "{}" cannot be recognized by the API'.format(param))
        return
