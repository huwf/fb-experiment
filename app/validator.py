import time 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


#This requires the Firefox driver (https://github.com/mozilla/geckodriver/releases) be installed to /usr/bin
def validate_account(email, password):
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

    elem = driver.find_element_by_name("profile_id")
    profile_id = elem.get_attribute('value')

    #Account age check

    #Friends check
    elem = driver.find_element_by_xpath("//a[@data-tab-key='friends']").find_element_by_tag_name("span")
    if int(elem.text) < MIN_FRIENDS:
        return False

    #Picture check

    #Other checks?


    driver.close()