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
        return "Check delivered personally!\nDate: {}\nValue: {}\nAccount: {}\n"\
            .format(self.date, self.value, self.account)


class Deposit:
    def __init__(self, date, value, account):
        self.date = date
        self.value = value
        self. account = account

    def __str__(self):
        return "The money was deposited in worker's account!\nDate: {}\nValue: {}\nAccount: {}\n".\
            format(self.date, self.value, self.account)


class PaymentHandler:
    def __init__(self, base_payment, agenda, payments=list()):
        self.base_payment = base_payment
        self.payment_list = payments
        self.agenda = agenda

    def get_agenda(self):
        return self.agenda

    def set_agenda(self, new_agenda):
        self.agenda = new_agenda

    def get_payment_list(self):
        return self.payment_list

    def get_last_payment(self):
        payment = self.payment_list.pop()
        self.payment_list.append(payment)
        return payment

    def get_payment_data(self):
        return self.base_payment

    def set_payment_data(self, date, value, account, address):
        payment_type = input("insert new payment type: DEPOSIT, MAIL CHECK or HAND CHECK")
        new_payment = 0
        if payment_type == "DEPOSIT":
            new_payment = Deposit(date, value, account)
        if payment_type == "MAIL CHECK":
            new_payment = MailCheck(date, value, account, address)
        if payment_type == "HAND CHECK":
            new_payment = HandCheck(date, value, account)
        self.base_payment = new_payment

    def add_payment(self, value, date):
        base = self.get_payment_data()
        base.value = value
        base.date = date
        print(base)
        self.payment_list.append(base)
