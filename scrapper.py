from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

START_URL = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome("chromedriver.exe")
browser.get(START_URL)
time.sleep(10)
headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyperlink", "planet_type", "orbital_radius", "orbital_period", "eccentricity"]
planet_data = []
new_planet_data = []
final_planet_data = []

def scrape():
    for i in range(0, 452):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        for ul_tag in soup.find_all("ul", attrs = {"class", "exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if(index == 0):
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            hyperlink_li_tag = li_tags[0]
            temp_list.append("https://exoplanets.nasa.gov" + hyperlink_li_tag.find_all("a", href = True)[0]["href"])

            planet_data.append(temp_list)

        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
    # with open("scrapper_2.csv", "w") as f:
        # csvwriter = csv.writer(f)
        # csvwriter.writerow(headers)
        # csvwriter.writerows(planet_data)

def scrape_more_data(href):
    page = requests.get(href)
    soup_object = BeautifulSoup(page.contents, "html.parser")
    for tr_tag in soup_object.find_all("tr", attrs = {"class": "fact_row"}):
        td_tags = tr_tag.find_all("td")
        temp_list = []
        for td_tag in td_tags:
            try:
                temp_list.append(td_tag.find_all("div", attrs = {"class":"value"})[0].contents[0])
            except:
                temp_list.append("")
        new_planet_data.append(temp_list)

scrape()
for index, data in enumerate(planet_data):
    scrape_more_data(data[5])

for index, data in enumerate(planet_data):
    # new_planet_data_element = new_planet_data[index]
    # new_planet_data_element = [elem.replace("\n", "")for elem in new_planet_data_element]
    # new_planet_data_element = new_planet_data_element[:7]
    final_planet_data.append(data + final_planet_data[index])

with open("final.csv", "w") as f:
    csv_writer = csv.writer(f)
    csv_writer = writerow(headers)
    csv_writer.writerow(final_planet_data)
