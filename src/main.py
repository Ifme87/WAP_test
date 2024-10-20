import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys


@pytest.fixture(scope="function")
def driver():
    # configure mobile emulation
    mobile_emulation = {"deviceName": "iPhone X"}
    chrome_options = Options()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    chrome_options.add_argument("--disable-popup-blocking")
    
    # setup Chrome WebDriver
    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    yield driver
    
    # quit the driver after the test
    driver.quit()

def test_twitch_mobile_search(driver):

    # 1 go to twitch
    driver.get("https://m.twitch.tv")
    
    # remove cookies modal
    cookie_modal = WebDriverWait(driver, 3).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div[3]')))
    driver.execute_script("arguments[0].remove();", cookie_modal)

    # 2 click in the search icon
    WebDriverWait(driver, 3).until(expected_conditions.element_to_be_clickable((By.XPATH, "//*[@id='root']/div[1]/div[1]/nav/div[3]/a"))).click()
    time.sleep(2)

    # 3 input StarCraft II
    search_box = WebDriverWait(driver, 3).until(
        expected_conditions.presence_of_element_located((By.XPATH, "//*[@id='page-main-content-wrapper']/nav/div/div/div[2]/div/div/input"))
    )
    search_box.send_keys("StarCraft II")
    search_box.send_keys(Keys.ENTER)

    # 4 scroll down 2 times
    time.sleep(3)
    for _ in range(2):
        driver.execute_script("window.scrollBy(0, 100);")
        time.sleep(1)

    # 5 select one streamer
    WebDriverWait(driver, 3).until(expected_conditions.element_to_be_clickable((By.XPATH, "//*[@id='page-main-content-wrapper']/div/div/section[1]/div[4]/a/div/div[2]/div/h2"))).click()
    time.sleep(3)

    # define and remove popup if any found
    try:
        consent_popup = driver.find_element(By.XPATH, '//*[@id="page-main-content-wrapper"]/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]')
        if consent_popup:
            WebDriverWait(driver, 3).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="channel-player-gate"]/div/div/div[4]/div/button'))).click()
    except Exception:
        pass

    # 6 on the streamer page wait until all is load and take a screenshot
    time.sleep(5)
    driver.save_screenshot("streamer_page.png")
