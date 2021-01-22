from .entities import Account

class TestAccount():
    def test_create_account(self, accounts_page, create_account_page, login_page, user):
        login_page.login_with(user)

        create_account_page.get()

        account = Account()
        create_account_page.fill_form(account)
        create_account_page.submit_form()

        assert accounts_page.is_displayed(account.name)
