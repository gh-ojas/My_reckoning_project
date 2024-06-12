import pandas as pd
import mysql.connector
import os

os.system('cls')
data = pd.read_csv('G:\\My Drive\\Projects\\Reckoning\\Report.csv')

variable = mysql.connector.connect(host='localhost',user='root',password='ojasvi940',database='my_transactions')
cur = variable.cursor()
print(data)
for i in range(data.shape[0]):
    print(f"INSERT INTO Transactions VALUES ({i+1},'{data['Date'][i]}','{data['Category'][i]}',{data['Amount'][i]},'{data['Type'][i]}','{data['Bank'][i]}','{data['Transfer'][i]}','{data['Note'][i]}',{data['Balance'][i]},{data['HDFC'][i]},{data['SBI'][i]},{data['UPI Lite'][i]},{data['Cash'][i]},{data['HDFCTataNeu'][i]})")
    cur.execute(f"INSERT INTO Transactions VALUES ({i+1},'{data['Date'][i]}','{data['Category'][i]}',{data['Amount'][i]},'{data['Type'][i]}','{data['Bank'][i]}','{data['Transfer'][i]}','{data['Note'][i]}',{data['Balance'][i]},{data['HDFC'][i]},{data['SBI'][i]},{data['UPI Lite'][i]},{data['Cash'][i]},{data['HDFCTataNeu'][i]})")

print(f"HDFC \t\t:\t {data['HDFC'][len(data)-1]}\nSBI \t\t:\t {data['SBI'][len(data)-1]}\nUPI Lite \t:\t {round(data['UPI Lite'][len(data)-1],2)}\nCash \t\t:\t {data['Cash'][len(data)-1]}\n\nTotal \t\t:\t {data['Balance'][len(data)-1]}\n\n")

i = input('Update? : ')
if i.capitalize() == 'Y':
    variable.commit()