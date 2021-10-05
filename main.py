import os
import time
import urllib.request

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from twisted.internet import task, reactor


def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host)  # Python 3.x
        return True
    except:
        return False


def reset_router():
    driver = webdriver.Chrome(executable_path='./chromedriver')
    driver.get("http://tplinkwifi.net/")
    password_field = driver.find_element_by_css_selector(
        "#form-login > div.login-field > div > div > div.widget-wrap.text-wrap.password-wrap.allow-visible > span.text-wrap.password-wrap > input.text-text.password-text.password-hidden.l")
    password_field.clear()
    password_field.send_keys(os.getenv('ROUTER_PASSWORD'))

    login = driver.find_element_by_css_selector("#login-btn")
    login.click()

    reset = driver.find_element_by_css_selector("#top-control-reboot")
    reset.click()

    reset_submit = driver.find_element_by_css_selector(
        "#reboot_confirm_msg > div.position-center-left > div > div > div.msg-btn-container > div > div:nth-child(2) > button")
    reset_submit.click()

    driver.close()


def run():
    if not connect():
        time.sleep(60)
        if connect():
            reset_router()
            time.sleep(180)


if __name__ == "__main__":
    timeout = 60.0  # Sixty seconds

    l = task.LoopingCall(run)
    l.start(timeout)  # call every sixty seconds

    reactor.run()
