import payroll as pr
import datetime as dt

menu = "PAYROLL\n\n\nMenu:\n1-Add a worker\n2-Remove a Worker\n3- Launch Time Card\n4- Insert sale\n" \
       "5- Add service tax\n6- Edit worker info\n7- Run the payroll\n8- Payment calendars\n\n E-Exit\n"
payroll = pr.Payroll()
opt = "start"

while opt.upper() != "E":
    print(menu)
    print("==============================================================\nWORKERS REPORT\n\n")
    payroll.workers_report()
    print("==============================================================\nSYNDICATE REPORT\n\n")
    payroll.syndicate_report()
    opt = input("\n\nInsert your desired operation: ")
    if opt == "1":
        name = input("insert name: ")
        address = input("insert address: ")
        w_type = input("insert worker type(HOURLY, SALARIED, COMMISSIONED): ")
        w_type = w_type.upper()
        syndicate = input("The worker is a member of the syndicate?(Y/N): ")
        syndicate = syndicate.upper()
        pay_method = input("Insert payment method (DEPOSIT, MAIL CHECK, HAND CHECK): ")
        pay_method = pay_method.upper()
        payroll.add(name, address, w_type, syndicate, pay_method)
    elif opt == "2":
        target = input("Insert worker id: ")
        payroll.remove_worker(int(target))
    elif opt == "3":
        target = input("Insert worker id: ")
        date_str = input("Insert date(DD/MM/YY): ")
        start_time_str = input("Starting at: ")
        end_time_str = input("Ending at: ")

        date = dt.datetime.strptime(date_str, '%d/%m/%y').date()
        s_time = dt.datetime.strptime(start_time_str, '%H:%M').time()
        e_time = dt.datetime.strptime(end_time_str, '%H:%M').time()
        payroll.launch_time_card(int(target), s_time, e_time, date)
    elif opt == "4":

        target = input("Insert worker id: ")
        date_str = input("Insert date(DD/MM/YY): ")
        value = input("Insert sale value: ")

        date = dt.datetime.strptime(date_str, '%d/%m/%y').date()
        payroll.launch_sale_result(int(target), date, value)
    elif opt == "5":
        tax = input("Insert the service tax value: ")
        target = input("Insert worker id: ")
        payroll.launch_service_tax(int(target), float(tax))
    elif opt == "6":
        target = input("Insert Worker ID: ")
        payroll.edit_worker_info(int(target))
    elif opt == "7":
        target_date_str = input("Insert target date: ")
        target_date = dt.datetime.strptime(target_date_str, '%d/%m/%y')
    elif opt == "8":
        payroll.payment_agendas()
    elif opt == "E":
        print("Bye!")
        break
    else:
        print("Insert a valid option!\n")

    input("press enter to continue")
