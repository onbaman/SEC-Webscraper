# From the TXT file extract the Mutual Fund Name and CIK
def extract_data(file):
    fundname = []
    tickernumber = []
    for lines in file:
        ticker = lines.split("|")[1].replace("\n", "").replace(" ", "")
        fund = lines.split("|")[0]
        tickernumber.append(ticker)
        fundname.append(fund)

    return fundname, tickernumber
