# payroll.py
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
    def search_worker_index(self, worker_id):
        for targeted in self.workers:
            if targeted.worker_id == worker_id:
                return self.workers.index(targeted)

    def search_worker_object(self, worker_id):
        target = self.search_worker_index(worker_id)
        return self.workers[target]

    def search_syndicate_index(self, worker):
        for targeted in self.syndicate_members:
            if targeted.worker == worker:
                return self.syndicate_members.index(targeted)

    def search_syndicate_object(self, worker):
        target = self.search_syndicate_index(worker)
        return self.syndicate_members[target]

# Payroll functions
    def add(self, name, address, worker_type, syndicate, pay_method):
        worker_id = self.worker_count + 1
        self.worker_count += 1
        new_worker = 0

        if worker_type == "HOURLY":
            rate = input("Insert the hourly rate: ")
            new_worker = wk.Hourly(name, address, worker_type, worker_id, syndicate, pay_method, float(rate))
            new_worker.set_payments_calendar("WEEKLY 1 FRIDAY")
        elif worker_type == "SALARIED":
            sal = input("Insert the worker's salary: ")
            new_worker = wk.Salaried(name, address, worker_type, worker_id, syndicate, pay_method, float(sal))
            new_worker.set_payments_calendar("MONTHLY 1")
        elif worker_type == "COMMISSIONED":
            sal = input("Insert worker's salary: ")
            comm = input("Insert worker's commission: ")
            new_worker = wk.Commissioned(name, address, worker_type, worker_id, syndicate, pay_method, float(sal),
                                         float(comm))
            new_worker.set_payments_calendar("WEEKLY 2 FRIDAY")

        if syndicate == "Y":
            syndicate_id = self.syndicate_member_count + 1
            self.syndicate_member_count += 1
            syndicate_tax = 50
            new_syndicate_member = wk.Syndicate(new_worker, syndicate_id, syndicate_tax)
            self.syndicate_members.append(new_syndicate_member)
        new_worker.set_payment_data(self.today)
        self.workers.append(new_worker)

    def remove_worker(self, worker_id):
        target = self.search_worker_object(worker_id)
        self.workers.remove(target)

    def launch_time_card(self, worker_id, s_time, e_time, date):
        card = wk.TimeCard(s_time, e_time, date)
        position = self.search_worker_index(worker_id)
        target = self.search_worker_object(worker_id)
        if target.worker_type == "HOURLY":
            target.punch(card)
            self.workers[position] = target
        else:
            print("This isn't an hourly worker!\n")

    def launch_sale_result(self, worker_id, date, val):
        sale = wk.SaleCard(date, val)
        position = self.search_worker_index(worker_id)
        target = self.search_worker_object(worker_id)
        if target.worker_type == "COMMISSIONED":
            target.sold(sale)
            self.workers[position] = target
        else:
            print("This isn't an commissioned worker!\n")

    def launch_service_tax(self, worker_id, service_tax):
        target = self.search_worker_object(worker_id)
        if target.syndicate == "Y":
            syndicate_position = self.search_syndicate_index(target)
            syndicate_object = self.search_syndicate_object(target)
            syndicate_object.add_service_tax(service_tax)
            self.syndicate_members[syndicate_position] = syndicate_object
        else:
            print("This isn't a syndicate member!\n")

    def edit_worker_info(self, target):
        worker_position = self.search_worker_index(target)
        worker_data = self.search_worker_object(target)
        flag = 0
        syndicate_index = 0
        syndicate_object = 0
        if worker_data.syndicate == "Y":
            syndicate_index = self.search_syndicate_index(worker_data)
            syndicate_object = self.search_syndicate_object(worker_data)
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
                new_worker_info = wk.Hourly(worker_data.name, worker_data.address, new_worker_type,
                                            worker_data.worker_id, worker_data.syndicate, worker_data.payment_type,
                                            rate)
            elif new_worker_type == "SALARIED":
                sal = input("Insert the worker's salary: ")
                new_worker_info = wk.Salaried(worker_data.name, worker_data.address, new_worker_type,
                                              worker_data.worker_id, worker_data.syndicate, worker_data.payment_type,
                                              sal)
            elif new_worker_type == "COMMISSIONED":
                sal = input("Insert worker's salary: ")
                comm = input("Insert worker's commission: ")
                new_worker_info = wk.Commissioned(worker_data.name, worker_data.address, new_worker_type,
                                                  worker_data.worker_id, worker_data.syndicate,
                                                  worker_data.payment_type, sal, comm)

            new_worker_info.set_payment_list(worker_data.get_payment_list())
            self.workers[worker_position] = new_worker_info
            if flag:
                syndicate_object.worker = new_worker_info
                self.syndicate_members[syndicate_index] = syndicate_object
        elif opt == "4":
            worker_data.edit_payment_data()
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
                syndicate_object = self.search_syndicate_object(worker_data)
                self.syndicate_members.remove(syndicate_object)
                worker_data.syndicate = "N"

            self.workers[worker_position] = worker_data
        elif opt == "6":
            new_syndicate_tax = input("Insert new syndicate tax: ")
            syndicate_index = self.search_syndicate_index(worker_data)
            syndicate_obj = self.search_syndicate_object(syndicate_index)
            syndicate_obj.set_syndicate_tax(new_syndicate_tax)
            self.syndicate_members[syndicate_index] = syndicate_obj

    def pay(self, worker):
        syndicate_taxes = 0
        income = 0
        new_payment = 0
        if worker.syndicate == "Y":
            syndicate_index = self.search_syndicate_index(worker)
            syndicate_obj = self.search_syndicate_object(worker)
            syndicate_taxes = syndicate_obj.charge()
            self.syndicate_members[syndicate_index] = syndicate_obj

        if worker.worker_type == "HOURLY":
            income = worker.get_rates()
        elif worker.worker_type == "SALARIED":
            income = worker.get_salary()
        elif worker.worker_type == "COMMISSIONED":
            income = worker.get_revenue(self.today)

        payment_data = worker.get_payment_data()
        total = income - syndicate_taxes

        if type(payment_data) == payments.MailCheck:
            new_payment = payments.MailCheck(self.today, total, payment_data.account, payment_data.address)
        elif type(payment_data) == payments.Deposit:
            new_payment = payments.Deposit(self.today, total, payment_data.account)
        elif type(payment_data) == payments.HandCheck:
            new_payment = payments.HandCheck(self.today, total, payment_data.account)
        print(new_payment)
        worker.add_payment(new_payment)
        return worker

    def run(self, target_date):
        while self.today <= target_date:
            for worker in self.workers:
                calendar = worker.payments_calendar.split()
                if calendar[0] == "WEEKLY":
                    if self.today - worker.get_last_payment() == 7*int(calendar[1]):
                        worker_position = self.search_worker_index(worker.worker_id)
                        worker = self.pay(worker)

                        self.workers[worker_position] = worker
                elif calendar[0] == "MONTHLY":
                    if self.today.day == int(calendar[1]):
                        worker_position = self.search_worker_index(worker.worker_id)
                        worker = self.pay(worker)
                        self.workers[worker_position] = worker

    def payment_agendas(self):
        print("PAYMENT CALENDAR MENU\n\n1- Add payment calendar\n2- Set work calendar to a specific worker\n\nE- Exit")
        opt = "start"
        while opt != "E":
            opt = input("Choose your option: ")
            if opt == "1":
                new_calendar = input("The calendar must be written like this:\n"
                                     "WEEKLY N DAYOFTHEWEEK(for weekly calendars)\nMONTHLY D(for monthly calendars)\n"
                                     "\nN= number of weeks\nD= day of the month\n\nInsert calendar string: ")
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
                worker_position = self.search_worker_index(int(worker_id))
                worker_object = self.search_worker_object(int(worker_id))
                worker_object.set_payments_calendar(self.payment_calendars[int(calendar_opt)-1])
                self.workers[worker_position] = worker_object

            else:
                print("Please choose a valid operation!\n")
            input("Press enter to continue")
