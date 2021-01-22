import time

class Account():
    def __init__(self):
        self.name = f"Account {time.time()}"
        self.type = "Credit Card"

class User():
    def __init__(self):
        self.name = f"John {time.time()} Doe"
        self.email = f"user-{time.time()}@nowhere.com"
        self.password = "1234567890"
