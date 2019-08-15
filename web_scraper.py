from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

# This function makes an HTTP GET request to retrieve the content at "url"
def retrieve_html(url):
    try: 
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        log_error('Error processing request to {0}: {1}'.format(url, str(e)))
        return None

# Return True if response is HTML, False otherwise    
def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return(resp.status_code == 200
          and content_type is not None
          and content_type.find('html') > -1)

# Error-logging function which prints any errors.
def log_error(e):
    print(e)

# The web-scraping of Indian election results will actually take several iterations because the country is broken up into states, each of which have a corresponding alphanumeric code, and then each state is broken up into constituencies, each of which is numbered. The election result URL for each constituency includes both of these, for example: "http://results.eci.gov.in/pc/en/constituencywise/ConstituencywiseU011.htm?ac=1" where U01 represents the state code and 1 is the constituency value.

# So I will scrape the initial page for the state alphanumeric codes, and then scrape a page from each state to obtain the list of constituency values for that state. Finally, I will scrape each individual constituency page to obtain the data I actually want about election results (candidates, parties, and number/percentage of votes for each candidate). There should be 543 constituencies if the data is complete.

# PART 1: Obtain all possible URLs to scrape data from

# First I retrieve the list of state codes.
# Pass the initial landing page for 2019 Indian Election to the "retrieve_html" function
initial_raw_html = retrieve_html('http://results.eci.gov.in/pc/en/constituencywise/ConstituencywiseU011.htm?ac=1')

# Use Beautiful Soup to narrow down text to the state codes from the initial HTML document, which is basically one large table
# Use the "lxml" parser
initial_html = BeautifulSoup(initial_raw_html, "lxml")
bigtable = initial_html.find('table', class_='tabc')
bigrow = bigtable.findAll('tr')[10]
# State codes are included under "options" tags
state_options = bigrow.td.findAll('option')[1:]

# Create a list to hold the state codes/abbreviations
state_abbreviations_list = []

# The last (37th) "option" tag refers to something else from the states, so we exclude that one and take the option values in options up to 36. Then we sort the list.
for option in state_options[:36]:
    state_abbreviations_list.append(option['value'])
state_abbreviations_list.sort()
print(state_abbreviations_list)



