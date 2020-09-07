import requests
from bs4 import BeautifulSoup
import re


class CriminalDataScrapper:
    def __init__(self, url, fname, lname, dob):
        self.url = url
        self.fname = fname
        self.lname = lname
        self.dob = dob
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'}

    def make_request1(self):
        response = requests.get(self.url, headers=self.headers, verify=False)
        self.cookies = response.cookies
        return response

    def parse_response1(self, response):
        soup = BeautifulSoup(response.content)
        event_target = "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$ddlSearchType"
        view_state = soup.find('input', {'name': '__VIEWSTATE'}).attrs['value']
        scroll_pos_x = soup.find(
            'input', {'name': '__SCROLLPOSITIONX'}).attrs['value']
        scroll_pos_y = soup.find(
            'input', {'name': '__SCROLLPOSITIONY'}).attrs['value']

        return self.get_payload_1(event_target, view_state,
                                  scroll_pos_x, scroll_pos_y, self.get_captcha_answer(soup))

    def make_request2(self, data):
        return requests.post(self.url, headers=self.headers,
                             cookies=self.cookies, data=data, verify=False)

    def parse_response2(self, response):
        soup = BeautifulSoup(response.content)
        view_state = soup.find('input', {'name': '__VIEWSTATE'}).attrs['value']
        scroll_pos_x = soup.find(
            'input', {'name': '__SCROLLPOSITIONX'}).attrs['value']
        scroll_pos_y = soup.find(
            'input', {'name': '__SCROLLPOSITIONY'}).attrs['value']

        return self.get_payload_2(view_state, scroll_pos_x,
                                  scroll_pos_y, self.get_captcha_answer(soup), self.fname, self.lname, self.dob)

    def make_request3(self, data):
        return requests.post(self.url, headers=self.headers,
                             cookies=self.cookies, data=data, verify=False)

    def parse_response3(self, response):
        soup = BeautifulSoup(response.content)
        card = soup.find('tr', {'class': 'gridViewRow'})
        return {
            'docket_number': card.find_all('td')[7].text,
            'court_office': card.find('span', {'id': 'ctl00_ctl00_ctl00_cphMain_cphDynamicContent_cphResults_gvDocket_ctl02_Label1'}).text,
            'short_caption': card.find('span', {'id': 'ctl00_ctl00_ctl00_cphMain_cphDynamicContent_cphResults_gvDocket_ctl02_Label2'}).text,
            'filling_date': card.find('span', {'id': 'ctl00_ctl00_ctl00_cphMain_cphDynamicContent_cphResults_gvDocket_ctl02_Label4'}).text,
            'county': card.find('span', {'id': 'ctl00_ctl00_ctl00_cphMain_cphDynamicContent_cphResults_gvDocket_ctl02_Label3'}).text,
            'primary_participant': card.find('span', {'id': 'ctl00_ctl00_ctl00_cphMain_cphDynamicContent_cphResults_gvDocket_ctl02_ctl00_ctl00_Label5'}).text,
            'otn': card.find('span', {'id': 'ctl00_ctl00_ctl00_cphMain_cphDynamicContent_cphResults_gvDocket_ctl02_Label6'}).text,
            'complaint_number': card.find('span', {'id': 'ctl00_ctl00_ctl00_cphMain_cphDynamicContent_cphResults_gvDocket_ctl02_ctl01_ctl00_Label7'}).text,
            'dob': soup.find('table', {'id': 'ctl00_ctl00_ctl00_cphMain_cphDynamicContent_cphResults_gvDocket_ctl02_ctl02'}).find('span').text
        }

    @staticmethod
    def get_payload_1(event_target, view_state, scroll_pos_x, scroll_pos_y, captcha_answer):
        return {
            "__EVENTTARGET": event_target,
            "__EVENTARGUMENT": '',
            "__LASTFOCUS": '',
            "__VIEWSTATE": view_state,
            "__VIEWSTATEGENERATOR": "4AB257F3",
            "__SCROLLPOSITIONX": scroll_pos_x,
            "__SCROLLPOSITIONY": scroll_pos_y,
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$ddlSearchType": "ParticipantName",
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsDocketNumber$ddlCounty": '',
            "ctl00$ctl00$ctl00$ctl07$captchaAnswer": captcha_answer
        }

    @staticmethod
    def get_payload_2(view_state, scroll_pos_x, scroll_pos_y, captcha_answer, fname, lname, dob):
        return {
            "__EVENTTARGET": '',
            "__EVENTARGUMENT": '',
            "__LASTFOCUS": '',
            "__VIEWSTATE": view_state,
            "__VIEWSTATEGENERATOR": "4AB257F3",
            "__SCROLLPOSITIONX": scroll_pos_x,
            "__SCROLLPOSITIONY": scroll_pos_y,
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$ddlSearchType": "ParticipantName",
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$txtLastName": lname,
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$txtFirstName": fname,
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$dpDOB$DateTextBox": dob,
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$dpDOB$DateTextBoxMaskExtender_ClientState": '',
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$ddlCounty": '',
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$ddlDocketType": "CR",
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$ddlCaseStatus": '',
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$DateFiledDateRangePicker$beginDateChildControl$DateTextBox": '__/__/____',
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$DateFiledDateRangePicker$beginDateChildControl$DateTextBoxMaskExtender_ClientState": '',
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$DateFiledDateRangePicker$endDateChildControl$DateTextBox": '__/__/____',
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$DateFiledDateRangePicker$endDateChildControl$DateTextBoxMaskExtender_ClientState": '',
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$btnSearch": "Search",
            "ctl00$ctl00$ctl00$ctl07$captchaAnswer": captcha_answer
        }

    @staticmethod
    def get_captcha_answer(soup):
        all_scripts = soup.find_all('script', {'type': 'text/javascript'})
        keyValueMatch = re.findall("value = '.*;", str(all_scripts))[0]
        return re.findall("-*[0-9]+", keyValueMatch)[0]


if __name__ == "__main__":
    scrapper = CriminalDataScrapper(
        'https://ujsportal.pacourts.us/DocketSheets/MDJ.aspx', 'Steve', 'Smith', '04/23/2001')

    resp1 = scrapper.make_request1()
    data = scrapper.parse_response1(resp1)

    resp2 = scrapper.make_request2(data)
    data = scrapper.parse_response2(resp2)

    resp3 = scrapper.make_request3(data)
    data = scrapper.parse_response3(resp3)

    print(data)
