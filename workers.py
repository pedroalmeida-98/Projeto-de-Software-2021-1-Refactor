# workers.py
import payments as payment


class Worker:
    def __init__(self, name, address, worker_type, worker_id, syndicate, payment_type, payments=list()):
        self.name = name
        self.address = address
        self.worker_type = worker_type
        self.worker_id = worker_id
        self.syndicate = syndicate
        self.payment_type = payment_type
        self.payments = payments
        self.payments_calendar = "MONTHLY"

    def __str__(self):
        return "Worker name: {}\nAddress: {}\nType: {}\nWorkerID: {}\nPart of Syndicate: {}\nPayment type: {]".format(
            self.name, self.address, self.worker_type, self.worker_id, self.syndicate, self.payment_type)

# getters and setters

    def get_name(self):
        return self.name

    def set_name(self, new_name):
        self.name = new_name

    def get_address(self):
        return self.address

    def set_address(self, new_address):
        self.address = new_address

    def get_syndicate(self):
        return self.syndicate

    def set_syndicate(self, new_syndicate):
        self.syndicate = new_syndicate

    def get_payment_type(self):
        return self.payment_type

    def set_payment_type(self, new_payment_type):
        self.payment_type = new_payment_type

    def get_payments_calendar(self):
        return self.payments_calendar

    def set_payments_calendar(self, new_payments_calendar):
        self.payments_calendar = new_payments_calendar

    def add_payment(self, new_payment):
        self.payments.append(new_payment)

    def get_payment_data(self):
        return self.payments[0]

    def get_payment_list(self):
        return self.payments

    def set_payment_list(self, new_payments=list()):
        self.payments = new_payments

    def set_payment_data(self, date):
        payment_data = 0
        account = input("Insert Worker's bank account")

        if self.payment_type == "DEPOSIT":
            payment_data = payment.Deposit(date, 0, account)
        elif self.payment_type == "MAIL CHECK":
            payment_data = payment.MailCheck(date, 0, account, self.address)
        elif self.payment_type == "HAND CHECK":
            payment_data = payment.HandCheck(date, 0, account)
        self.add_payment(payment_data)

    def edit_payment_data(self):
        new_payment_data = 0
        opt = input("insert the new payment method: ")
        opt = opt.upper()
        old_payment_data = self.get_payment_data()
        if opt == "DEPOSIT":
            new_payment_data = payment.Deposit(old_payment_data.date, 0, old_payment_data.account)
        elif opt == "HAND CHECK":
            new_payment_data = payment.HandCheck(old_payment_data.date, 0, old_payment_data.account)
        elif opt == "MAIL CHECK":
            new_payment_data = payment.MailCheck(old_payment_data.date, 0, old_payment_data.account, self.address)
        self.payment_type = opt
        self.payments[0] = new_payment_data

    def get_last_payment(self):
        return self.payments[len(self.payments)-1]


# Syndicate
class Syndicate:
    def __init__(self, worker, syndicate_id, syndicate_tax, service_taxes=list()):
        self.worker = worker
        self.syndicate_id = syndicate_id
        self.syndicate_tax = syndicate_tax
        self.service_taxes = service_taxes

    def __str__(self):
        return "{}\nSyndicate ID: {}\nSyndicate tax: {}\nService taxes: {}\n"\
            .format(self.worker, self.syndicate_id, self.syndicate_tax, self.service_taxes)

    def add_service_tax(self, new_service_tax):
        self.service_taxes.append(new_service_tax)

    def set_syndicate_tax(self, new_syndicate_tax):
        self.syndicate_tax = new_syndicate_tax

    def get_syndicate_tax(self):
        return self.syndicate_tax

    def get_service_taxes(self):
        total = 0
        for tax in self.service_taxes:
            total += tax
            self.service_taxes.remove(tax)
        return total

    def charge(self):
        return self.syndicate_tax() + self.get_service_taxes()


# Card types #
class TimeCard:
    def __init__(self, start, end, date):
        self.start = start
        self.end = end
        self.date = date

    def get_hours(self):
        result = self.end - self.start
        return result.hour


class SaleCard:
    def __init__(self, date, value):
        self.date = date
        self.value = value

    def get_value(self):
        return self.value


# Worker Types #
class Hourly(Worker):
    def __init__(self, name, address, worker_type, worker_id, syndicate, payment_type, hr_rate, time_cards=list()):
        Worker.__init__(self, name, address, worker_type, worker_id, syndicate, payment_type)
        self.rate = hr_rate
        self.time_cards = time_cards

    def __str__(self):
        return "Worker name: {}\nAddress: {}\nType: {}\nWorkerID: {}\nHourly Rate: {}\nTime cards qty: {}\n" \
               "Payment type: {}\nPart of syndicate: {}\n"\
            .format(self.name, self.address, self.worker_type, self.worker_id, self.rate, len(self.time_cards),
                    self.payment_type, self.syndicate)

    def punch(self, card):
        self.time_cards.append(card)

    def get_rates(self):
        total = 0
        for card in self.time_cards:
            day_result = card.get_hours()
            if day_result <= 8:
                total += day_result*self.rate
            else:
                total += 8*self.rate + 1.5*self.rate*(day_result-8)

        return total


class Salaried(Worker):
    def __init__(self, name, address, worker_type, worker_id, syndicate, payment_type, salary):
        Worker.__init__(self, name, address, worker_type, worker_id, syndicate, payment_type)
        self.salary = salary

    def __str__(self):
        return "Worker name: {}\nAddress: {}\nType: {}\nWorkerID: {}\nSalary: {}\n" \
               "Payment type: {}\nPart of syndicate: {}\n"\
            .format(self.name, self.address, self.worker_type, self.worker_id, self.salary, self.payment_type,
                    self.syndicate)

    def get_salary(self):
        return self.salary


class Commissioned(Worker):
    def __init__(self, name, address, worker_type, worker_id, syndicate, payment_type, salary, commission_rate,
                 sales=list()):
        Worker.__init__(self, name, address, worker_type, worker_id, syndicate, payment_type)
        self.salary = salary
        self.commission_rate = commission_rate
        self.sales = sales

    def __str__(self):
        return "Worker name: {}\nAddress: {}\nType: {}\nWorkerID: {}\nSalary: {}\nSales qty: {}\n" \
               "Payment type: {}\nPart of Syndicate: {}"\
            .format(self.name, self.address, self.worker_type, self.worker_id, self.salary, len(self.sales),
                    self.payment_type, self.syndicate)

    def sold(self, sale):
        self.sales.append(sale)

    def get_sales_value(self, target_date):
        total = 0
        for sale in self.sales:
            if sale.date <= target_date:
                total += sale.get_value()

        return total

    def get_revenue(self, target_date):
        commissions = self.get_sales_value(target_date)
        return self.salary + commissions
