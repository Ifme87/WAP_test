from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
import time

mobile_emulation = {
    "deviceName": "iPhone X" 
}
chrome_options = Options()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
chrome_options.add_argument("--disable-popup-blocking")


service = Service('/usr/bin/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # 1
    driver.get("https://m.twitch.tv")
   
    
    # remove cookies modal
    cookie_modal = WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div[3]')))
    driver.execute_script("arguments[0].remove();", cookie_modal)

    # 2
    WebDriverWait(driver, 3).until(expected_conditions.element_to_be_clickable((By.XPATH, "//*[@id='root']/div[1]/div[1]/nav/div[3]/a"))).click()
    time.sleep(2)

    # 3
    search_box = WebDriverWait(driver, 3).until(
        expected_conditions.presence_of_element_located((By.XPATH, "//*[@id='page-main-content-wrapper']/nav/div/div/div[2]/div/div/input"))
    )
    search_box.send_keys("StarCraft II")
    search_box.send_keys(Keys.ENTER)

    # 4
    time.sleep(3)
    for _ in range(2):
        driver.execute_script("window.scrollBy(0, 100);")
        time.sleep(1)

    # 5

    WebDriverWait(driver, 3).until(expected_conditions.element_to_be_clickable((By.XPATH, "//*[@id='page-main-content-wrapper']/div/div/section[1]/div[4]/a/div/div[2]/div/h2"))).click()
    
    time.sleep(3)
    try:
        consent_popup = driver.find_element(By.XPATH, '//*[@id="page-main-content-wrapper"]/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]')
        if consent_popup:
            WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="channel-player-gate"]/div/div/div[4]/div/button'))).click()
    except Exception:
        pass


    # 6
    time.sleep(3)
    driver.save_screenshot("streamer_page.png")

finally:
    driver.quit()