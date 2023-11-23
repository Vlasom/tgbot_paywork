class User:
    def __init__(self, tg_id: int, username: str = None, fullname: str = None):
        self.tg_id = tg_id
        self.username = username
        self.fullname = fullname
