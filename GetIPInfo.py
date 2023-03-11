import os.path
import openpyxl
import requests
from bs4 import BeautifulSoup

REPORTED_NUM_INDEX = 1
ABUSE_CONFIDENCE_INDEX = 2
HOSTNAME_INDEX = 5
EXPECTED_LENGTH = 9
excel_name = "results.xlsx"
inputs_name = "inputs.txt"

def get_reported_stats(ip_info, soup):
    stats = soup.find(class_='well').find_all('b')
    if len(stats) < 3:  # means IP address is not in abuseipdb database
        ip_info.extend(["-", "-"])
        return

    ip_info.append(int(stats[REPORTED_NUM_INDEX].get_text().replace(",", "")))
    ip_info.append(int(stats[ABUSE_CONFIDENCE_INDEX].get_text().strip("%")))

def get_ip_info(ip_info, soup):
    table = soup.find(class_='table').find_all('td')
    for info in table:
        ip_info.append(info.get_text().strip("\n"))

def main():
    file_exists = os.path.exists(excel_name)
    if file_exists:  # Use that excel file, dont need to add column headers
        excel = openpyxl.load_workbook(excel_name)
        excel_sheet = excel.active
    else:
        excel = openpyxl.Workbook()
        excel_sheet = excel.active
        excel_sheet.append(["IP",
                            "No. of times reported",
                            "Abuse Confidence (%)",
                            "ISP",
                            "Usage Type",
                            "Hostname",
                            "Domain name",
                            "Country",
                            "City"])

    with open(inputs_name) as f:
        ips = f.read().splitlines()

    # if no user agent, GET request returns 403
    user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

    count = 1
    for ip in ips:
        ip_info = [ip]
        print(str(count) + ". " + ip)

        url = "https://www.abuseipdb.com/check/" + ip
        response = requests.get(url, headers=user_agent).text
        soup = BeautifulSoup(response, 'html.parser')
        
        try:  # sometimes response doesn't render properly, occurs when sending > 50 GET requests
            get_reported_stats(ip_info, soup)
            get_ip_info(ip_info, soup)
        except:
            print("Writing stopped at " + str(count) + ": " + ip)
            excel.save(excel_name)
            exit()

        if len(ip_info) < EXPECTED_LENGTH:  # means no hostname, put "-" instead
            ip_info.insert(HOSTNAME_INDEX, "-")

        excel_sheet.append(ip_info)
        count = count + 1

    excel.save(excel_name)

if __name__ == "__main__":
    main()
