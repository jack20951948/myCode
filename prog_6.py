account = ['Chase Checking', 'Citi Saving', 'WellsFargo Saving'] 
balance = [1000, 10000, 999.99]

def print_account(acc, bal):
    print("My Bank Account Summary =========")
    for index, (a, b) in enumerate(zip(account, balance)):
        print("  %2d %-20s %10.2f" %(index, a, b))
    print()

def add_account(acc, bal):
    print("Opening a new account. Enter new account name:", acc)
    print("Enter opening deposit:", bal)
    if acc in account:
        print(" ***\tAn account with the name {} is on the list.".format(acc))
    else:
        account.append(acc)
        balance.append(bal)
        print(" ***\tAdding account {} with {}".format(acc, bal))
    print()
    print()
    print_account(account, balance)

def deposit(acc, bal):
    print("Deposit money. Enter the account name:", acc)
    print("Enter the amount:", bal)
    if acc in account:
        balance[account.index(acc)] += bal
        print(" ***\t{} new balance =".format(acc), balance[account.index(acc)])
    else:
        print(" ***\t{} not found.".format(acc))
    print()
    print()
    print_account(account, balance)

def withdraw(acc, bal):
    print("Withdraw money. Enter the account name:", acc)
    print("Enter the amount:", bal)
    if acc not in account:
        print(" ***\t{} not found.".format(acc))
    elif bal > balance[account.index(acc)]:
        print(" ***\tInsufficient fund")
    else:
        balance[account.index(acc)] -= bal
        print(" ***\t{} new balance =".format(acc), balance[account.index(acc)])
    print()
    print()
    print_account(account, balance)

print_account(account, balance)
add_account("Chase CD1", 200)
add_account("Chase CD1", 300)
add_account("Chase CD2", 900)
withdraw("Chase Saving", 100)
withdraw("Chase Checking", 2000)
withdraw("Chase Checking", 99)
deposit("Chase Saving", 300)
deposit("Chase Checking", 1400)
deposit("Citi Saving", 999)