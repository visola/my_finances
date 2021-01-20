from .entities import Account
from .fixtures import *

class TestAccount():
    def test_create_account(self, accounts_page, create_account_page, logged_in_user):
        create_account_page.go()

        account = Account()
        create_account_page.fill_form(account)
        create_account_page.submit_form()

        assert accounts_page.is_displayed(account.name)
