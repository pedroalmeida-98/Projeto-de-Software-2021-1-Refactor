# workers.py
import payments as payment


class Worker:
    def __init__(self, name, address, worker_id, syndicate, payment_handler):
        self.name = name
        self.address = address
        self.worker_id = worker_id
        self.syndicate = syndicate
        self.payment_handler = payment_handler

    def __str__(self):
        return "Worker name: {}\nAddress: {}\nType: {}\nWorkerID: {}\nPart of Syndicate: {}\n".format(
            self.name, self.address, type(self), self.worker_id, self.syndicate)

# getters and setters

    def set_name(self, new_name):
        self.name = new_name

    def set_address(self, new_address):
        self.address = new_address

    def set_syndicate(self, new_syndicate):
        self.syndicate = new_syndicate


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
        return self.syndicate_tax + self.get_service_taxes()


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
    def __init__(self, name, address, worker_id, syndicate, payment_handler, hr_rate, time_cards=list()):
        Worker.__init__(self, name, address, worker_id, syndicate, payment_handler)
        self.rate = hr_rate
        self.time_cards = time_cards

    def __str__(self):
        return "Worker name: {}\nAddress: {}\nType: {}\nWorkerID: {}\nHourly Rate: {}\nTime cards qty: {}\n" \
               "Part of syndicate: {}\n"\
            .format(self.name, self.address, type(self), self.worker_id, self.rate, len(self.time_cards),
                    self.syndicate)

    def punch(self, card):
        self.time_cards.append(card)

    def get_income(self):
        total = 0
        for card in self.time_cards:
            day_result = card.get_hours()
            if day_result <= 8:
                total += day_result*self.rate
            else:
                total += 8*self.rate + 1.5*self.rate*(day_result-8)

        return total


class Salaried(Worker):
    def __init__(self, name, address, worker_id, syndicate, payment_handler, salary):
        Worker.__init__(self, name, address, worker_id, syndicate, payment_handler)
        self.salary = salary

    def __str__(self):
        return "Worker name: {}\nAddress: {}\nType: {}\nWorkerID: {}\nSalary: {}\n" \
               "Part of syndicate: {}\n"\
            .format(self.name, self.address, type(self), self.worker_id, self.salary, self.syndicate)

    def get_income(self):
        return self.salary


class Commissioned(Worker):
    def __init__(self, name, address, worker_id, syndicate, payment_handler, salary, commission_rate,
                 sales=list()):
        Worker.__init__(self, name, address, worker_id, syndicate, payment_handler)
        self.salary = salary
        self.commission_rate = commission_rate
        self.sales = sales

    def __str__(self):
        return "Worker name: {}\nAddress: {}\nType: {}\nWorkerID: {}\nSalary: {}\nSales qty: {}\n" \
               "Part of Syndicate: {}"\
            .format(self.name, self.address, type(self), self.worker_id, self.salary, len(self.sales), self.syndicate)

    def sold(self, sale):
        self.sales.append(sale)

    def get_sales_value(self, target_date):
        total = 0
        for sale in self.sales:
            if sale.date <= target_date:
                total += sale.get_value()

        return total

    def get_income(self, target_date):
        commissions = self.get_sales_value(target_date)
        return self.salary + commissions
