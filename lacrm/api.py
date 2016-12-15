"Core classes and exceptions for lacrm"

import logging
import warnings
import requests
import json

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


    def search(self, term):
        method_payload = self.payload
        method_payload['Function'] = 'SearchContacts'

        parameters = {'SearchTerms': term}
        method_payload['Parameters'] = json.dumps(parameters)
        
        r = requests.post(self.endpoint_url, data=method_payload)
        response = r.json()
        if response.get('Success') == False:
            return LacrmError(response.get('Error'))
        else:
            return response.get('Result')

    def create_contact(self,*args,**kwargs):
        parameters = {}
        for key,value in kwargs.items():
            parameters[key] = value

        method_payload = self.payload
        method_payload['Function'] = 'CreateContact'

        method_payload['Parameters'] = json.dumps(parameters)
        
        print method_payload
        r = requests.post(self.endpoint_url, data=method_payload)
        response = r.json()
        if response.get('Success') == False:
            return LacrmError(response.get('Error'))
        else:
            return response.get('Result')
        # if kwargs.keys not in ['FullName', 'Salutation', 'FirstName', 'MiddleName', 'LastName',
        #  'Suffix', 'CompanyName', 'CompanyId', 'Title', 'Industry',
        #  'NumEmployees', 'BackgroundInfo', 'Email', 'Phone', 'Address',
        #  'Website', 'Birthday', 'CustomFields', 'assignedTo']:
        #
        # 'FullName'
        # 'Salutation'
        # 'FirstName'
        # 'MiddleName'
        # 'LastName'
        # 'Suffix'
        # 'CompanyName'
        # 'CompanyId'
        # 'Title'
        # 'Industry'
        # 'NumEmployees'
        # 'BackgroundInfo'
        # 'Email'
        # 'Phone'
        # 'Address'
        # 'Website'
        # 'Birthday'
        # 'CustomFields'
        # 'assignedTo'
