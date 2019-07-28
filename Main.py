import Parse_Funds as pf
import Read_data as rd

pathTodata = "data/mutual funds.txt"
mutualFunds = rd.extract_data(open(pathTodata, "r"))
fundNames = mutualFunds[0]
fundTickers = mutualFunds[1]

for index in range(len(fundNames)):
    print(fundNames[index])
    target_docs = pf.gather_target_docs(fundTickers[index])
    pf.scrape_documents(target_docs, fundNames[index])
