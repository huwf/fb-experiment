import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

MIN_TIME = timedelta(365)
MIN_FRIENDS = 25

#This requires the Firefox driver (https://github.com/mozilla/geckodriver/releases) be installed to /usr/bin
def validate_account(email, password):
    
    


    driver = webdriver.Firefox()
    driver.get("http://www.facebook.com")

    try:
        if not log_in(driver, email, password):
            return False

        #Check for "validness" of profile here:
        if not validate_profile_age(driver):
            return False

        #Friends check
        if not validate_friends(driver):
            return False

        #Picture check
        pass

        #Other checks?
        pass

    except Exception as e:
        print(e)
        driver.close()
        return False


    driver.close()
    return True


def log_in(driver, email, password):
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
    else:
        return True


def validate_profile_age(driver):
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
    return True


def validate_friends(driver):
    elem = driver.find_element_by_xpath("//a[@data-tab-key='friends']").find_element_by_tag_name("span")
    if int(elem.text) < MIN_FRIENDS:
        driver.close()
        return False
    else:
        return True