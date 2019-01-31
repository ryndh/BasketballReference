from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

import time

driver = webdriver.Chrome('../../Selenium/chromedriver')
driver.get('https://www.basketball-reference.com/leaders/ft_career.html')
# driver.get('https://www.basketball-reference.com/leaders/pts_per_g_career.html')


soup = BeautifulSoup(driver.page_source, 'html.parser')
nba = soup.find('table', id='nba')
links = nba.find_all('a')
names = []
for link in links:
    names.append(link.get_text())

stats = []
for name in names:
    try:
        # wait = WebDriverWait(driver, 5)
        # link = wait.until(EC.presence_of_element_located((By.LINK_TEXT, name)))

        link = driver.find_element_by_link_text(name)
        # driver.execute_script('arguments[0].click()', link)
        link.click()

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table = soup.find('table', id='totals')
        row = table.find('tfoot')
        ftm_stat = int(row.find('td', attrs={'data-stat':'ft'}).get_text())
        fgm_stat = int(row.find('td', attrs={'data-stat': 'fg'}).get_text())
        stats.append(f'{name}: {fgm_stat - ftm_stat}')
        driver.execute_script("window.history.go(-1)")
    except:
        print(f'{name} was not able to be clicked')

print(stats)

driver.quit()