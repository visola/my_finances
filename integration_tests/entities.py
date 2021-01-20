import time

class User():
    def __init__(self):
        self.name = f"John {time.time()} Doe"
        self.email = f"user-{time.time()}@nowhere.com"
        self.password = "1234567890"
