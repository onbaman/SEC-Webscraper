from bs4 import BeautifulSoup
import requests
import re
import urllib.request
import csv


# Find all documents with the 13F tag given Ticker#
def gather_target_docs(CIK):
    fundurl = "https://www.sec.gov/cgi-bin/browse-edgar?CIK=" + CIK + "&owner=exclude&action=getcompany"
    targetSite = requests.get(fundurl, timeout=10)
    # print(targetSite.text)
    soup = BeautifulSoup(targetSite.text, 'html.parser')

    table = soup.find('table', {"class": "tableFile2"})
    rows = table.find_all("tr")

    final_list = []
    for row in rows:
        items = []
        cell = row.find("td", text=re.compile('13F'))
        if cell:
            cleanedLine = str(cell.text.strip()).replace("/", "-")
            items.append(cleanedLine)
            newURL = str(cell.find_next('a')['href']).replace("-index.htm", ".txt")
            items.append(newURL)
            items.append(cell.find_next('a').find_next('td').find_next('td').text.strip())
            final_list.append(items)

    return final_list


# Using the list of files scrape only the most recent data from a fund
def scrape_documents(documentURL, fundName):

    baseWebsite = "https://www.sec.gov"
    # Save a copy of the information locally in buffer.txt
    urllib.request.urlretrieve(baseWebsite + documentURL[0][1], "data/buffer.txt")

    # Cleaning document to keep only infotable sections
    isTable = False
    with open("data/buffer.txt", "r", newline='') as f:
        lines = f.readlines()
    with open("data/buffer.txt", "w+", newline='') as f:
        for line in lines:
            if "infoTable" in line or "ns1:infoTable" in line:
                isTable = True
                f.write(line)
                continue
            elif "/infoTable" in line or "/ns1:infoTable" in line:
                isTable = False
                f.write(line)
            elif isTable:
                f.write(line)

    header = ['nameOfIssuer', 'titleOfClass', 'cusip', 'value', 'sshPrnamt', 'sshPrnamtType', 'putCall',
              'investmentDiscretion', 'otherManager', 'VotingAuthSole', 'VotingAuthShared', 'VotingAuthNone']
    cols = ['nameOfIssuer', 'titleOfClass', 'cusip', 'value', 'sshPrnamt', 'sshPrnamtType', 'putCall',
            'investmentDiscretion', 'otherManager', 'Sole', 'Shared', 'None']
    data = []
    # Only need to run this once but can be modified to allow for all previous files to be scraped
    for row in range(0, 1):
        # Create file
        tsvFile = "Data/" + fundName + str(documentURL[0][0]) + " " + str(documentURL[0][2]) + ".tsv"

        # Begin parsing and writing data to .tsv file
        with open(tsvFile, "w+", newline='') as file:
            headercolumn = csv.writer(file, delimiter="\t")
            headercolumn.writerows([header])

            soup = BeautifulSoup(open("data/buffer.txt", "r").read(), 'lxml')
            for info_table in soup.find_all(['ns1:infotable', 'infotable']):
                fundData = []
                for col in cols:
                    cell = info_table.find([col.lower(), 'ns1:' + col.lower()])
                    fundData.append(cell.text.strip() if cell else 'NaN')
                data.append(fundData)

            # Save newly collected data into the TSV file
            csvwriter = csv.writer(file, delimiter="\t")
            csvwriter.writerows(data)
            file.close()
