import time

from .fixtures import *
from .entities import User

class TestUser:
    def test_create_user(self, create_user_page, login_page):
        login_page.go()
        login_page.click_sign_up_link()
        
        user = User()
        create_user_page.fill_user_form(user)
        create_user_page.submit_user_form()

        assert login_page.is_displayed()

    def test_login(self, dashboard_page, login_page, user):
        login_page.go()
        login_page.login_with(user)

        assert dashboard_page.is_displayed(user.name)
