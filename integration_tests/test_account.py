from .fixtures import *

class TestAccount():
    def test_create_account(self, accounts_page, logged_in_user):
        accounts_page.go()
