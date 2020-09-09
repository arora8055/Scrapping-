import json
import pytest
from scrap_criminal_data import CriminalDataScrapper


def test_scrapper_valid_data():
    fname, lname, dob = 'William', 'Rios', '07/31/1975'
    expected_output = [{
        'docket_number': 'MJ-31201-CR-0001050-2007',
        'court_office': 'MDJ-31-2-01',
        'short_caption': 'Comm. v. Rios Rivera, William Antonio',
        'filling_date': '11/06/2007',
        'country': 'Lehigh',
        'case_status': 'Closed',
        'primary_participant': 'Rios Rivera, William Antonio',
        'OTN': 'K6846641',
        'complaint_number': '0790050',
        'police_incident': '0790050',
        'date_of_birth': '7/31/1975'
    }]

    scrapper = CriminalDataScrapper(
        'https://ujsportal.pacourts.us/DocketSheets/MDJ.aspx', fname, lname, dob)
    actual_output = scrapper.scrap()

    assert expected_output == actual_output


def test_scrapper_valid_multiple_data():
    fname, lname, dob = 'Steve', 'Smith', '04/23/2001'
    expected_output = [
        {
            'docket_number': 'MJ-44302-CR-0000159-2019',
            'court_office': 'MDJ-44-3-02',
            'short_caption': 'Comm. v. Smith, Steven C.',
            'filling_date': '11/18/2019',
            'country': 'Wyoming',
            'case_status': 'Closed',
            'primary_participant': 'Smith, Steven C.',
            'OTN': 'U7703754',
            'complaint_number': '2019 019120',
            'police_incident': '2019 019120',
            'date_of_birth': '4/23/2001'
        },
        {
            'docket_number': 'MJ-44301-CR-0000211-2019',
            'court_office': 'MDJ-44-3-01',
            'short_caption': 'Comm. v. Smith, Steven C.',
            'filling_date': '10/21/2019',
            'country': 'Wyoming',
            'case_status': 'Closed',
            'primary_participant': 'Smith, Steven C.',
            'OTN': 'X2905593',
            'complaint_number': 'R19 405',
            'police_incident': 'R19 405',
            'date_of_birth': '4/23/2001'
        },
        {
            'docket_number': 'MJ-44301-CR-0000205-2019',
            'court_office': 'MDJ-44-3-01',
            'short_caption': 'Comm. v. Smith, Steven Charles',
            'filling_date': '10/07/2019',
            'country': 'Wyoming',
            'case_status': 'Closed',
            'primary_participant': 'Smith, Steven Charles',
            'OTN': 'U7567921',
            'complaint_number': 'R19 395',
            'police_incident': 'R19 395',
            'date_of_birth': '4/23/2001'
        }
    ]

    scrapper = CriminalDataScrapper(
        'https://ujsportal.pacourts.us/DocketSheets/MDJ.aspx', fname, lname, dob)
    actual_output = scrapper.scrap()

    assert expected_output == actual_output


def test_scrapper_invalid_data():
    fname, lname, dob = 'Invalid', 'name', ''
    expected_output = []

    scrapper = CriminalDataScrapper(
        'https://ujsportal.pacourts.us/DocketSheets/MDJ.aspx', fname, lname, dob)
    actual_output = scrapper.scrap()

    assert expected_output == actual_output
