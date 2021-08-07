from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests 

START_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"

browser = webdriver.Chrome("/Users/saakshi/Downloads/PRO-C-128/venv/chromedriver-Windows")

browser.get(START_URL)
time.sleep(10)

headers = ["Star","Constellation","Right_ascension","Declination","App._mag.","Distance","Spectral_type","Brown_dwarf","Mass","Radius","Orbital_period","Semimajor_axis","Ecc.","Discovery_year"]
star_data = []
new_star_data = []
def scrape():
    for i in range(0,428):
        soup = BeautifulSoup(browser.page_source,"html.parser")
        for ul_tag in soup.find_all("ul",attrs = {"class","Star"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index,li_tag in enumerate(li_tags):
                if index == 0 :
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except: 
                        temp_list.append("")
            star_data.append(temp_list)
        browser.find_element_by_xpath('')


def scrape_more_data(hyperlink):
    try :
        page = requests.GET(hyperlink)
        soup = BeautifulSoup(page.content,"html.parser")
        temp_list = []
        for tr_tag in soup.find_all("tr",attrs = {"class":"fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div",attrs={"class":"value"})[0].contents[0])
                except:
                    temp_list.append("")
        new_star_data.append(temp_list)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)                  

scrape()
for data in star_data:
    scrape_more_data(data[5])
final_star_data=[]

for index,data in enumerate(planet_data):
    new_star_data_element = new_star_data[index]
    new_star_data_element = [elem.replace("\n","")for elem in new_star_data_element]
    new_star_data_element = new_star_data_element[:7]
    final_star_data.append(data + new_star_data_element)
    

    with open ("scraper_2.csv","w") as f:
        csvwriter  = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(star_data)