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
    responses.add(
        responses.POST,
        re.compile('^https://api.lessannoyingcrm.com.*$'),
        body='{}',
        status=http.OK
    )

    assert lacrm_conn.edit_contact('12345', data) == http.OK


@responses.activate
def test_create_pipeline(lacrm_conn):
    responses.add(
        responses.POST,
        re.compile('^https://api.lessannoyingcrm.com.*$'),
        body='{"PipelineItemId":"abcd"}',
        status=http.OK
    )

    assert lacrm_conn.create_pipeline('12345', {}) == "abcd"

@responses.activate
def test_create_pipeline_raw(lacrm_conn):
    responses.add(
        responses.POST,
        re.compile('^https://api.lessannoyingcrm.com.*$'),
        body='{"PipelineItemId":"abcd", "OpportunityId":"abcd", "Success": true}',
        status=http.OK
    )

    assert lacrm_conn.create_pipeline('12345', {}, raw_response=True) == {"PipelineItemId":"abcd", "OpportunityId":"abcd", "Success": True}

@responses.activate
def test_update_pipeline(lacrm_conn):
    responses.add(
        responses.POST,
        re.compile('^https://api.lessannoyingcrm.com.*$'),
        body='{}',
        status=http.OK
    )

    assert lacrm_conn.update_pipeline('12345', {}) == http.OK


@responses.activate
def test_create_note(lacrm_conn):
    responses.add(
        responses.POST,
        re.compile('^https://api.lessannoyingcrm.com.*$'),
        body='{"NoteId": "32987108", "Success": true}',
        status=http.OK
    )

    assert lacrm_conn.create_note('12345', 'A nice note') == '32987108'


@responses.activate
def test_create_note_raw(lacrm_conn):
    responses.add(
        responses.POST,
        re.compile('^https://api.lessannoyingcrm.com.*$'),
        body='{"NoteId": "32987108", "Success": true}',
        status=http.OK
    )

    assert lacrm_conn.create_note('12345', 'A nice note', raw_response=True) == {'NoteId': '32987108', 'Success': True}


@responses.activate
def test_create_task(lacrm_conn):
    responses.add(
        responses.POST,
        re.compile('^https://api.lessannoyingcrm.com.*$'),
        body='{"TaskId": "42987108", "Success": true}',
        status=http.OK
    )

    data = {'DueDate':'2017-12-01', 'Description': 'Important meeting'}
    assert lacrm_conn.create_task(data) == '42987108'


@responses.activate
def test_create_task_raw(lacrm_conn):
    responses.add(
        responses.POST,
        re.compile('^https://api.lessannoyingcrm.com.*$'),
        body='{"TaskId": "42987108", "Success": true}',
        status=http.OK
    )

    data = {'DueDate':'2017-12-01', 'Description': 'Important meeting'}
    assert lacrm_conn.create_task(data, raw_response=True) == {"TaskId": "42987108", "Success": True}

@responses.activate
def test_create_event(lacrm_conn):
    responses.add(
        responses.POST,
        re.compile('^https://api.lessannoyingcrm.com.*$'),
        body='{"EventId": "42987000", "Success": true}',
        status=http.OK
    )

    data = {'Date':'2017-12-01', 'StartTime': '22:00', 'EndTime': '23:00', 'Description': 'Important event'}
    assert lacrm_conn.create_event(data) == '42987000'


@responses.activate
def test_create_event_raw(lacrm_conn):
    responses.add(
        responses.POST,
        re.compile('^https://api.lessannoyingcrm.com.*$'),
        body='{"EventId": "42987199", "Success": true}',
        status=http.OK
    )

    data = {'Date':'2017-12-01', 'StartTime': '22:00', 'EndTime': '23:00', 'Description': 'Important event'}
    assert lacrm_conn.create_event(data, raw_response=True) == {"EventId": "42987199", "Success": True}


@responses.activate
def test_get_pipeline_report(lacrm_conn):
    responses.add(
        responses.POST,
        re.compile('^https://api.lessannoyingcrm.com.*$'),
        body='{"Result": [], "Success": true}',
        status=http.OK
    )

    data = {}
    assert lacrm_conn.get_pipeline_report('pipeline_id', data) == []


@responses.activate
def test_get_pipeline_report_raw(lacrm_conn):
    responses.add(
        responses.POST,
        re.compile('^https://api.lessannoyingcrm.com.*$'),
        body='{"Result": [], "Success": true}',
        status=http.OK
    )

    data = {}
    assert lacrm_conn.get_pipeline_report('pipeline_id', data, raw_response=True) == {"Result": [], "Success": True}

@responses.activate
def test_get_all_pipeline_report(lacrm_conn):
    rng = [i for i in range(0,699)]
    with responses.RequestsMock(assert_all_requests_are_fired=True) as rsps:
        rsps.add(
            responses.POST,
            re.compile('^https://api.lessannoyingcrm.com.*$'),
            json={'Result': rng[0:500], 'Success': True},
            status=http.OK
        )
        rsps.add(
            responses.POST,
            re.compile('^https://api.lessannoyingcrm.com.*$'),
            json={'Result': rng[500:], 'Success': True},
            status=http.OK
        )

        assert lacrm_conn.get_all_pipeline_report('pipeline_id', status='all') == rng
