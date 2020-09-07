import json
import pytest
from ./test import CriminalDataScrapper


def test_scrapper_valid_data():
    fname, lname, dob = 'Steve', 'Smith', '04/23/2001'
    expected_output = {
        'docket_number': 'MJ-44302-CR-0000159-2019',
        'court_office': 'MDJ-44-3-02',
        'short_caption': 'Comm. v. Smith, Steven C.',
        'filling_date': 'Closed',
        'county': 'Wyoming',
        'primary_participant': 'Smith, Steven C.',
        'otn': 'U7703754',
        'complaint_number': '2019 019120',
        'dob': '4/23/2001'
    }

    scrapper = CriminalDataScrapper(
        'https://ujsportal.pacourts.us/DocketSheets/MDJ.aspx', fname, lname, dob)
    resp1 = scrapper.make_request1()
    data = scrapper.parse_response1(resp1)

    resp2 = scrapper.make_request2(data)
    data = scrapper.parse_response2(resp2)

    resp3 = scrapper.make_request3(data)
    actual_output = scrapper.parse_response3(resp3)

    assert expected_output == actual_output


# def test_scrapper_invalid_data():
#     fname, lname, dob = 'Invalid', 'name', ''
#     expected_output = {
#         'docket_number': '',
#         'court_office': '',
#         'short_caption': '',
#         'filling_date': '',
#         'county': '',
#         'primary_participant': '',
#         'otn': '',
#         'complaint_number': '',
#         'dob': ''
#     }

#     scrapper = CriminalDataScrapper(
#         'https://ujsportal.pacourts.us/DocketSheets/MDJ.aspx', fname, lname, dob)
#     resp1 = scrapper.make_request1()
#     data = scrapper.parse_response1(resp1)

#     resp2 = scrapper.make_request2(data)
#     data = scrapper.parse_response2(resp2)

#     resp3 = scrapper.make_request3(data)
#     actual_output = scrapper.parse_response3(resp3)

#     assert expected_output == actual_output


# Taks To be done
# 1. Run test cases
# 2. Handle Invalid Scenario
# 3. Handle Multiple Scenario
