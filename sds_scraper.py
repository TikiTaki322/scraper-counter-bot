import re

from time import sleep

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By


def sigma_parse(source, item):
    browser = webdriver.Chrome()
    browser.get(source)
    sleep(1.5)
    open_search = browser.find_element(By.ID, "header-search-search-wrapper-input")
    open_search.send_keys(item)
    sleep(1.5)
    # Checking if possible to retrieve quickly sds after insertion the catalog number into the search bar
    sds_div_quick_access = browser.find_element(By.ID, 'header-search-search-wrapper-menu')
    sds_quick_access = [tag for tag in sds_div_quick_access.find_elements(By.TAG_NAME, 'a') if 'SDS' in tag.get_attribute('href').upper()]
    if sds_quick_access != [] and sds_quick_access[0].is_enabled():
        result = sds_quick_access[0].get_attribute('href')
        return f'\nResult from the {source}:\n{result}\n'
    else:
        pass

    button = browser.find_element(By.ID, 'header-search-submit-search-wrapper')
    browser.execute_script("arguments[0].click();", button)
    sleep(2)

    try:
        sds_button = browser.find_element(By.CLASS_NAME, 'MuiTypography-colorSecondary')
        sds_button.click()
        sleep(1.5)
    except:
        return f'\nA search of the {source} yielded no results...\n'

    soup = BeautifulSoup(browser.page_source, 'html.parser')
    result = soup.find('a', {'id': 'sds-link-EN'})
    if result == []:
        result = soup.find('a', {'id': 'sds-link-DE'})

    try:
        return f'\nResult from the {source}:\n{source + result["href"]}\n'
    except TypeError:
        return f'\nA search of the {source} yielded no results...\n'


def lgc_parse(source, item):
    browser = webdriver.Chrome()
    browser.get(source)
    sleep(1.5)
    open_search = browser.find_element(By.CLASS_NAME, 'aa-DetachedSearchButton')
    browser.execute_script("arguments[0].click();", open_search)
    sleep(2)
    search_bar = browser.find_element(By.CLASS_NAME, 'aa-Input')
    search_bar.send_keys(item)
    sleep(1.5)
    # Checking if possible to get quickly sds after insertion the catalog number in search bar
    sds_quick_access = [elem for elem in browser.find_elements(By.CLASS_NAME, 'product-info') if 'SDS' in elem.get_attribute('href').upper()]
    if sds_quick_access != [] and sds_quick_access[0].is_enabled():
        result = sds_quick_access[0].get_attribute('href')
        return f'\nResult from the {source}:\n{result}\n'
    else:
        pass

    search_button = browser.find_element(By.CLASS_NAME, 'aa-SubmitButton')
    browser.execute_script("arguments[0].click();", search_button)
    sleep(2)
    research_tools_checkmark = [i for i in browser.find_elements(By.CLASS_NAME, 'form-container') if i.text.split('\n')[0] == 'Research Tools']
    if research_tools_checkmark != []:
        research_tools_checkmark[0].click()
    sleep(2)
    sds_checkmark = [i for i in browser.find_elements(By.CLASS_NAME, 'form-container') if i.text.split('\n')[0] == 'SDS']
    if sds_checkmark == [] or sds_checkmark[0].text.split('\n')[1] == '0':
        return f'\nA search of the {source} yielded no results...\n'
    else:
        sds_checkmark[0].click()
    sleep(2)

    soup = BeautifulSoup(browser.page_source, 'html.parser')
    all_tags = soup.find_all('a')
    sds_tags = [tag['href'] for tag in all_tags if 'SDS' in tag.get('href', '')]
    result = sds_tags[0]
    return f'\nResult from the {source}:\n{result}\n'


def usp_parse(source, item):
    browser = webdriver.Chrome()
    browser.get(source)
    sleep(2.5)
    search_bar = browser.find_element(By.CLASS_NAME, 'search-query')
    search_bar.send_keys(item)
    sleep(1.5)
    try:
        collapsed_product = browser.find_element(By.CLASS_NAME, 'typeaheadProductName')
        collapsed_product.click()
    except:
        return f'\nA search of the {source} yielded no results...\n'
    sleep(2)
    sds = browser.find_element(By.PARTIAL_LINK_TEXT, 'Safety data sheet.pdf')
    sds.click()
    sleep(1.5)
    all_open_tabs = browser.window_handles
    browser.switch_to.window(all_open_tabs[-1])
    result = browser.current_url
    return f'\nResult from the {source}:\n{result}\n'


def abcam_parse(source, item):
    pass


def main(item):
    print(f'\t\t\tWelcome! Searching for an item -> {item}')
    print(sigma_parse(urls_db[0], item))
    #print(lgc_parse(urls_db[1], item))
    #print(usp_parse(urls_db[2], item))
    #print(abcam_parse(urls_db[3], item))
    pass


urls_db = ['https://www.sigmaaldrich.com', 'https://www.lgcstandards.com/US/en/', 'https://store.usp.org/', ]
test_items = ['342920-50G', 'S0756-50MG', 'U829930', 'TRC-V097110-50MG', '1006801', '1499414', 'MM0084.01-0025', 'TRC-N424598-5G', 'U829930', 'TRC-E521160-500MG', '150495']
# Add the https://www.scientificlabs.ie/ to source list

#x = input('Enter the catalog number: ')
#main(x)
main(test_items[0])

