class Sender:
    def __init__(self):
        self.number_of_calls = 0

    def send(self, message):
        self.number_of_calls += 1


class SMSSender(Sender):  # Пусть будет какая-нибудь dummy реализация
    def send(self, message):
        print('SMS is sended')
        super().send(message)


class EmailSender(Sender):
    def send(self, message):
        print('Email is sended')
        super().send(message)
