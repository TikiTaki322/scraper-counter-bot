import re
import requests

from time import sleep

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


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
    if research_tools_checkmark != [] and research_tools_checkmark[0].is_enabled():
        #research_tools_checkmark[0].click()
        browser.execute_script("arguments[0].click();", research_tools_checkmark[0])
    sleep(2)
    sds_checkmark = [i for i in browser.find_elements(By.CLASS_NAME, 'form-container') if i.text.split('\n')[0] == 'SDS']
    if sds_checkmark == [] or sds_checkmark[0].text.split('\n')[1] == '0':
        return f'\nA search of the {source} yielded no results...\n'
    else:
        #sds_checkmark[0].click()
        browser.execute_script("arguments[0].click();", sds_checkmark[0])
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
    sleep(2.5)
    sds = browser.find_element(By.PARTIAL_LINK_TEXT, 'Safety data sheet.pdf')
    sds.click()
    sleep(1.5)
    all_open_tabs = browser.window_handles
    browser.switch_to.window(all_open_tabs[-1])
    result = browser.current_url
    return f'\nResult from the {source}:\n{result}\n'


# Here need to find solution for normal downloading process without hardcoding
def abcam_parse(source, item):
    browser_options = Options()
    prefs = {
        "profile.default_content_setting_values.automatic_downloads": 1,
        "download.default_directory": f"C:\\users\wentu\downloads\\{item}-sds-parse"
    }
    browser_options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(browser_options)
    browser.get(source)
    sleep(1.5)
    search_bar = browser.find_element(By.ID, 'searchfieldtop')
    search_bar.send_keys(item)
    search_button = browser.find_element(By.ID, 'btnSearch')
    search_button.click()
    sleep(2)
    description_menu = [elem for elem in browser.find_elements(By.CLASS_NAME, 'h3') if 'Datasheets and documents' in elem.text]
    if description_menu != [] and description_menu[0].is_enabled():
        browser.execute_script("arguments[0].click();", description_menu[0])
        sleep(0.3)
        # Maybe better not specify exact country. If it will trigger an errors, need to change the code
        select_country = browser.find_element(By.ID, 'pdf-links__select--country')
        specified_country = [elem for elem in select_country.find_elements(By.TAG_NAME, 'option') if 'United' in elem.text]
        specified_country[1].click()
        sleep(0.3)
        select_language = browser.find_element(By.ID, 'pdf-links__select--language')
        specified_language = [elem for elem in select_language.find_elements(By.TAG_NAME, 'option') if 'Select language' not in elem.text]
        specified_language[0].click()
        sleep(0.3)

        all_tags = [tag for tag in browser.find_elements(By.CLASS_NAME, 'pdf-links__sds-download-btn')]
        counter = 1
        print(f'\nResult from the {source}:\nTotal number of files: {len(all_tags)}')
        for tag in all_tags:
            browser.execute_script("arguments[0].click();", tag)
            print(f"Download file №{counter} -> {tag.get_attribute('data-uri').split('/')[5]}")
            counter += 1
            sleep(0.5)
        return ''
    else:
        return f'\nA search of the {source} yielded no results...\n'


def tci_parse(source, item):
    browser = webdriver.Edge()
    browser.get(source)
    sleep(1.5)
    search_bar = browser.find_element(By.ID, 'js-site-search-input')
    search_bar.send_keys(item)
    sleep(1.3)
    search_button = browser.find_element(By.CLASS_NAME, 'js_search_button')
    search_button.click()
    sleep(1.3)
    current_url = browser.current_url
    browser.close()
    sleep(0.3)
    # Re-entry to site
    browser = webdriver.Edge()
    browser.get(current_url)
    sleep(1.5)

    item_page = browser.find_element(By.CLASS_NAME, 'text-concat')
    if item_page.is_enabled() and item_page.tag_name == 'div':
        item_page_href = item_page.find_element(By.TAG_NAME, 'a')
        result = item_page_href.get_attribute('href')
        return f'\nResult from the {source}:\n{result}\n'
    else:
        return f'\nA search of the {source} yielded no results...\n'


def main(item):
    print(f'\t\t\tWelcome! Searching for an item -> {item}')
    #print(sigma_parse(urls_db[0], item))
    #print(lgc_parse(urls_db[1], item))
    #print(usp_parse(urls_db[2], item))
    #print(abcam_parse(urls_db[3], item))
    print(tci_parse(urls_db[4], item))
    pass


urls_db = [
    'https://www.sigmaaldrich.com',
    'https://www.lgcstandards.com/US/en/',
    'https://store.usp.org/',
    'https://www.abcam.com/',
    'https://www.tcichemicals.com/US/en',
]

test_items = ['M0795-25ML', 'ab150686', 'MM0084.01-0025', 'TRC-N424598-5G', '150495']

# Add the https://www.scientificlabs.ie/ to source list
# Add the https://www.merckmillipore.com/
# https://www.aniara.com/ for brand "BIOPHEN"; Test cat item - 221802
# https://www.progen.com/ for brand "PROGEN"
# https://www.honeywell.com/us/en ---- https://lab.honeywell.com/en/sds

#x = input('Enter the catalog number: ')
#main(x)

main(test_items[0])
