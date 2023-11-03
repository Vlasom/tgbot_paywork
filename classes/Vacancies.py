class Vacancy:
    def __init__(self,
                 values: dict = None,
                 id: int = None,
                 text: str = None,
                 photo: bytes = None):
        self.photo = photo
        self.values: dict = values
        self.id: int = id
        self.text: str = text

        # if values and not id:
        #     self.id = values["id"]