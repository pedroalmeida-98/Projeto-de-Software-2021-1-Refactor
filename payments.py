# payments.py
class MailCheck:
    def __init__(self, date, value, account, address):
        self.date = date
        self.value = value
        self.address = address
        self.account = account

    def __str__(self):
        return "Check sent by mail!\nDate: {}\nValue: {}\nAccount: {}\nAddress: {}\n"\
            .format(self.date, self.value, self.account, self.address)


class HandCheck:
    def __init__(self, date, value, account):
        self.date = date
        self.value = value
        self.account = account

    def __str__(self):
        return "Check delivered personally!\nDate: {}\nValue: {}\nAccount: {}\n".format(self.date, self.value, self.account)


class Deposit:
    def __init__(self, date, value, account):
        self.date = date
        self.value = value
        self. account = account

    def __str__(self):
        return "The money was deposited in worker's account!\nDate: {}\nValue: {}\nAccount: {}\n".\
            format(self.date, self.value, self.account)
