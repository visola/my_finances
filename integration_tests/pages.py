from functools import wraps
import time

slow_down = False

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
        self.browser.get("http://localhost:5000/accounts")

    @page_action
    def is_displayed(self, account_name):
        return "Accounts" in self.browser.page_source and account_name in self.browser.page_source

class CreateAccountPage():
    def __init__(self, browser):
        self.browser = browser

    @page_action
    def fill_form(self, account):
        self.browser.find_element_by_name("name").send_keys(account.name)
        self.browser.find_element_by_css_selector(f"option[value='{account.type}']").click()

    @page_action
    def submit_form(self):
        self.browser.find_element_by_css_selector("input[type=submit]").click()

    @page_action
    def go(self):
        self.browser.get("http://localhost:5000/accounts/new")

class CreateUserPage():
    def __init__(self, browser):
        self.browser = browser

    @page_action
    def fill_user_form(self, user):
        self.browser.find_element_by_name("name").send_keys(user.name)
        self.browser.find_element_by_name("email").send_keys(user.email)
        self.browser.find_element_by_name("password").send_keys(user.password)

    @page_action
    def go(self):
        self.browser.get("http://localhost:5000/users/new")

    @page_action
    def submit_user_form(self):
        self.browser.find_element_by_css_selector("input[type=submit]").click()

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
        self.browser.find_element_by_link_text("Sign Up").click()

    @page_action
    def go(self):
        self.browser.get("http://localhost:5000")

    @page_action
    def is_displayed(self):
        return self.browser.find_element_by_link_text("Sign Up").is_displayed()

    @page_action
    def login_with(self, user):
        self.browser.find_element_by_name("email").send_keys(user.email)
        self.browser.find_element_by_name("password").send_keys(user.password)
        self.browser.find_element_by_css_selector("input[type=submit]").click()
