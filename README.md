# SEC 13-F WebScraper

Webscraper that goes through a list of Mutual Funds and Tickers and gathers information from the first document

This project comes in three main Python Files
1. Main.py (Central file that runs all my files together)
2. Parse_Funds.py (Goes to each respective fund and scrapes data from most recent report)
3. Read_Data.py (Reads from text file with all of Mutual Funds & Tickers)

# How to get started
After unzipping my project you will see a folder labeled `data`. This is where all of the .tsv files will be stored in. 

![picture alt](DataOnee.JPG)

From there you will see a file named `mutual funds.txt` This is where the names and tickers for the mutual funds will be stored for later parsing. To modify simply just change the name and ticker number 
EX: `Invesco | 0000001`

![picture alt](DataTwo.JPG)

# Using my Program

After adjusting the `mutual funds.txt` with what data you want to scrape simply run the `main.py`. 


# Thought process and Difficulties

* After spending a day brainstorming I took a look at the format of the data from the SEC. One of the problems that I encountered was that the data was not in proper XML format. This made it difficult for me to use `xml.etree` library.

* Some of the mutual funds did not have the xml info table for me to scrape the data from. However, I noticed that there was a .txt file which contained the company's information along with data in XML format and to access this .txt file.

* I found out for each of the URL's contained this substring `CIK=0001166559`. That means to navigate between companies, all I needed to know was the CIK number. This was the solution I found to navigating between the companies. This same process was used when scraping the financial data from each company.
Changing the document URL from `https://www.sec.gov/Archives/edgar/data/1166559/000110465919029714/0001104659-19-029714-index.htm` 
to
`https://www.sec.gov/Archives/edgar/data/1166559/000110465919029714/0001104659-19-029714.txt`
Getting direct access to the .txt files.

* As for actually scraping the data. Each time I go through a documents I save the entire thing locally in a `buffer.txt` file. From there I do one round of processing to only keep items with `<infoTable> || <ns1:infoTable>` tags. After that cleaning has been done I then parse through it again to save it in its final destination `COMPANY NAME 13F DATE` 

* If I was more comfortable with threads, it would have been a great addition to the program. I would have one thread going to a company and scraping the data to the buffer while another thread is processing the document for saving to .tsv file. 

* While my task was to only look at the most recent financial report, I decided to take a look at how the older .txt files were formatted. One problem is that many of these documents had the correct XML tags, they all were merged into one file with little/no white space in between. I am not sure how you would deal with this kind of problem.

#Libraries

* lxml==4.3.4
* beautifulsoup4==4.7.1
* urllib3==1.23
* requests==2.21.0