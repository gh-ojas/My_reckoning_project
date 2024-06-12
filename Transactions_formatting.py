import mysql.connector
import pandas as pd
import openpyxl
import os
from tkinter import messagebox

variable = mysql.connector.connect(host='localhost',user='root',password='ojasvi940',database='my_transactions')
cur = variable.cursor()

def load_data():
    
    Files=[]
    for file in os.listdir('G:\\My Drive\\'):
        if file.endswith(".csv"):Files.append(file)
    if Files != []:          
        for i in range(len(Files)):
            if i == 0:
                data = pd.read_csv(f"G:\\My Drive\\{Files[i]}").drop_duplicates()
            else:
                data = pd.concat([data,pd.read_csv(f'G:\\My Drive\\{Files[i]}')]).drop_duplicates().sort_values("Date")
            
        
        data = data.iloc[:,[0,1,2,4,5,6,3]]
        data = data.rename(columns={'type':'Type','To payment mode':'Transfer','Payment mode':'Bank'})
        data['Date'] = pd.to_datetime(data['Date'])
        data['Amount'] = data['Amount'].str.replace(',','').astype(float)
        data = data.sort_values("Date")
        data = data.reset_index(drop=True)
        cur.execute(f"Select min(Sr_no) from transactions where date = '{data['Date'][0].date()}'")
        Sr_no = cur.fetchone()
        cur.execute(f"Select max(Sr_no) from transactions where date = '{data['Date'][len(data)-1].date()}'")
        Sr_no_end = cur.fetchone()

        if Sr_no[0] != None:
            if Sr_no_end[0] == None:    old_data = pd.read_sql(f"SELECT Date,Category,Amount,Type,Bank,Transfer,Note FROM Transactions where Sr_no < {Sr_no[0]};",'mysql://root:ojasvi940@localhost/my_transactions')
            if Sr_no_end[0] != None:    old_data = pd.read_sql(f"SELECT Date,Category,Amount,Type,Bank,Transfer,Note FROM Transactions where Sr_no < {Sr_no[0]} or Sr_no > {Sr_no_end[0]};",'mysql://root:ojasvi940@localhost/my_transactions')
        
        else:                           old_data = pd.read_sql(f"SELECT Date,Category,Amount,Type,Bank,Transfer,Note FROM Transactions;",'mysql://root:ojasvi940@localhost/my_transactions')
        
        old_data['Date'] = pd.to_datetime(old_data['Date'],format='%Y-%m-%d')
        data = pd.concat([old_data,data])
        data = data.sort_values(by='Date')
        data = data.fillna('None')
        data['Bank'] = data['Bank'].str.replace('HDFC Tata Neu','HDFCTataNeu')
        data['Transfer'] = data['Transfer'].str.replace('HDFC Tata Neu','HDFCTataNeu')
        data = data.drop_duplicates()
        data = data.reset_index(drop=True)
        return data
    
    else:
        messagebox.showerror("Error!","No Files in the dictionary!")
        data = pd.read_sql("SELECT Date,Category,Amount,Type,Bank,Transfer,Note FROM Transactions;",'mysql://root:ojasvi940@localhost/my_transactions')
        data['Date'] = pd.to_datetime(data['Date'],format='%Y-%m-%d')    
        data = data.sort_values(by='Date')
        data = data.fillna('None')
        data = data.drop_duplicates()
        data = data.reset_index(drop=True)
        return data

data = load_data()

data['Bank'] = data['Bank'].str.replace('HDFC Tata Neu','HDFCTataNeu')
data['Transfer'] = data['Transfer'].str.replace('HDFC Tata Neu','HDFCTataNeu')

data['Balance'] = ['None' for j in data['Amount']]
data['Balance'][0] = 26314

data['HDFC'] = ['None' for j in data['Amount']]
data['HDFC'][0] = 17443

data['SBI'] = ['None' for j in data['Amount']]
data['SBI'][0] = 6114

data['UPI Lite'] = ['None' for j in data['Amount']]
data['UPI Lite'][0] = 2757

data['Cash'] = ['None' for j in data['Amount']]
data['Cash'][0] = 0

Limit = 60000.0
data['HDFCTataNeu'] = ['None' for j in data['Amount']]
data['HDFCTataNeu'][0] = Limit


for i in range(1,len(data['Amount'])):

    # For Expenses
    if data['Type'][i] == 'Expense':
        data[data['Bank'][i]][i] = float(data[data['Bank'][i]][i-1]) - float(data['Amount'][i])
        Banks = ['HDFC','SBI','UPI Lite','Cash','HDFCTataNeu']
        Banks.remove(data['Bank'][i])
        for j in Banks:
            data[j][i] = float(data[j][i-1])            
        data['Balance'][i] = float(data['HDFC'][i]) + float(data['SBI'][i]) + float(data['UPI Lite'][i]) + float(data['Cash'][i])
        os.system('cls')

    # For income
    elif data['Type'][i] == 'Income':
        data[data['Bank'][i]][i] = float(data[data['Bank'][i]][i-1]) + float(data['Amount'][i])
        Banks = ['HDFC','SBI','UPI Lite','Cash','HDFCTataNeu']
        Banks.remove(data['Bank'][i])
        for j in Banks:
            data[j][i] = float(data[j][i-1])            
        data['Balance'][i] = float(data['HDFC'][i]) + float(data['SBI'][i]) + float(data['UPI Lite'][i]) + float(data['Cash'][i])
        os.system('cls')

    # For Transfers
    elif data['Type'][i] == 'Transfer':
        data[data['Bank'][i]][i] = round(float(data[data['Bank'][i]][i-1]),1) - round(float(data['Amount'][i]),1)
        data[data['Transfer'][i]][i] = round(float(data[data['Transfer'][i]][i-1]),1) + round(float(data['Amount'][i]),1)
        Banks = ['HDFC','SBI','UPI Lite','Cash','HDFCTataNeu']
        Banks.remove(data['Bank'][i])
        Banks.remove(data['Transfer'][i])
        for j in Banks:
            data[j][i] = float(data[j][i-1])
        data['Balance'][i] = float(data['HDFC'][i]) + float(data['SBI'][i]) + float(data['UPI Lite'][i]) + float(data['Cash'][i])
        if data['Transfer'][i] == 'HDFCTataNeu':data['HDFCTataNeu'][i] = Limit
        os.system('cls')

os.system('cls')

data.to_csv('C:\\Users\\ojasv\\OneDrive\\Desktop\\Temp.csv',index=False)
print(f"HDFC \t\t:\t {data['HDFC'][len(data)-1]}\nSBI \t\t:\t {data['SBI'][len(data)-1]}\nUPI Lite \t:\t {round(data['UPI Lite'][len(data)-1],2)}\nCash \t\t:\t {data['Cash'][len(data)-1]}\n\nTotal \t\t:\t {data['Balance'][len(data)-1]}\n\n")

# print(data.tail(60))

concent = 'n'

concent = input('Update this? Y/N : ')

if concent.capitalize() == 'Y':
    cur.execute('Delete from transactions')
    print('Dataset shape: ',data.shape)
    for i in range(len(data['Amount'])):
        print(f"INSERT INTO Transactions VALUES ({i+1},'{data['Date'][i]}','{data['Category'][i]}',{data['Amount'][i]},'{data['Type'][i]}','{data['Bank'][i]}','{data['Transfer'][i]}','{data['Note'][i]}',{data['Balance'][i]},{data['HDFC'][i]},{data['SBI'][i]},{data['UPI Lite'][i]},{data['Cash'][i]},{data['HDFCTataNeu'][i]})")
        cur.execute(f"INSERT INTO transactions VALUES ({i+1},'{data['Date'][i]}','{data['Category'][i]}',{data['Amount'][i]},'{data['Type'][i]}','{data['Bank'][i]}','{data['Transfer'][i]}','{data['Note'][i]}',{data['Balance'][i]},{data['HDFC'][i]},{data['SBI'][i]},{data['UPI Lite'][i]},{data['Cash'][i]},{data['HDFCTataNeu'][i]})")

    variable.commit()
    data.to_csv('G:\\My Drive\\Projects\\Reckoning\\Report.csv',index=False)
    print('\nOperation successful!\n\nOpening Dashboard')
else:print('Operation aborted!\n\nOpening Dashboard')
os.startfile('D:\\Work\\Excel\\My reckoning.xlsm')
