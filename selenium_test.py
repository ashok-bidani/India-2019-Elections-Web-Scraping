from selenium import webdriver

driver = webdriver.Chrome()
url = "http://results.eci.gov.in/pc/en/constituencywise/ConstituencywiseS011.htm?ac=1"
driver.get(url)
inner_html = driver.execute_script("return document.body.innerHTML")
print(inner_html)
driver.quit()