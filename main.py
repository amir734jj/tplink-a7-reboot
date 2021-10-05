import os
import time
import urllib.request

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from twisted.internet import task, reactor
from dotenv import load_dotenv

password_field = "#form-login > div.login-field > div > div > div.widget-wrap.text-wrap.password-wrap.allow-visible > " \
                 "span.text-wrap.password-wrap > input.text-text.password-text.password-hidden.l "
login_button = "#login-btn"
reboot_modal = "#top-control-reboot"
submit_reboot = "#reboot_confirm_msg > div.position-center-left > div > div > div.msg-btn-container > div > " \
               "div:nth-child(2) > button "


def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host)  # Python 3.x
        return True
    except:
        return False


def reboot_router():
    driver = webdriver.Chrome(executable_path=os.getenv('chromedriver'))
    driver.get(os.getenv('routerurl'))
    driver.implicitly_wait(15)
    password_elm = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.CSS_SELECTOR, password_field))
    password_elm.clear()
    password_elm.send_keys(os.getenv('ROUTER_PASSWORD'))

    login_elm = driver.find_element_by_css_selector(login_button)
    login_elm.click()

    reboot_elm = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.CSS_SELECTOR, reboot_modal))
    reboot_elm.click()

    submit_elm = WebDriverWait(driver, 10).until(lambda x: x.find_element(By.CSS_SELECTOR, submit_reboot))
    submit_elm.click()

    driver.close()


def run():
    if not connect():
        print("No internet access ...")
        time.sleep(60)  # 60 seconds
        print("Restarting router after second try ...")
        if connect():
            print("Restarting router ...")
            reboot_router()
            time.sleep(300)  # 300 seconds
            print("Successfully restarted the router ...")


if __name__ == "__main__":
    timeout = 60.0  # Sixty seconds

    load_dotenv()
    l = task.LoopingCall(run)
    l.start(timeout)

    reactor.run()
