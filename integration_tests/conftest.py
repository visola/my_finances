import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .entities import User
from .pages import AccountsPage, CreateAccountPage, CreateUserPage, DashboardPage, LoginPage

@pytest.fixture(name='browser')
def fixture_browser():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.close()

@pytest.fixture(name='accounts_page')
def fixture_accounts_page(browser):
    return AccountsPage(browser)

@pytest.fixture(name='create_account_page')
def fixture_create_account_page(browser):
    return CreateAccountPage(browser)

@pytest.fixture(name='create_user_page')
def fixture_create_user_page(browser):
    return CreateUserPage(browser)

@pytest.fixture(name='dashboard_page')
def fixture_dashboard_page(browser):
    return DashboardPage(browser)

@pytest.fixture(name='login_page')
def fixture_login_page(browser):
    return LoginPage(browser)

@pytest.fixture(name='user')
def fixture_user(create_user_page):
    new_user = User()
    create_user_page.get()
    create_user_page.fill_user_form(new_user)
    create_user_page.submit_user_form()
    return new_user
