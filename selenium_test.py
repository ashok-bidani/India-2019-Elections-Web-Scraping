from selenium import webdriver

browser = webdriver.Chrome()
url = "http://results.eci.gov.in/pc/en/constituencywise/ConstituencywiseS011.htm?ac=1"
browser.get(url)
innerHTML = browser.execute_script("return document.body.innerHTML")
print(len(innerHTML))