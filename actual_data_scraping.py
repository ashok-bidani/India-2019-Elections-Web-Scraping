# INDIAN ELECTIONS DATA WEB SCRAPER. USES DATA FROM ECI.GOV.IN, SELENIUM, AND BEAUTIFULSOUP.

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas as pd
import os

# PART 0: SET UP
# Fields to hold scraped data
state = []
constituency = []
candidates = []
parties = []
evm_votes = []
postal_votes = []
total_votes = []
vote_percentages = []

# Field to hold state abbreviations (not end data)
state_abbreviations_list = []

# Temporary field to store values for each constituency (will update for each state) (not end data)
constituency_value_holder = []

# Field to hold number of constituencies in each state (not end data)
constituencies_in_state_list = []

# Temporary fields to store data about candidates, parties, EVM votes, postal votes, total votes, and vote percentage in each constituency (not end data). 
constituency_candidates_holder = []
constituency_parties_holder = []
constituency_evm_votes_holder = []
constituency_postal_votes_holder = []
constituency_total_votes_holder = []
constituency_vote_percentages_holder = []

# PART 1: GET ECI STATE CODES/ABBREVIATIONS
# Use selenium to open starting URL
start_url = 'http://results.eci.gov.in/pc/en/constituencywise/ConstituencywiseU011.htm?ac=1'
driver = webdriver.Chrome()
driver.get(start_url)

# Identify state codes for each of India's state & union territories - using HTML text from page source
initial_soup = BeautifulSoup(driver.page_source, 'lxml')
state_options = initial_soup.find('table', class_='tabc').findAll('tr')[10].td.findAll('option')[1:37]
for option in state_options:
    state_abbreviations_list.append(option['value'])
state_abbreviations_list.sort()
print(state_abbreviations_list)

# PART 2: GET NUMBER OF CONSTITUENCIES IN EACH STATE (used for navigating URLs)
for state_code in state_abbreviations_list:
    state_url = 'http://results.eci.gov.in/pc/en/constituencywise/Constituencywise'+state_code+'1.htm?ac=1'
    driver.get(state_url)
    state_soup = BeautifulSoup(driver.page_source, 'lxml')
    constituency_values = state_soup.find('table', class_='tabc').findAll('tr')[10].td.findAll('option')[38:]
    for option in constituency_values:
        constituency_value_holder.append(option['value'])
    constituencies_in_state_list.append(len(constituency_value_holder))
    constituency_value_holder = []
    sleep(1)
print(constituencies_in_state_list)

# PART 3: WEB SCRAPER
# Obtain data for each constituency by looping through all of the states and all of the constituencies in each state
#for i in range(len(state_abbreviations_list)):
for i in range(1,2):
    for j in range(1, (constituencies_in_state_list[i]+1)):
        
        # Navigate to the particular URL        
        constituency_url = 'http://results.eci.gov.in/pc/en/constituencywise/Constituencywise' + state_abbreviations_list[i] + str(j) + '.htm?ac=' + str(j)
        driver.get(constituency_url)

        # Use BeautifulSoup to retrieve relevant data
        constituency_soup = BeautifulSoup(driver.page_source, 'lxml')
        text = constituency_soup.find('table', class_='tabc').findAll('table')[7]
        constituency_info = text.th.string
        tabular_data = text.findAll('tr')
        usable_data = tabular_data[6:(len(tabular_data)-1)]

        # Insert data into temporary fields for each row of the ECI table for that particular constituency. Each row responds to one candidate for office in that constituency. Also, format data as string/int/float and edit data in final 'Total' row to better represent desired information
        for row in usable_data:
            candidate_data = []
            candidate_info = row.findAll('td')
            for data_entry in candidate_info:
                candidate_data.append(data_entry.string)
            print(candidate_data)
            constituency_evm_votes_holder.append(int(candidate_data[3]))
            constituency_postal_votes_holder.append(int(candidate_data[4]))
            constituency_total_votes_holder.append(int(candidate_data[5]))  
            if candidate_data[6] is None:
                constituency_candidates_holder.append('TOTAL')
                constituency_parties_holder.append('TOTAL')
                constituency_vote_percentages_holder.append(100.0)
            else:
                constituency_candidates_holder.append(candidate_data[1].title())
                constituency_parties_holder.append(candidate_data[2])
                constituency_vote_percentages_holder.append(float(candidate_data[6]))
            print(candidate_data[0])

#        # Replace data in stored temporary fields to better represent the 'Total' row
#        constituency_candidates_holder = ['TOTAL' if v is 'Total' else v for v in constituency_vote_percentages_holder]
#        constituency_vote_percentages_holder = ['ALL' if v is '\xa0' else v for v in constituency_vote_percentages_holder]
#        constituency_vote_percentages_holder = [100.0 if v is None else v for v in constituency_vote_percentages_holder]

        # Insert data from temporary fields into end result fields. For state and constituency fields, one value is inserted for each constituency; in the other fields (candidates, parties, evm_votes, etc.), a list of values is inserted which represents the information for each candidate running for office.
        constituency_info_list = constituency_info.replace('\n', '').strip().split('-', 1)
        state.append(constituency_info_list[0])
        constituency.append(constituency_info_list[1])
        candidates.append(constituency_candidates_holder)
        parties.append(constituency_parties_holder)
        evm_votes.append(constituency_evm_votes_holder)
        postal_votes.append(constituency_postal_votes_holder)
        total_votes.append(constituency_total_votes_holder)
        vote_percentages.append(constituency_vote_percentages_holder)

        # Reset temporary fields
        constituency_candidates_holder = []
        constituency_parties_holder = []
        constituency_evm_votes_holder = []
        constituency_postal_votes_holder = []
        constituency_total_votes_holder = []
        constituency_vote_percentages_holder = []

        # Rest one second to approximate human web use
        sleep(1)
        
# Exit the browser
driver.quit()

# PART 4: PRINT RESULTS
print(state)
print(constituency)
print(candidates)
print(parties)
print(evm_votes)
print(postal_votes)
print(total_votes)
print(vote_percentages)