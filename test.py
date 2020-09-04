import requests
from bs4 import BeautifulSoup
import re


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


def get_payload_2(view_state2, scroll_pos_x2, scroll_pos_y2, captcha_answer2):
    return {
        "__EVENTTARGET": '',
        "__EVENTARGUMENT": '',
        "__LASTFOCUS": '',
        "__VIEWSTATE": view_state2,
        "__VIEWSTATEGENERATOR": "4AB257F3",
        "__SCROLLPOSITIONX": scroll_pos_x2,
        "__SCROLLPOSITIONY": scroll_pos_y2,
        "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$ddlSearchType": "ParticipantName",
        "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$txtLastName": "rios",
        "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$txtFirstName": "william",
        "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$dpDOB$DateTextBox": "07/31/1975",
        "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$dpDOB$DateTextBoxMaskExtender_ClientState": '',
        "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$ddlCounty": '',
        "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$ddlDocketType": "CR",
        "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$ddlCaseStatus": '',
        "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$DateFiledDateRangePicker$beginDateChildControl$DateTextBox": '__/__/____',
        "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$DateFiledDateRangePicker$beginDateChildControl$DateTextBoxMaskExtender_ClientState": '',
        "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$DateFiledDateRangePicker$endDateChildControl$DateTextBox": '__/__/____',
        "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$DateFiledDateRangePicker$endDateChildControl$DateTextBoxMaskExtender_ClientState": '',
        "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$btnSearch": "Search",
        "ctl00$ctl00$ctl00$ctl07$captchaAnswer": captcha_answer2
    }


def get_criminal_data(card, soup):
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


def get_captcha_answer(soup):
    all_scripts = soup.find_all('script', {'type': 'text/javascript'})
    keyValueMatch = re.findall("value = '.*;", str(all_scripts))[0]
    return re.findall("-*[0-9]+", keyValueMatch)[0]


link = 'https://ujsportal.pacourts.us/DocketSheets/MDJ.aspx'
headers = {'Content-Type': 'application/x-www-form-urlencoded',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
           'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'}

response1 = requests.get(link, headers=headers, verify=False)

cokkie = response1.cookies
# print(response)
# print(response.text)

soup = BeautifulSoup(response1.content)

# To find captcha without use of REGEX
# captcha_answer = soup.find_all('script',{'type':'text/javascript'})[24].string.split(".value =")[1].split(";")[0].split("'")[1]


event_target = "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$ddlSearchType"
view_state = soup.find('input', {'name': '__VIEWSTATE'}).attrs['value']
scroll_pos_x = soup.find('input', {'name': '__SCROLLPOSITIONX'}).attrs['value']
scroll_pos_y = soup.find('input', {'name': '__SCROLLPOSITIONY'}).attrs['value']


payload_1 = get_payload_1(event_target, view_state,
                          scroll_pos_x, scroll_pos_y, get_captcha_answer(soup))

reponse2 = requests.post(link, headers=headers,
                         cookies=cokkie, data=payload_1, verify=False)

soup2 = BeautifulSoup(reponse2.content)

view_state2 = soup2.find('input', {'name': '__VIEWSTATE'}).attrs['value']

scroll_pos_x2 = soup2.find(
    'input', {'name': '__SCROLLPOSITIONX'}).attrs['value']

scroll_pos_y2 = soup2.find(
    'input', {'name': '__SCROLLPOSITIONY'}).attrs['value']


payload_2 = get_payload_2(view_state2, scroll_pos_x2,
                          scroll_pos_y2, get_captcha_answer(soup2))

reponse3 = requests.post(link, headers=headers,
                         cookies=cokkie, data=payload_2, verify=False)

soup3 = BeautifulSoup(reponse3.content)
card = soup3.find('tr', {'class': 'gridViewRow'})

print(get_criminal_data(card, soup3))
