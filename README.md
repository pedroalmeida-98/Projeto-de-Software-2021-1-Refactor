# Projeto-de-Software-2021-1-Refactor
This project's goal is to detect bad code smells and apply design patterns in order to correct them.

## Detected Code Smells and how I solved them
The following sections will show the code smells that were detected in the old version of the software and the solution 
implemented to solve each one.

### 1: Menu [Switch statement]
The old version od the payroll used a kind of switch statement in the operations' menu, as you can see in this code
snippet:

```python
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
```
### 1.1: Switch case solution
I've used the Command pattern and now the menu commands are executed from a list, as you can see in the snippets bellow:
```python
command_list = [cm.AddWorkerCommand(), cm.RemoveWorkerCommand(), cm.TimeCardCommand(), cm.SaleCardCommand(),
                cm.ServiceTaxCommand(), cm.EditWorkerCommand(), cm.RunPayrollCommand(), cm.PaymentCalendarCommand()]
payroll = pr.Payroll()
command = cm.Command()
menu = cm.MenuControl(command)
```
```python
while opt.upper() != "E":
    print("==============================================================\nWORKERS REPORT\n\n")
    payroll.workers_report()
    print("==============================================================\nSYNDICATE REPORT\n\n")
    payroll.syndicate_report()
    print(menu)
    opt = input()
    if opt == "E":
        break
    elif 0 < int(opt) <= 8:
        menu.set_command(command_list[int(opt)-1])
        menu.command_slot.execute(payroll)
    else:
        print("Insert a valid option!\n")
```
### 2: Payroll class is too big [Large Class]
The payroll class used to be the biggest class in this project. This make sense because it's the "core" of the project
but on the other hand this class had to deal with all the requests when it doesn't own the majority of the information
(directly).

### 2.1: Large Class solution

I've created a PaymentHandler Class which is responsible to keep track of the worker's payment data, along with the
list of payments. the edit functions of this type of data were moved to this class too [Move method] and now the list
of payments isn't part of worker class anymore, helping with smells detected in this class, which were Large Class and 
long parameter list[Move method and Move Parameter]. Now the payroll system only get the values from the workers and 
calculate the total of their payments, then pass the data to the PaymentHandler object contained into the Worker 
superclass.

### 3: Undo/Redo

My first attempt on the undo/redo function didn't work out, So I've used the Memento pattern with my command class 
acting as my Invoker object. The Memento class stores a Payroll object and the CareTaker class is responsible to store
these states and navigate into them with undo/redo functions.

### Minor fixes
* Removed "worker_type" field from worker's classes because it's unnecessary [Remove parameter]
* Removed all the getters related to worker's info in the Worker class because they aren't being used 
[Speculative Generality]
* Merged the search_worker_index() and search_worker_object into one unique function search_worker, 
since they perform the same steps and just have different returns [Duplicate Code]:

Before:      
```python
             
    def search_worker_index(self, worker_id):
        for targeted in self.workers:
            if targeted.worker_id == worker_id:
                return self.workers.index(targeted)

    def search_worker_object(self, worker_id):
        target = self.search_worker_index(worker_id)
        return self.workers[target]   
```
After:
```python
     def search_worker(self, worker_id):
        for targeted in self.workers:
            if targeted.worker_id == worker_id:
                return self.workers.index(targeted), targeted
```

* Did the same to the syndicate's members search-related functions