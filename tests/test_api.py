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

testdata = [
        {'Email': 'coolgal@fakemail.com'},
        {'FirstName': 'Bob', 'LastName': 'Vila'}
        ]

@pytest.fixture
def lacrm_conn():
    return Lacrm(user_code="1234", api_token="abcdef")


@responses.activate
def test_get_contact(lacrm_conn):
    responses.add(
        responses.POST,
        re.compile(r"^https://.*$"),
        body='{"Contact":"Cool attributes"}',
        status=http.OK
     )

    assert lacrm_conn.get_contact("12345") == "Cool attributes"


@responses.activate
def test_create_contact(lacrm_conn):
    responses.add(
        responses.POST,
        re.compile('^https://api.lessannoyingcrm.com.*$'),
        body='{"ContactId":"1234abcd"}',
        status=http.OK
     )

    assert lacrm_conn.create_contact({'FullName':'fake data'}) == "1234abcd"


@responses.activate
def test_delete_contact(lacrm_conn):
    responses.add(
        responses.POST,
        re.compile('^https://api.lessannoyingcrm.com.*$'),
        body='{}',
        status=http.OK
    )

    assert lacrm_conn.delete_contact("some_contact_id") == http.OK

@responses.activate
def test_search(lacrm_conn):
    responses.add(
        responses.POST,
        re.compile('^https://api.lessannoyingcrm.com.*$'),
        body='{"Results": ["1","2","3"]}',
        status=http.OK
    )

    assert lacrm_conn.search("search term") == ["1","2","3"]

@responses.activate
def test_add_contact_group(lacrm_conn):
    responses.add(
        responses.POST,
        re.compile('^https://api.lessannoyingcrm.com.*$'),
        body='{}',
        status=http.OK
    )

    assert lacrm_conn.add_contact_to_group('contact_id', 'cool_kids') == http.OK

@pytest.mark.parametrize('data', testdata, ids=['email','names'])
@responses.activate
def test_edit_contact(lacrm_conn, data):
    print(data)
    responses.add(
        responses.POST,
        re.compile('^https://api.lessannoyingcrm.com.*$'),
        body='{}',
        status=http.OK
    )

    assert lacrm_conn.edit_contact('12345', data) == http.OK
