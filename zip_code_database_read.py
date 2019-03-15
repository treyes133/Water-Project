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
run = 1

link_num = 1
links = []
exit_cond = False
while not exit_cond:
    try:
        weather_station = driver.find_element_by_xpath('/html/body/app/city-today/city-today-layout/div/div[2]/section/div[3]/div[3]/div/div[1]/div/div/nearby-stations/div/div[2]/div/ng-saw/div/table/tbody/tr['+str(link_num)+']/td[1]/ng-saw-cell-parser/div/span/a')
        links.append(weather_station.get_attribute("href"))
        link_num += 1
        #print(links)
    except:
        exit_cond = True
    
print(links)


for station in links:
    driver.get(station)
    print(station)

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
    table = soup
    
    headers = [th.text.encode("utf-8").decode() for th in table.select("tr th")]
    
    try:
        file_name = station[station.index("=")+1:]
        year = headers[0]
        month = headers[7]
        headers.insert(0,"Date")
        headers = headers[8:]
        
        with open(str(file_name)+".csv", "w") as f:
            wr = csv.writer(f)
            wr.writerow([year,month])
            wr.writerow(headers)
            wr.writerows([[td.text.encode().decode() for td in row.find_all("td")] for row in table.select("tr + tr")])
    except:
        print("Problem")
    finally:    
        run += 1


    
    

    
    
         

    #driver.get("https://www.wunderground.com/weather/us/"+state+"/"+city)
