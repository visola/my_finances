class AccountsPage():
    def __init__(self, browser):
        self.browser = browser

    def go(self):
        self.browser.get("http://localhost:5000/accounts")

        
class CreateUserPage():
    def __init__(self, browser):
        self.browser = browser
    
    def fill_user_form(self, user):
        self.browser.find_element_by_name("name").send_keys(user.name)
        self.browser.find_element_by_name("email").send_keys(user.email)
        self.browser.find_element_by_name("password").send_keys(user.password)

    def go(self):
        self.browser.get("http://localhost:5000/users/new")

    def submit_user_form(self):
        self.browser.find_element_by_css_selector("input[type=submit]").click()

class DashboardPage():
    def __init__(self, browser):
        self.browser = browser

    def is_displayed(self, username):
        return f"Welcome {username}!" in self.browser.page_source

class LoginPage():
    def __init__(self, browser):
        self.browser = browser

    def click_sign_up_link(self):
        self.browser.find_element_by_link_text("Sign Up").click()

    def go(self):
        self.browser.get("http://localhost:5000")

    def is_displayed(self):
        return self.browser.find_element_by_link_text("Sign Up").is_displayed()

    def login_with(self, user):
        self.browser.find_element_by_name("email").send_keys(user.email)
        self.browser.find_element_by_name("password").send_keys(user.password)
        self.browser.find_element_by_css_selector("input[type=submit]").click()
