from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas as pd
import os

# Fields to hold scraped data
state = []
constituency = []
candidates = []
parties = []
evm_votes = []
postal_votes = []
total_votes = []
percentages_of_votes = []

# Field to hold state abbreviations (not end data)
state_abbreviations_list = []

# Temporary field to store values for each constituency (will update for each state)
constituency_value_holder = []

# Use selenium to open starting URL
start_url = 'http://results.eci.gov.in/pc/en/constituencywise/ConstituencywiseU011.htm?ac=1'
driver = webdriver.Chrome()
driver.get(start_url)

# Identify state codes for each of India's state & union territories - using HTML text from page source
initial_soup = BeautifulSoup(driver.page_source, 'lxml')
state_options = initial_soup.find('table', class_='tabc').findAll('tr')[10].td.findAll('option')[1:]
for option in state_options[:36]:
    state_abbreviations_list.append(option['value'])
state_abbreviations_list.sort()
print(state_abbreviations_list)
print(len(state_abbreviations_list))

for state_code in state_abbreviations_list:
    url = 'http://results.eci.gov.in/pc/en/constituencywise/Constituencywise'+state_code+'1.htm?ac=1'
    driver.get(url)
    inner_html = driver.execute_script("return document.body.innerHTML")
    sleep(2)

driver.quit()