import os.path
import openpyxl
import requests
from bs4 import BeautifulSoup

excel_name = "results.xlsx"

excel_exists = os.path.exists(excel_name)
if excel_exists:  # Use that excel file, dont need to add column headers
    excel = openpyxl.load_workbook(excel_name)
    excel_sheet = excel.active
else:
    excel = openpyxl.Workbook()
    excel_sheet = excel.active
    excel_sheet.append(["IP", "ISP", "Usage Type", "Hostname", "Domain name", "Country", "City"])

with open('inputs.txt') as f: 
    ips = f.read().splitlines()

user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'} # if no user agent, GET request returns 403

count = 1
for ip in ips:
    print(str(count) + ". " + ip)

    url = "https://www.abuseipdb.com/check/" + ip
    response = requests.get(url, headers=user_agent).text
    soup = BeautifulSoup(response, 'html.parser')
    
    try:  # sometimes GET request doesn't get response
        table = soup.find( class_ = 'table' ).find_all('td')
    except:
        print("writing stopped at " + str(count) + ": " + ip)
        excel.save(excel_name)
        exit()

    ip_info = [ip]
    for info in table:
        ip_info.append(info.get_text().strip("\n"))
    
    if len(ip_info) < 7:  # means no hostname, put "-" instead
        ip_info.insert(3, "-")
    
    excel_sheet.append(ip_info)
    count = count + 1
    
excel.save("results.xlsx")
