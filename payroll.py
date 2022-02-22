# payroll.py
import datetime

import workers as wk
import datetime as dt
import payments


class Payroll:
    def __init__(self, workers=list(), syndicate_members=list()):
        self.workers = workers
        self.syndicate_members = syndicate_members
        self.worker_count = 0
        self.syndicate_member_count = 0
        self.today = dt.date.today()
        self.payment_calendars = ["WEEKLY 1 FRIDAY", "MONTHLY 1", "WEEKLY 2 FRIDAY"]

    def __str__(self):
        return "number of workers: {}\nnumber of syndicate members: {}\n".format(len(self.workers),
                                                                                 len(self.syndicate_members))

    def workers_report(self):
        size = len(self.workers)
        if size == 0:
            print("there are no workers in the system yet!")
        else:
            for worker in self.workers:
                print(worker)

    def syndicate_report(self):
        size = len(self.syndicate_members)
        if size == 0:
            print("there are no workers in the system yet!")
        else:
            for worker in self.syndicate_members:
                print(worker)

    # Search functions
    def search_worker(self, worker_id):
        for targeted in self.workers:
            if targeted.worker_id == worker_id:
                return self.workers.index(targeted), targeted

    def search_syndicate_member(self, worker):
        for targeted in self.syndicate_members:
            if targeted.worker == worker:
                return self.syndicate_members.index(targeted), targeted

# Payroll functions
    def add(self, name, address, worker_type, syndicate, pay_method):
        worker_id = self.worker_count + 1
        self.worker_count += 1
        new_worker = 0
        new_payment = 0
        account = input("Insert worker's account: ")
        if pay_method == "DEPOSIT":
            new_payment = payments.Deposit(self.today, 0, account)
        if pay_method == "MAIL CHECK":
            new_payment = payments.MailCheck(self.today, 0, account, address)
        if pay_method == "HAND CHECK":
            new_payment = payments.HandCheck(self.today, 0, account)
        if worker_type == "HOURLY":
            rate = input("Insert the hourly rate: ")

            pay_handler = payments.PaymentHandler(new_payment, self.payment_calendars[0])
            new_worker = wk.Hourly(name, address, worker_id, syndicate, pay_handler, float(rate))

        elif worker_type == "SALARIED":
            sal = input("Insert the worker's salary: ")
            pay_handler = payments.PaymentHandler(new_payment, self.payment_calendars[1])
            new_worker = wk.Salaried(name, address, worker_id, syndicate, pay_handler, float(sal))
        elif worker_type == "COMMISSIONED":
            sal = input("Insert worker's salary: ")
            comm = input("Insert worker's commission: ")
            pay_handler = payments.PaymentHandler(new_payment, self.payment_calendars[2])
            new_worker = wk.Commissioned(name, address, worker_id, syndicate, pay_handler, float(sal),
                                         float(comm))

        if syndicate == "Y":
            syndicate_id = self.syndicate_member_count + 1
            self.syndicate_member_count += 1
            syndicate_tax = 50
            new_syndicate_member = wk.Syndicate(new_worker, syndicate_id, syndicate_tax)
            self.syndicate_members.append(new_syndicate_member)
        self.workers.append(new_worker)

    def remove_worker(self, worker_id):
        index, target = self.search_worker(worker_id)
        self.workers.remove(target)

    def launch_time_card(self, worker_id, s_time, e_time, date):
        card = wk.TimeCard(s_time, e_time, date)
        position, target = self.search_worker(worker_id)

        if type(target) == wk.Hourly:
            target.punch(card)
            self.workers[position] = target
        else:
            print("This isn't an hourly worker!\n")

    def launch_sale_result(self, worker_id, date, val):
        sale = wk.SaleCard(date, val)
        position, target = self.search_worker(worker_id)
        if type(target) == wk.Commissioned:
            target.sold(sale)
            self.workers[position] = target
        else:
            print("This isn't an commissioned worker!\n")

    def launch_service_tax(self, worker_id, service_tax):
        position, target = self.search_worker(worker_id)
        if target.syndicate == "Y":
            syndicate_position, syndicate_object = self.search_syndicate_member(target)
            syndicate_object.add_service_tax(service_tax)
            self.syndicate_members[syndicate_position] = syndicate_object
        else:
            print("This isn't a syndicate member!\n")

    def edit_worker_info(self, target):
        worker_position, worker_data = self.search_worker(target)
        flag = 0
        syndicate_index = 0
        syndicate_object = 0
        if worker_data.syndicate == "Y":
            syndicate_index, syndicate_object = self.search_syndicate_member(worker_data)
            flag = 1

        opt = input("What info do you want to edit?\n\n1- Name\n2- Address\n3- Type\n4- Payment method\n5- Syndicate"
                    "\n6- Syndicate tax\n")
        if opt == "1":
            new_name = input("Insert new name: ")
            worker_data.set_name(new_name)

            self.workers[worker_position] = worker_data
            if flag:
                syndicate_object.worker = worker_data
                self.syndicate_members[syndicate_index] = syndicate_object

        elif opt == "2":
            new_address = input("Insert new address: ")
            worker_data.set_address(new_address)
            self.workers[worker_position] = worker_data
            if flag:
                syndicate_object.worker = worker_data
                self.syndicate_members[syndicate_index] = syndicate_object
        elif opt == "3":
            new_worker_type = input("Insert new worker type: ")
            new_worker_info = 0

            if new_worker_type == "HOURLY":
                rate = input("Insert the hourly rate: ")
                new_worker_info = wk.Hourly(worker_data.name, worker_data.address, worker_data.worker_id,
                                            worker_data.syndicate, worker_data.payment_handler, rate)
            elif new_worker_type == "SALARIED":
                sal = input("Insert the worker's salary: ")
                new_worker_info = wk.Salaried(worker_data.name, worker_data.address, worker_data.worker_id,
                                              worker_data.syndicate, worker_data.payment_handler, sal)
            elif new_worker_type == "COMMISSIONED":
                sal = input("Insert worker's salary: ")
                comm = input("Insert worker's commission: ")
                new_worker_info = wk.Commissioned(worker_data.name, worker_data.address, worker_data.worker_id,
                                                  worker_data.syndicate, worker_data.payment_handler, sal, comm)

            self.workers[worker_position] = new_worker_info
            if flag:
                syndicate_object.worker = new_worker_info
                self.syndicate_members[syndicate_index] = syndicate_object
        elif opt == "4":
            old_data = worker_data.payment_handler.get_payment_data()
            worker_data.payment_handler.set_payment_data(old_data.date, 0, old_data.account, worker_data.address)
            self.workers[worker_position] = worker_data
            if flag:
                syndicate_object.worker = worker_data
                self.syndicate_members[syndicate_index] = syndicate_object
        elif opt == "5":
            old_status = worker_data.syndicate
            if old_status == "N":
                print("Current syndicate status: N\nAdding worker to the syndicate")
                syndicate_id = self.syndicate_member_count + 1
                self.syndicate_member_count += 1
                syndicate_tax = 50
                worker_data.syndicate = "Y"
                new_syndicate_member = wk.Syndicate(worker_data, syndicate_id, syndicate_tax)
                self.syndicate_members.append(new_syndicate_member)
            elif old_status == "Y":
                print("Current syndicate status: Y\nRemoving worker to the syndicate")
                pos, syndicate_object = self.search_syndicate_member(worker_data)
                self.syndicate_members.remove(syndicate_object)
                worker_data.syndicate = "N"

            self.workers[worker_position] = worker_data
        elif opt == "6":
            new_syndicate_tax = input("Insert new syndicate tax: ")
            syndicate_index, syndicate_obj = self.search_syndicate_member(worker_data)
            syndicate_obj.set_syndicate_tax(new_syndicate_tax)
            self.syndicate_members[syndicate_index] = syndicate_obj

    def pay(self, worker):
        syndicate_taxes = 0
        new_payment = 0
        if worker.syndicate == "Y":
            syndicate_index, syndicate_obj = self.search_syndicate_member(worker)
            syndicate_taxes = syndicate_obj.charge()

        income = worker.get_income()
        total = income - syndicate_taxes
        worker.payment_handler.add_payment(self.today, total)
        return worker

    def run(self, target_date):
        while self.today <= target_date:
            print(self.today)
            print(":\n")
            for worker in self.workers:
                calendar = worker.payment_handler.agenda.split()
                if calendar[0] == "WEEKLY":
                    if self.today - worker.payment_handler.get_last_payment() == 7*int(calendar[1]):
                        worker_position, worker_obj = self.search_worker(worker.worker_id)
                        worker_obj = self.pay(worker_obj)
                        self.workers[worker_position] = worker_obj
                elif calendar[0] == "MONTHLY":
                    if self.today.day == int(calendar[1]):
                        worker_position, worker_obj = self.search_worker(worker.worker_id)
                        worker_obj = self.pay(worker_obj)
                        self.workers[worker_position] = worker_obj
            self.today += datetime.timedelta(days=1)
            print("\n")

    def payment_agendas(self):
        print("PAYMENT CALENDAR MENU\n\n1- Add payment calendar\n2- Set work calendar to a specific worker\n\nE- Exit")
        opt = "start"
        while opt != "E":
            opt = input("Choose your option: ")
            if opt == "1":
                new_calendar = input("The calendar must be written like this:\n"
                                     "WEEKLY N DAY-OF-THE-WEEK(for weekly calendars)\nMONTHLY D(for monthly calendars)"
                                     "\n\nN= number of weeks\nD= day of the month\n\nInsert calendar string: ")
                self.payment_calendars.append(new_calendar)
            elif opt == "2":
                menu_string = "{}- {}"
                worker_id = input("Please insert worker id: ")
                print("These are the available payment calendars:\n\n")
                n = 0
                while n < len(self.payment_calendars):
                    print(menu_string.format(n+1, self.payment_calendars[n]))
                    n += 1

                calendar_opt = input("Insert desired calendar option number: ")
                worker_position, worker_object = self.search_worker(int(worker_id))
                worker_object.set_payments_calendar(self.payment_calendars[int(calendar_opt)-1])
                self.workers[worker_position] = worker_object

            else:
                print("Please choose a valid operation!\n")
            input("Press enter to continue")
