import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .entities import User
from .pages import AccountsPage, CreateAccountPage, CreateUserPage, DashboardPage, LoginPage

@pytest.fixture
def browser():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.close()

@pytest.fixture
def accounts_page(browser):
    return AccountsPage(browser)

@pytest.fixture
def create_account_page(browser):
    return CreateAccountPage(browser)

@pytest.fixture
def create_user_page(browser):
    return CreateUserPage(browser)

@pytest.fixture
def dashboard_page(browser):
    return DashboardPage(browser)

@pytest.fixture
def login_page(browser):
    return LoginPage(browser)

@pytest.fixture
def logged_in_user(login_page, user):
    login_page.login_with(user)

@pytest.fixture
def user(create_user_page):
    new_user = User()
    create_user_page.go()
    create_user_page.fill_user_form(new_user)
    create_user_page.submit_user_form()
    return new_user
