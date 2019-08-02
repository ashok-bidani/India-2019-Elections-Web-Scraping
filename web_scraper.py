from bs4 import BeautifulSoup
import urllib.request as ur

#loop through pages
for i in range (0,6):
    
    #read and open url to scrape
    #note: for India election I will first need to scrape "http://results.eci.gov.in/pc/en/partywise/partywiseresult-U01.htm" for the "Select State" menu and capture all of the values in that option as this is part of the url of each state. Then I will loop through the items in this list to scrape each state detail url.
    urlToScrape = "https://www.city.ac.uk/courses?level=Undergraduate&p=" + str(i * 10 + 1)
    r = ur.urlopen(urlToScrape).read()
    soup = BeautifulSoup(r, "lxml")
    
    #attributes for each course
    #note: here I will just need to 
    courseList = soup.find_all('div', attrs={'class': 'course-finder_results_item course-finder_results_item - undergraduate'})