import sys
import requests
import time

session = requests.Session()

def run_test():
    print("Load login page")
    get_login = session.get(f"http://{hostname}:{port}/login")
    get_login.raise_for_status()
    assert "New to us" in get_login.text

    print("Logging in")
    login_resp = session.post(
        f"http://{hostname}:{port}/login",
        data={'email': "viniciusisola@gmail.com", 'password': '1234'}
    )
    login_resp.raise_for_status()
    assert "Welcome" in login_resp.text

    print("Accounts screen")
    get_accounts = session.get(f"http://{hostname}:{port}/accounts")
    get_accounts.raise_for_status()
    assert "Accounts" in get_accounts.text

    print("Get new account screen")
    get_new_account = session.get(f"http://{hostname}:{port}/accounts/new")
    get_new_account.raise_for_status()
    assert "Name:" in get_new_account.text

    print("Create new account")
    account_name = f"Account-{time.time()}"
    create_new_account = session.post(
        f"http://{hostname}:{port}/accounts/save",
        data={"id": "", 'name': account_name, 'type': 'Checkings'}
    )
    create_new_account.raise_for_status()
    assert account_name in create_new_account.text

if __name__ == "__main__":
    hostname = sys.argv[1]
    port = sys.argv[2]
    print(f"Starting test at {hostname}:{port}")
    run_test()
