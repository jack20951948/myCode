def format_string(data):
    li_data = data.split("/")
    if int(li_data[2]) > 21:
        return "19" + li_data[2] + "-" + li_data[0] + "-" + li_data[1]
    else:
        return "20" + li_data[2] + "-" + li_data[0] + "-" + li_data[1]

def format_Date(data):
    for i in [2,4,5]:
        data[i] = format_string(data[i])
    return data

def build_table():
    data = []
    while True:
        rawData = input("Please enter a record:")
        if rawData == '':
            return data
        splitData = rawData.split("$")
        try:
            formatedData = format_Date(splitData)
        except:
            print("Input error! Please enter again!")
        else:
            data.append(tuple(map(str, formatedData)))

def print_table(_table):
    print("%-10s %-10s %-10s %-20s %-10s %-10s " %("Last Name", "First Name", "DoB", "Vaccine Product", "1st V-Date", "2nd V-Date"))
    for i in _table:
        print("%-10s %-10s %-10s %-20s %-10s %-10s " %i)
    print()

def main():
    table = build_table()
    print_table(table)
    table.sort(key=lambda x:x[5])
    print_table(table)

main()