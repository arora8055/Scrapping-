import requests
from bs4 import BeautifulSoup
import re


class CriminalDataScrapper:
    """Fetching Criminal Records of a person from Peninsula Website"""

    def __init__(self, url, fname, lname, dob):
        self.url = url
        self.fname = fname
        self.lname = lname
        self.dob = dob
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'}

    def make_request1(self):
        """Calling first GET request, Getting cookies from Response and returning Response """
        response = requests.get(self.url, headers=self.headers, verify=False)
        self.cookies = response.cookies
        return response

    def parse_response1(self, response):
        """Parsing Response from first GET request and calling get_payload1() for creating FORM DATA  """
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
        """Calling first POST request with cookies and return Response"""
        return requests.post(self.url, headers=self.headers,
                             cookies=self.cookies, data=data, verify=False)

    def parse_response2(self, response):
        """Parsing response from POST request and calling get_payload2() for creating FORM DATA"""
        soup = BeautifulSoup(response.content)
        view_state = soup.find('input', {'name': '__VIEWSTATE'}).attrs['value']
        scroll_pos_x = soup.find(
            'input', {'name': '__SCROLLPOSITIONX'}).attrs['value']
        scroll_pos_y = soup.find(
            'input', {'name': '__SCROLLPOSITIONY'}).attrs['value']

        return self.get_payload_2(view_state, scroll_pos_x,
                                  scroll_pos_y, self.get_captcha_answer(soup), self.fname, self.lname, self.dob)

    def make_request3(self, data):
        """ Calling second POST request with cookies and returning Response"""
        return requests.post(self.url, headers=self.headers,
                             cookies=self.cookies, data=data, verify=False)

    def parse_response3(self, response):
        """ Parsing response from second POST request and and returning final result required by end user """
        soup = BeautifulSoup(response.content)
        records = list()
        cards = soup.find_all('tr', {'class': 'gridViewRow'})
        if cards:
            for card in cards:
                table_data = card.find_all("td")
                if table_data:
                    record = {
                        "docket_number": table_data[7].text.strip(),
                        "court_office": table_data[8].text.strip(),
                        "short_caption": table_data[9].text.strip(),
                        "filling_date": table_data[10].text.strip(),
                        "country": table_data[11].text.strip(),
                        "case_status": table_data[12].text.strip(),
                        "primary_participant": table_data[13].text.strip(),
                        "OTN": table_data[15].text.strip(),
                        "complaint_number": table_data[18].text.strip(),
                        "police_incident": table_data[18].text.strip(),
                        "date_of_birth": table_data[19].text.strip()
                    }
                    # print(record)
                    records.append(record)
        return records

    def scrap(self):
        """Calling  required methods for scrapping data and returning the required data use by end user"""
        resp1 = self.make_request1()
        data = self.parse_response1(resp1)

        resp2 = self.make_request2(data)
        data = self.parse_response2(resp2)

        resp3 = self.make_request3(data)
        return scrapper.parse_response3(resp3)

    @staticmethod
    def get_payload_1(event_target, view_state, scroll_pos_x, scroll_pos_y, captcha_answer):
        """Creating FORM DATA for first POST request"""
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
        """Creating FORM DATA for second POST request"""
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
        """Solving captcha generated by JS dynamically with Regex"""
        all_scripts = soup.find_all('script', {'type': 'text/javascript'})
        keyValueMatch = re.findall("value = '.*;", str(all_scripts))[0]
        return re.findall("-*[0-9]+", keyValueMatch)[0]


if __name__ == "__main__":
    scrapper = CriminalDataScrapper(
        'https://ujsportal.pacourts.us/DocketSheets/MDJ.aspx', 'Steve', 'Smith', '04/23/2001')

    data = scrapper.scrap()
    print(data)
