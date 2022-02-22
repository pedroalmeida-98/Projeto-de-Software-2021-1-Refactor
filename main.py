import payroll as pr
import commands as cm
import memento as meme

command_list = [cm.AddWorkerCommand(), cm.RemoveWorkerCommand(), cm.TimeCardCommand(), cm.SaleCardCommand(),
                cm.ServiceTaxCommand(), cm.EditWorkerCommand(), cm.RunPayrollCommand(), cm.PaymentCalendarCommand()]
payroll = pr.Payroll()
command = cm.Command()
menu = cm.MenuControl(command)
memory = meme.CareTaker()
memory.add_state(payroll)
opt = "start"

while opt.upper() != "E":

    print("==============================================================\nWORKERS REPORT\n")
    payroll.workers_report()
    print("==============================================================\nSYNDICATE REPORT\n")
    payroll.syndicate_report()
    print(payroll)
    print(menu)
    print(memory)
    print("You can also UNDO or REDO the last operations. Insert your option:")
    opt = input()
    if opt == "E":
        break
    elif opt == "UNDO":
        payroll = memory.undo()
    elif opt == "REDO":
        payroll = memory.redo()
    elif 0 < int(opt) <= 8:
        menu.set_command(command_list[int(opt)-1])
        menu.command_slot.execute(payroll)
        memory.add_state(payroll)
    else:
        print("Invalid Command!\n")

    input("press enter to continue")
