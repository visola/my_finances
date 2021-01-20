import configparser
from functools import wraps
import os
import pathlib
import time
from selenium.webdriver.common.by import By

slow_down = False
host_name = "http://localhost:5000"

config = configparser.ConfigParser()

config_file = f"{pathlib.Path(__file__).parent.absolute()}/test_config.ini"
if os.path.exists(config_file):
    config.read(config_file)

default = config['DEFAULT']

if "MY_FINANCES_HOST" in default:
    host_name = default["MY_FINANCES_HOST"]

def page_action(function_to_wrap):
    @wraps(function_to_wrap)
    def decorated_function(*args, **kwargs):
        result = function_to_wrap(*args, **kwargs)
        if slow_down:
            time.sleep(1)
        return result
    return decorated_function

class AccountsPage():
    def __init__(self, browser):
        self.browser = browser

    @page_action
    def go(self):
        self.browser.get(f"{host_name}/accounts")

    @page_action
    def is_displayed(self, account_name):
        return "Accounts" in self.browser.page_source and account_name in self.browser.page_source

class CreateAccountPage():
    def __init__(self, browser):
        self.browser = browser

    @page_action
    def fill_form(self, account):
        self.browser.find_element(by=By.NAME, value="name").send_keys(account.name)
        self.browser.find_element(by=By.CSS_SELECTOR, value=f"option[value='{account.type}']").click()

    @page_action
    def submit_form(self):
        self.browser.find_element(by=By.CSS_SELECTOR, value="input[type=submit]").click()

    @page_action
    def go(self):
        self.browser.get(f"{host_name}/accounts/new")

class CreateUserPage():
    def __init__(self, browser):
        self.browser = browser

    @page_action
    def fill_user_form(self, user):
        self.browser.find_element(by=By.NAME, value="name").send_keys(user.name)
        self.browser.find_element(by=By.NAME, value="email").send_keys(user.email)
        self.browser.find_element(by=By.NAME, value="password").send_keys(user.password)

    @page_action
    def go(self):
        self.browser.get(f"{host_name}/users/new")

    @page_action
    def submit_user_form(self):
        self.browser.find_element(by=By.CSS_SELECTOR, value="input[type=submit]").click()

class DashboardPage():
    def __init__(self, browser):
        self.browser = browser

    @page_action
    def is_displayed(self, username):
        return f"Welcome {username}!" in self.browser.page_source

class LoginPage():
    def __init__(self, browser):
        self.browser = browser

    @page_action
    def click_sign_up_link(self):
        self.browser.find_element(by=By.LINK_TEXT, value="Sign Up").click()

    @page_action
    def go(self):
        self.browser.get(f"{host_name}")

    @page_action
    def is_displayed(self):
        return self.browser.find_element(by=By.LINK_TEXT, value="Sign Up").is_displayed()

    @page_action
    def login_with(self, user):
        self.browser.find_element(by=By.NAME, value="email").send_keys(user.email)
        self.browser.find_element(by=By.NAME, value="password").send_keys(user.password)
        self.browser.find_element(by=By.CSS_SELECTOR, value="input[type=submit]").click()
