

def premute(num, input_list):
    if num == 1:
        return input_list
    else:
        return [ i+j 
                for i in input_list 
                for j in premute(num-1, input_list)
                ]

def premutation(input_list, start, end):
    if start == end:
        print(input_list)
    else:
        for i in premutation(input_list, start, end-1):
            i[0], i[1] = i[1], i[0]
        

def main():
    print(premute(1, ['a', 'b', 'c']))
    print(premute(2, ['a', 'b', 'c']))
    print(premute(3, ['a', 'b', 'c']))

main()