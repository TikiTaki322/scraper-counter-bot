import re
import requests

from time import sleep
from random import shuffle

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


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
        browser.execute_script("arguments[0].click();", sds_button)
        sleep(1.5)
    except NoSuchElementException:
        return f'\nA search of the {source} yielded no results...\n'

    soup = BeautifulSoup(browser.page_source, 'html.parser')
    result = soup.find('a', {'id': 'sds-link-EN'})
    if result == []:
        result = soup.find('a', {'id': 'sds-link-DE'})

    try:
        return f'\nResult from the {source}:\n{source + result["href"]}\n'
    except TypeError:
        return f'\nA search of the {source} yielded no results...\n'


def cymitquimica_parse(source, item):
    browser = webdriver.Chrome()
    browser.get(source)
    sleep(1.5)
    try:
        search_bar = browser.find_element(By.NAME, 'search') if 'text' == browser.find_element(By.NAME, 'search').get_attribute('type') else None
        search_bar.send_keys(item, Keys.RETURN)
        sleep(1)
        item_page = browser.find_element(By.CLASS_NAME, 'js-product-link')
        browser.execute_script("arguments[0].click();", item_page)
        sleep(1.5)
        sds_button = browser.find_element(By.CLASS_NAME, 'js-show-pdf-sds')
        result = sds_button.get_attribute('href')
        return f'\nResult from the {source}:\n{result}\n'
    except (NoSuchElementException, AttributeError):
        return f'\nA search of the {source} yielded no results...\n'


def usp_parse(source, item):
    browser = webdriver.Chrome()
    browser.get(source)
    sleep(1.5)
    search_bar = browser.find_element(By.CLASS_NAME, 'search-query')
    search_bar.send_keys(item)
    sleep(1)
    try:
        collapsed_product = browser.find_element(By.CLASS_NAME, 'typeaheadProductName')
        collapsed_product.click()
    except:
        return f'\nA search of the {source} yielded no results...\n'
    sleep(2.5)
    sds_page = browser.find_element(By.PARTIAL_LINK_TEXT, 'Safety data sheet.pdf')
    browser.execute_script("arguments[0].click();", sds_page)
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

    try:
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
    except (NoSuchElementException, IndexError):
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


def trc_parse(source, item):
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
    sleep(1.6)
    research_tools_checkmark = [i for i in browser.find_elements(By.CLASS_NAME, 'form-container') if i.text.split('\n')[0] == 'Research Tools']
    if research_tools_checkmark != [] and research_tools_checkmark[0].is_enabled():
        browser.execute_script("arguments[0].click();", research_tools_checkmark[0])
        sleep(1.6)
    sds_checkmark = [i for i in browser.find_elements(By.CLASS_NAME, 'form-container') if i.text.split('\n')[0] == 'SDS']
    if sds_checkmark == [] or sds_checkmark[0].text.split('\n')[1] == '0':
        return f'\nA search of the {source} yielded no results...\n'
    else:
        browser.execute_script("arguments[0].click();", sds_checkmark[0])
        sleep(2)

    soup = BeautifulSoup(browser.page_source, 'html.parser')
    all_tags = soup.find_all('a')
    sds_tags = [tag['href'] for tag in all_tags if 'SDS' in tag.get('href', '')]
    result = sds_tags[0]
    return f'\nResult from the {source}:\n{result}\n'


def progen_parse(source, item):
    browser = webdriver.Chrome()
    browser.get(source)
    sleep(1.5)
    search_icon = browser.find_element(By.ID, 'scrollToBannerSearch')
    browser.execute_script("arguments[0].click();", search_icon)
    sleep(1.5)
    search_bar = browser.find_element(By.CLASS_NAME, 'dfd-searchbox-input')
    search_bar.send_keys(item)
    sleep(1.5)
    item_pages = [elem for elem in browser.find_elements(By.CLASS_NAME, 'dfd-card-type-product')
                  if item == elem.find_element(By.CLASS_NAME, 'dfd-card-id').text.split()[-1]]

    if item_pages != [] and item_pages[0].is_enabled():
        item_page = item_pages[0].find_element(By.TAG_NAME, 'a')
        result = item_page.get_attribute('href')
        return f'\nResult from the {source}:\n{result}\n'
    else:
        return f'\nA search of the {source} yielded no results...\n'


def honeywell_parse(source, item):
    browser = webdriver.Chrome()
    browser.get(source)
    sleep(1.5)
    country_navigate_button = browser.find_element(By.ID, 'countryNavigate')
    browser.execute_script("arguments[0].click();", country_navigate_button)
    sleep(1)
    select_region = browser.find_element(By.LINK_TEXT, 'Europe')
    browser.execute_script("arguments[0].click();", select_region)
    sleep(1)
    select_country = browser.find_element(By.LINK_TEXT, 'SWITZERLAND')
    browser.execute_script("arguments[0].click();", select_country)
    sleep(1)
    search_bar = browser.find_element(By.CLASS_NAME, 'isc-button-wrap').find_element(By.TAG_NAME, 'input')
    search_bar.send_keys(item, Keys.RETURN)
    sleep(1)

    try:
        sds_page = browser.find_element(By.CLASS_NAME, 'sds-download')
        browser.execute_script("arguments[0].click();", sds_page)
        sleep(1.5)
        all_open_tabs = browser.window_handles
        browser.switch_to.window(all_open_tabs[-1])
        result = browser.current_url
        return f'\nResult from the {source}:\n{result}\n'
    except NoSuchElementException:
        return f'\nA search of the {source} yielded no results...\n'


def aniara_parse(source, item):
    browser = webdriver.Chrome()
    browser.get(source)
    sleep(1.5)
    search_bar = browser.find_element(By.ID, 'l-Search')
    search_bar.send_keys(item, Keys.RETURN)
    sleep(0.5)

    try:
        sds_page = browser.find_element(By.PARTIAL_LINK_TEXT, 'MSDS')
        result = sds_page.get_attribute('href')
        return f'\nResult from the {source}:\n{result}\n'
    except NoSuchElementException:
        return f'\nA search of the {source} yielded no results...\n'


def biorad_parse(source, item):
    browser = webdriver.Chrome()
    browser.get(source)
    sleep(2)
    decline_button = browser.find_element(By.LINK_TEXT, 'Decline')
    browser.execute_script("arguments[0].click();", decline_button)
    sleep(1)
    search_bar = browser.find_element(By.ID, 'views-exposed-form-brc-acquia-search-brc-site-search').find_element(By.TAG_NAME, 'input')
    search_bar.send_keys(item, Keys.RETURN)
    sleep(1.5)

    try:
        pdf_button = browser.find_element(By.LINK_TEXT, 'Download PDF')
        browser.execute_script("arguments[0].click();", pdf_button)
        sleep(1)
        all_open_tabs = browser.window_handles
        browser.switch_to.window(all_open_tabs[-1])
        result = browser.current_url
        return f'\nResult from the {source}:\n{result}\n'
    except NoSuchElementException:
        return f'\nA search of the {source} yielded no results...\n'


def edqm_parse(source, item):
    browser = webdriver.Chrome()
    browser.get(source)
    sleep(1.5)
    search_option = browser.find_element(By.NAME, 'vSelectName')
    search_option.send_keys('Catalogue Code')
    search_type = browser.find_element(By.NAME, 'vContains')
    search_type.send_keys('is exactly')
    sleep(0.5)
    search_bar = browser.find_element(By.NAME, 'vtUserName')
    search_bar.send_keys(item, Keys.RETURN)
    sleep(0.5)

    try:
        item_page = browser.find_element(By.LINK_TEXT, item)
        browser.execute_script("arguments[0].click();", item_page)
        sleep(0.5)
        all_open_tabs = browser.window_handles
        browser.switch_to.window(all_open_tabs[-1])

        sds_list = [elem for elem in browser.find_elements(By.TAG_NAME, 'a') if 'click to download safety data sheet' in elem.text.lower()]
        browser.execute_script("arguments[0].click();", sds_list[0])
        all_open_tabs = browser.window_handles
        browser.switch_to.window(all_open_tabs[-1])

        all_links = [elem for elem in browser.find_elements(By.TAG_NAME, 'a') if 'SDS_' in elem.text]
        english_link = [elem.get_attribute('href') for elem in all_links if elem.text.__contains__("EN")]
        result = english_link[0] if english_link else all_links[0].get_attribute('href')
        return f'\nResult from the {source}:\n{result}\n'
    except (NoSuchElementException, IndexError):
        return f'\nA search of the {source} yielded no results...\nIn this case, it means that the item is most likely not hazard\n'


def chemicalsafety_parse(source, item):
    browser = webdriver.Chrome()
    browser.get(source)
    sleep(1.5)
    search_bar = browser.find_element(By.TAG_NAME, 'input') if browser.find_element(By.TAG_NAME, 'input').get_attribute('type') == 'text' else None
    search_bar.send_keys(item, Keys.RETURN)
    sleep(1)
    result_block = browser.find_element(By.ID, 'cs_divResults')
    if result_block.text == '':
        return f'\nA search of the {source} yielded no results...\n'

    all_tags = [elem for elem in browser.find_elements(By.TAG_NAME, 'td')]
    all_links, intermediate_results = list(), list()
    for tag in all_tags:
        try:
            elem = tag.find_element(By.TAG_NAME, 'a').get_attribute('href')
            if elem and elem not in all_links:
                all_links.append(elem)
        except NoSuchElementException:
            pass

    browser.close()
    length_all_links = len(all_links)
    if length_all_links >= 7:
        shuffle(all_links)
        all_links = all_links[:6]

    for link in all_links:
        browser = webdriver.Chrome()
        browser.get(link)
        sleep(2)
        try:
            sds_button = browser.find_element(By.ID, 'sds_links').find_element(By.TAG_NAME, 'a')
            result = sds_button.get_attribute('href')
            intermediate_results.append(result)
            browser.close()
        except NoSuchElementException:
            pass

    results = f'\nThe {source} source gives {length_all_links} sds-documents, ' \
              f'but we took only {len(intermediate_results)} to avoid slowing down the program:\n\n'
    counter = 1
    for result in intermediate_results:
        results += f'{counter}. {result}\n'
        counter += 1
    return results


def vwr_parse(source, item):
    browser = webdriver.Chrome()
    browser.get(source)
    sleep(1.5)
    search_bar = browser.find_element(By.ID, 'msdsSearchPartNumber')
    search_bar.send_keys(item, Keys.RETURN)
    sleep(1.5)

    try:
        sds_button = [elem for elem in browser.find_elements(By.TAG_NAME, 'a') if 'View SDS' == elem.text]
        result = sds_button[0].get_attribute('href')
        return f'\nResult from the {source}:\n{result}\n'
    except (NoSuchElementException, IndexError):
        return f'\nA search of the {source} yielded no results...\n'


def bdbiosciences_parse(source, item):
    browser = webdriver.Chrome()
    browser.get(source)
    sleep(1.5)
    search_icon = browser.find_element(By.CLASS_NAME, 'bdb-header__search-nav-link')
    search_icon.click()
    sleep(1)
    search_bar = browser.find_element(By.ID, 'searchModal').find_element(By.TAG_NAME, 'input')
    search_bar.send_keys(item, Keys.RETURN)
    sleep(1.5)

    try:
        item_page = browser.find_element(By.CLASS_NAME, 'card-title')
        browser.execute_script("arguments[0].click();", item_page)
        sleep(1.5)
        sds_button = browser.find_element(By.LINK_TEXT, 'Safety Data Sheet')
        browser.execute_script("arguments[0].click();", sds_button)
        sleep(1.5)
        lang_popup = browser.find_element(By.CLASS_NAME, 'data-sheets-container_multi-lang-popup').find_element(By.CLASS_NAME, 'btn')
        browser.execute_script("arguments[0].click();", lang_popup)
        sleep(1.5)
        all_open_tabs = browser.window_handles
        browser.switch_to.window(all_open_tabs[-1])
        result = browser.current_url
        return f'\nResult from the {source}:\n{result}\n'
    except NoSuchElementException:
        return f'\nA search of the {source} yielded no results...\n'


def main(item):
    print(f'\t\t\tWelcome! Searching for an item -> {item}')
    print(sigma_parse(urls_db['sigma_parse'], item)) # search by Sigma, Supelco, Merc etc.
    #print(cymitquimica_parse(urls_db['cymitquimica_parse'], item)) # search by TCI, TRC, TLC, USP, EDQM, Reagecon, Biosynth, Mikromol etc.
    #print(usp_parse(urls_db['usp_parse'], item))
    #print(abcam_parse(urls_db['abcam_parse'], item))
    #print(tci_parse(urls_db['tci_parse'], item))
    #print(trc_parse(urls_db['trc_parse'], item))
    #print(progen_parse(urls_db['progen_parse'], item))
    #print(honeywell_parse(urls_db['honeywell_parse'], item))
    #print(aniara_parse(urls_db['aniara_parse'], item)) # search by Biophen
    #print(biorad_parse(urls_db['biorad_parse'], item))
    #print(edqm_parse(urls_db['edqm_parse'], item))
    #print(chemicalsafety_parse(urls_db['chemicalsafety_parse'], item)) # search by product name istead of catalog
    #print(vwr_parse(urls_db['vwr_parse'], item)) # search for Roshe, VWR
    #print(bdbiosciences_parse(urls_db['bdbiosciences_parse'], item)) # search for BD Biosciences
    pass


urls_db = {
    'sigma_parse': 'https://www.sigmaaldrich.com',
    'cymitquimica_parse': 'https://cymitquimica.com',
    'usp_parse': 'https://store.usp.org/',
    'abcam_parse': 'https://www.abcam.com/',
    'tci_parse': 'https://www.tcichemicals.com/US/en',
    'trc_parse': 'https://www.lgcstandards.com/US/en/',
    'progen_parse': 'https://www.progen.com',
    'honeywell_parse': 'https://lab.honeywell.com/en/sds',
    'aniara_parse': 'https://www.aniara.com/product-documentation.html',
    'biorad_parse': 'https://www.bio-rad.com/',
    'edqm_parse': 'https://crs.edqm.eu/',
    'chemicalsafety_parse': 'https://chemicalsafety.com/sds-search',
    'vwr_parse': 'https://uk.vwr.com/store/search/searchMSDS.jsp',
    'bdbiosciences_parse': 'https://www.bdbiosciences.com',
}

test_items = ['']

flag = 0
data = input('Enter the catalog number: ') if flag else test_items[0]
main(data)
