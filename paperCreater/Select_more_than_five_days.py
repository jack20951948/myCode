import pandas as pd 
import numpy as np 

if __name__ == '__main__':
    ### Parameters:
    #Result = pd.read_csv('test.csv')  
    Result = pd.read_csv('paperCreater\\final_result\\final_result.csv')  

    ### drop null from column['STARTDATE', 'ENDDATE']:
    Result_drop_null_date = Result.dropna(subset=['STARTDATE', 'ENDDATE'], how='any')

    ### set dataType to time frame:
    Result_drop_null_date['STARTDATE'] = pd.to_datetime(Result_drop_null_date['STARTDATE'])
    Result_drop_null_date['ENDDATE'] = pd.to_datetime(Result_drop_null_date['ENDDATE'])


    print('\n========= Data dropped =========\n')
    print(Result_drop_null_date)

    print('\n========= Data Info =========\n')
    print(Result_drop_null_date.info())
    
    print('\n========= Day period =========\n')
    print(Result_drop_null_date['ENDDATE'] - Result_drop_null_date['STARTDATE'])

    ### reset index(drop the old index):
    Result_drop_null_date = Result_drop_null_date.reset_index(drop=True)

    ### select the data which time period is not less than 5 days
    print('\n========= Drop less than five days =========\n')
    data_drop_less_than_five = Result_drop_null_date[pd.Series(delta.days for delta in (Result_drop_null_date['ENDDATE'] - Result_drop_null_date['STARTDATE'])) >= 5] # pd.Series(xxxxxx : select the attribute "days":
    print(data_drop_less_than_five) 
    export_less_than_five_csv = data_drop_less_than_five.to_csv('paperCreater\export_result\data_drop_less_than_five.csv', index = None, header=True) # Don't forget to add '.csv' at the end of the path

    ### select the data which absolute value of time period is not less than 5 days(some time period is negative)
    print('\n========= Drop less than abs(five) days =========\n')
    data_drop_less_than_abs_five = Result_drop_null_date[pd.Series(abs(delta.days) for delta in (Result_drop_null_date['ENDDATE'] - Result_drop_null_date['STARTDATE'])) >= 5]
    print(data_drop_less_than_abs_five)
    export_less_than_abs_five_csv = data_drop_less_than_abs_five.to_csv('paperCreater\export_result\data_drop_less_than_abs_five.csv', index = None, header=True)

    print('\n========= Display negative period =========\n')
    pd.set_option('display.max_rows', None)
    print(Result_drop_null_date[pd.Series(delta.days for delta in (Result_drop_null_date['ENDDATE'] - Result_drop_null_date['STARTDATE'])) < 0].loc[:, 'SUBJECT_ID':'ENDDATE'])