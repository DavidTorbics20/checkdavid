
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


url = "https://www.kiwi.com/en/search/results/vienna-austria/barcelona-spain/2023-02-20/2023-02-26/"

def main():
    PATH = "C:\\Programme (x86)\\chromedriver.exe"
    driver = webdriver.Chrome(PATH)

    driver.get(url)
    time.sleep(10)

    print(driver.page_source)
    driver.quit()


if __name__ == "__main__":
    main()
