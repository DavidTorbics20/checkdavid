import re
import sys
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

URL = "https://www.kiwi.com/en/search/results/vienna-austria/barcelona-spain/2023-02-20/2023-02-26/"  # noqa: E501
URL = "https://tarkov-market.com/"


def tarkov():
    options = webdriver.ChromeOptions()
    options.add_argument("start-minimized")
    # options.add_argument('disable-infobars')
    options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(URL)

    initial_XPATH = '//*[@id="__layout"]/div/div/div[2]/div[2]/button'
    max_click_SHOW_MORE = 20
    count = 0

    WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH, initial_XPATH))).click()  # noqa: E501

    last_height = driver.execute_script("return document.body.scrollHeight")

    while count < max_click_SHOW_MORE:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        print("scroll down... new height: " + str(new_height))

        if new_height == last_height:
            break

        last_height = new_height

        try:
            new_XPATH = initial_XPATH[:67] + str(count) + initial_XPATH[67:]
            WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, new_XPATH))).click()  # noqa: E501
            print("Button clicked #", count+1)
        except TimeoutException:
            pass
        count += 1

    original_stdout = sys.stdout

    with open('webpage.html', 'w', encoding="utf-8") as f:

        sys.stdout = f
        print(driver.page_source.encode("utf-8"))
        sys.stdout = original_stdout

    driver.quit()


def findall_re():
    items = []
    with open("webpage.html", "r") as f:
        found_items = re.findall('(?<=alt=).*(?= class)', f.read())

    for item in found_items:
        items.append(item.replace('\"', "").replace('&quot;', '\"'))

    for item in items:
        print(item)


if __name__ == "__main__":
    tarkov()
    # findall_re()
