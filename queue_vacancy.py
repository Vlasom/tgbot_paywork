
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
        self.queue.extend(vacancy)
        return True


class QueueIter:
    def __init__(self, lst: list, user_id: int):
        self.lst: list = lst
        self.user_id = user_id

    def is_in(self, obj: object):
        return True if obj in self.lst else False

    def content(self):
        return self.lst

    def insert(self, insrt: list | object):
        self.lst.extend(insrt if type(insrt) is list else [insrt])

    def next(self):
        if self.lst:
            result = self.lst[0]
            self.lst.pop(0)
            return result




