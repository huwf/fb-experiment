import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#This requires the Firefox driver (https://github.com/mozilla/geckodriver/releases) be installed to /usr/bin
def validate_account(email, password):
    MIN_TIME = timedelta(365)
    MIN_FRIENDS = 25


    driver = webdriver.Firefox()
    driver.get("http://www.facebook.com")

    elem = driver.find_element_by_name("email")
    elem.clear()
    elem.send_keys(email)

    elem = driver.find_element_by_name("pass")
    elem.clear()
    elem.send_keys(password, Keys.RETURN)
    #Delay while wait for login (there's actually a better way to do this with selenium.webdriver.support.ui.WebDriverWait)
    time.sleep(5)

    elem = driver.find_element_by_id("pageTitle")

    if "log in" in elem.text.lower():
        driver.close()
        return False # Password was wrong

    #Check for "validness" of profile here:
    driver.find_element_by_xpath("//div[@data-click='profile_icon']").click()
    time.sleep(5)
    elem = driver.find_element_by_name("profile_id")
    profile_id = elem.get_attribute('value')

    #Account age check
    #Bit of a hack - check their earliest profile pic
    driver.find_element_by_xpath("//img[@class='profilePic img']").click()
    time.sleep(5)
    elem = driver.find_element_by_xpath("//img[@class='spotlight']")
    elem.send_keys(Keys.ARROW_LEFT)
    time.sleep(5)
    elem = driver.find_element_by_xpath("//span[@id='fbPhotoSnowliftTimestamp']/a/abbr/span[@class='timestampContent']")

    created_date = datetime.strptime(elem.text, "%d %B %Y")

    if datetime.now() - created_date < MIN_TIME:
        driver.close()
        return False

    elem.send_keys(Keys.ESCAPE)

    #Friends check
    elem = driver.find_element_by_xpath("//a[@data-tab-key='friends']").find_element_by_tag_name("span")
    if int(elem.text) < MIN_FRIENDS:
        driver.close()
        return False

    #Picture check

    #Other checks?


    driver.close()
    return True