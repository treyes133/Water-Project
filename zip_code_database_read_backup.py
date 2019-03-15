import csv,sys,time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup as BS
import numpy as np


zip_code = int(input("Enter zip code :: "))
reader = None
city = None
state = None
with open('fzd.csv', mode='r') as infile:
    reader = csv.reader(infile)
    for row in reader:
        if row[1] == str(zip_code):
            city = row[3].lower().replace(" ","-")
            state = row[4].lower()
            break
print("City of",city+",",state)

caps = DesiredCapabilities().FIREFOX
driver = webdriver.Firefox(capabilities=caps,executable_path="geckodriver.exe")


driver.get("https://www.wunderground.com/weather/us/"+state+"/"+city)

list_of_weather_stations = driver.find_elements_by_tag_name('td')
for element in list_of_weather_stations:
    link_element = element.find_element_by_tag_name('a')
    link_element.click()

    time.sleep(2)

    for option_value in driver.find_elements_by_tag_name("option"):
        if option_value.text == "Yearly Mode":
            option_value.click()
            print("Yearly Mode selected")
            break

    time.sleep(2)
    driver.find_element_by_id('view-btn').click()

    

    driver.find_element_by_xpath('//*[@id="history-tab-group"]/dd[2]/a').click()

    currentURL = driver.current_url
    driver.get(currentURL)
    time.sleep(10)
    #try:
    #    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'history_table')))
    #except TimeoutException:
    #    pass  # Handle the exception here
    
    table = driver.find_element_by_id('history_table').get_attribute('innerHTML')
    if table is ['']:
        print("Table empty")
    else:
        print("Table not empty")

    soup = BS(table, 'lxml')
    soup_text = str(soup)
    print("\n\n")
    table = soup_text.splitlines()
    #print(table)
    print("\n\n")
    new_table = np.zeros((366,10))
    print("NT")
    print(new_table[0])

    with open('table.csv','rw') as file:
        year = table[2][table[2].index('<th class="year-cell">')+len('<th class="year-cell">'):table[2].index('<th class="year-cell">')+len('<th class="year-cell">')+4]
        file.write(y
            
            

    
    

    
    
         

    #driver.get("https://www.wunderground.com/weather/us/"+state+"/"+city)
    sys.exit(0)
