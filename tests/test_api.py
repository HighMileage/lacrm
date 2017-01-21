" Tests for api.py "
import re
import pytest
from lacrm.api import Lacrm
import responses
try:
    # Python 2.6/2.7
    import httplib as http
    # from mock import Mock, patch
except ImportError:
    # Python 3
    import http.client as http
    # from unittest.mock import Mock, patch

@pytest.fixture
def lacrm_conn():
    return Lacrm(user_code="1234", api_token="ABCDEF")

@responses.activate
def test_get_contact(lacrm_conn):
    responses.add(
        responses.POST,
        re.compile(r"^https://.*$"),
        body='{"Contact":"Cool attributes"}',
        status=http.OK
     )

    assert lacrm_conn.get_contact("12345") == "Cool attributes"
