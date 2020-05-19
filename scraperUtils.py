from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
import sys
import os


def secondary_security(browser):
    try:
        button = browser.find_element_by_class_name("secondary-action")
        button.click()
    except Exception as e:
        pass


def input_locator(elements, field):
    elements = [element for element in elements if element.get_attribute("type") == "text"]
    for element in elements:
        if field in element.get_attribute("placeholder"):
            return element


def button_locator(elements, field):
    for element in elements:
        if field == element.get_attribute("data-control-name"):
            return element


def scrape(driver, url, excel_obj, company, page_limit, seen_names):
    for page in range(int(page_limit) + 1): #change to desired page range 
        page_url = ""
        if page == 1:
            page_url = url
        else:
            page_url = url + "&page=" + str(page)
        print("Scraping this URL: " + page_url)
        driver.get(page_url)
        time.sleep(2)
        
        names = []

        for i in range(5):
            # print(i)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/5);")
            while not page_has_loaded(driver):
                pass    
            # print("load")
            source_code = driver.page_source
            soup = BeautifulSoup(source_code)
            names_soup = soup.findAll("span", {"class" : "name actor-name"})

            for names_html in (str(names_soup)[1:-1]).split(', '):
                # print(names_html)
                cur_name = re.findall(r".*\"name actor-name\">([A-Za-z ]*).*", names_html)
                names.extend(cur_name)
                # print(cur_name)

        for name in names:
            if name in seen_names:
                continue
            seen_names.add(name)
            name = name.split(" ")
            wb_act = excel_obj.workbook.active
            wb_act['A' + str(excel_obj.curr_row)] = company
            wb_act['B' + str(excel_obj.curr_row)] = name[0]
            wb_act['C' + str(excel_obj.curr_row)] = name[-1]
            excel_obj.curr_row += 1
        
        excel_obj.saveFile()
        return seen_names


def page_has_loaded(driver):
    page_state = driver.execute_script('return document.readyState;')
    return page_state == 'complete'


def execute(user, pwd, titles, company, pages, excel_obj):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = None
    while True:
        try: 
            browser = webdriver.Chrome(executable_path= os.getcwd() + '/chromedriver', chrome_options=chrome_options)
            browser.implicitly_wait(30)
            browser.get("https://www.linkedin.com")
            browser.find_element_by_class_name("nav__button-secondary").click()
            username = browser.find_element_by_id("username")
            username.send_keys(user)
            password = browser.find_element_by_id("password")
            password.send_keys(pwd)
            password.submit()
            break
        except Exception as e:
            # browser.close()
            print(e)

    #FILTER PAGE
    browser.get("https://www.linkedin.com/search/results/people/?origin=DISCOVER_FROM_SEARCH_HOME")

    #ALL FILTERS BUTTON
    time.sleep(3)
    button_elements = browser.find_elements_by_tag_name("button")
    all_filters_button = button_locator(button_elements, "all_filters")
    all_filters_button.click()

    #ELEMENTS
    input_elements = browser.find_elements_by_tag_name("input")
    button_elements = browser.find_elements_by_tag_name("button")

    #FILTER CURRENT COMPANY
    company_elem = input_locator(input_elements, "current company")
    company_elem.send_keys(company)
    time.sleep(1)
    company_elem.send_keys(Keys.DOWN)
    company_elem.send_keys(Keys.ENTER)
    time.sleep(1)

        #APPLY FILTERS
    apply_button = button_locator(button_elements, "all_filters_apply")
    apply_button.click()

    #BASE FILTER URL
    time.sleep(3)
    filter_url = browser.current_url
    print("Filter URL is: " + filter_url)

    #URL FOR EACH TITLE

    seen = set()

    for title in titles:
        title_url = filter_url + "&title=" + title
        seen = scrape(browser, title_url, excel_obj, company, pages, seen)

    excel_obj.closeFile()
    print("Linkedin email scraping is complete.")