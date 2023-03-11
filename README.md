# GetIPInfo

This is a simple Python script that takes in a list of IP addresses, `inputs.txt`, and outputs additional information on the IP addresses into an excel spreadsheet `results.xlsx`. This information includes:
- Number of times IP has been reported
- Abuse Confidence (%)
- Internet Service Provider
- Usage Type
- Hostname (if available)
- Domain name
- Country
- City

The script uses the website https://www.abuseipdb.com/ to obtain the information. This is useful to check for IP addresses that are associated with malicious activity. 
