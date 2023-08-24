
class QueueVacancy:
    def __init__(self, user_id, expire_date, *vacancys):
        self.user_id = user_id
        self.expire_date = expire_date
        self.queue: list = list(vacancys)

    def get_next(self):
        if not self.queue:
            return "Вакансии закончились"
        else:
            vac = self.queue[-1]
        self.queue.pop(-1)
        return str(vac)

    def insert(self, vacancy):
        self.queue.append(vacancy)
        return True
