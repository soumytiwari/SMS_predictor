
class Main():

    def __init__(self) -> None:
        self.command_handlers = {
            'TXMS'  :   self.txms,
            'STAT'  :   self.stat,
            'ANIN'  :   self.anin,
            'CDSC'  :   self.cdsc,
            'TXNW'  :   self.txnw,
            'TXNM'  :   self.txnm,
            'TXNY'  :   self.txny,
            'MEXP'  :   self.mexp,
            'QUIT'  :   self.quit
        }

    # show them their name and associated bank names and connected email and their address
    def basic_user_info(self):
        print('basic_user_info')
        pass

    # show them their current balance, account type along with the earlier info
    def basic_bank_info(self):
        print('basic_bank_info')
        pass

    # show them menu of what they want
    def menu(self):
        menu = """

====================================    MENU    ====================================


Description:
Press the follwoing sequence of number mentioned for the respective query


TXMS                      See your latest transaction message
STAT                      See your stats and features
ANIN                      Check your annual income
CDSC                      Check your credit score
TXNW                      Check your transactions of any week
TXNM                      Check your transactions of any month
TXNY                      Check your transactions of any year
MEXP                      Check your maximum expenditure data
EXPY                      Check your yearly expenditure
SAPY                      Check your savings per year
EXPM                      Check your expensive months
FAVB                      Check your most used bank
QUIT                      To Quit
"""
        print(menu)
        print("\nMenu Sent", 'success')

    def handle_cmds(self, cmd:str) -> str:
        try:
            self.cmd = cmd[:4]
        except:
            self.cmd = None
        return cmd

    # take input of what they want option
    def op_impl(self):
        while True:
            try:
                cmd = input("\nEnter your desired query >> ").upper()
                cmd = self.handle_cmds(cmd)
                if cmd:
                    if cmd in self.command_handlers:
                        self.command_handlers[cmd]()
                    else:
                        print('\nInvalid command! Please enter a valid command.')
                    
            except KeyboardInterrupt:
                print('\nKey Board interrupted, closing conection..')
                break



    # implement that operation
    def txms(self):
        print('txms')
        pass

    def stat(self):
        print('stat')
        pass

    def anin(self):
        print('anin')
        pass

    def cdsc(self):
        print('cdsc')
        pass

    def txnw(self):
        print('txnw')
        pass

    def txnm(self):
        print('txnm')
        pass

    def txny(self):
        print('txny')
        pass
    
    def mexp(self):
        print('mexp')
        pass

    def quit(self):
        print('\n221 Goodbye. Exiting...')
        exit()



if __name__ == "__main__":
    user_input_num = int(input("\nEnter your mobile number connected to your account whose query you want to know >> "))
    obj = Main()
    obj.basic_user_info()
    user_input_bank = input("\nEnter your bank name whose query you want associated >> ")
    obj.basic_bank_info()
    obj.menu()
    # take input of what they want option
    obj.op_impl()


