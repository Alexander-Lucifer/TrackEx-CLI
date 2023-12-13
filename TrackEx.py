import pymysql
from random import choice
from platform import system
import os
from time import sleep
import tabulate
import datetime

def clear():
    if system() == "Windows":
        os.system("cls")
    elif system() == "Linux":
        os.system("clear")

#data = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*_;:1234567890"
# Function to connect to MySQL database
def connect_to_database():
    try:
        connection = pymysql.connect(
            host="localhost",
            user="god",
            password="Lucifer@666",
            database="TrackEx",
            
        )

        # Change terminal title
        #os.system("title TrackEx")

        # Change prompt color to green
        #os.system("color a")

        return connection
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return None


# Function to create the expense table if not exists
def create_expense_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            UserName VARCHAR(255),
            description VARCHAR(255),
            amount DECIMAL(10, 2),
            date DATE,
            startingAmt DECIMAL(10, 2)
        )
    """)
def create_account_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ACC (
            id INT AUTO_INCREMENT PRIMARY KEY,
            UserName VARCHAR(255),
            PassWord VARCHAR(16),
            PassKey VARCHAR(255)
        )
    """)

def Keygen(data):
    x = ""
    for i in range(0,17):
        x += choice(data)
    return x

#Signup
def add_user(cursor, name, Pass, Key):
    query = "INSERT INTO ACC (UserName, PassWord, PassKey) VALUES (%s, %s, %s)"
    data = (name, Pass, Key)
    cursor.execute(query, data)
#

def report(cursor, name):
    y1,m1,d1 = input("Enter Starting Year: "),  input("Enter Starting Month: "), input("Enter Starting Date: ")
    if y1 == "":
        y1 = datetime.datetime.today().year
    if m1 == "":
        m1 = datetime.datetime.today().month
    if d1 == "":
        d1 = datetime.datetime.today().day
    y2,m2,d2 = input("Enter ending Year: "),  input("Enter ending Month: "), input("Enter ending Date: ")
    if y2 == "":
        y2 = datetime.datetime.today().year
    if m2 == "":
        m2 = datetime.datetime.today().month
    if d2 == "":
        d2 = datetime.datetime.today().day
    starting = datetime.date(int(y1),int(m1),int(d1))
    ending = datetime.date(int(y2),int(m2),int(d2))
    

    query = "SELECT date, amount, description from expenses WHERE UserName = %s AND date BETWEEN %s AND %s"
    dates = (name, starting, ending)
    cursor.execute(query, dates)
    rep = cursor.fetchall()
    
    
    if not rep:
        print("No expenses found.")
    else:
        print(f"Here's your report for the term {starting} till {ending}")
        print("")
        print("")
        f = tabulate.tabulate(rep,headers = ['Date', 'Amount', 'Description'], tablefmt="fancy_grid")
        print(f)
    
    

#Auth
def Auth(cursor, name, Pass):
    query = "select * from ACC where UserName = %s and PassWord = %s"
    data = (name, Pass)
    cursor.execute(query, data)
    user = cursor.fetchone()

    return user is not None

#Key Auth
def keyauth(cursor, name, Pass):
    query = "select PassKey from ACC where UserName = %s and PassWord = %s"
    val = (name, Pass)
    cursor.execute(query, val)
    Ckey = cursor.fetchone()

    return Ckey

# Function to add an expense
def add_expense(cursor, name, description, amount, date):
    query = "INSERT INTO expenses (UserName, description, amount, date) VALUES (%s, %s, %s, %s)"
    data = (name, description, amount, date)
    cursor.execute(query, data)

# Function to view all expenses
def view_expenses(cursor, name):
    query = "SELECT description, amount, date FROM expenses WHERE UserName = %s"
    data = (name)
    cursor.execute(query, data)
    expenses = cursor.fetchall()
    f = tabulate.tabulate(expenses)

    if not expenses:
        print("No expenses found.")
    else:
        print("Where  Amt   Date")
        print(f)

def spent(cursor, name):
    query = "SELECT SUM(amount) from expenses WHERE UserName = %s"
    data = (name)
    cursor.execute(query, data)
    expenses = cursor.fetchall()
    f = tabulate.tabulate(expenses)
    
    if not expenses:
        print("No expenses found.")
    else:
        print("Total Spend")
        print(f)
    
def dele(cursor, name):
    print("How to delete? \n1By Amount \n2By Description")
    choice = input('>_')
    if choice == "1":
        amt = input("Enter Amount: ")
        query = "DELETE FROM expenses WHERE amount = %s"
        cursor.execute(query, amt)
        print('record Deleted')
    else:
        amt = input("Enter Description: ")
        query = "DELETE FROM expenses WHERE description = %s"
        cursor.execute(query, amt)
        print('record Deleted')
# Main function
def main():
    Mame = ""
    connection = connect_to_database()

    if connection:
        cursor = connection.cursor()
        create_expense_table(cursor)
        create_account_table(cursor)
        while True:
            #sleep(30)
            Authen:bool = False
            clear()
            count = 1
            print(system())
            clear()
            print("")
            print("Welcome To Track.Ex \nby Suryanshu Mittal and Shivansh Sharma \nPress1 to create an Account \nPress 2 to Log-In \nPress 3 to Exit")
            choice = input("Enter Your Choice: ")
            

            if choice == "3":
                break
            if choice == "1":
                sleep(6)
                name = input("Enter Your UserName: ")
                Pass = input("Enter Your passWord: ")
                CPass = input("Confirm Your passWord: ")
                if Pass == CPass:
                    if not Auth(cursor, name, Pass):
                        add_user(cursor, name, Pass, "0")
                        connection.commit()
                    continue
            else:
                name = input("Enter Your UserName: ")
                Pass = input("Enter your password: ")
                if Auth(cursor, name, Pass):
                    print("Auth Success; Redirecting...")
                    Authen = True
                    sleep(5)
                    clear()
                else:
                    print("Auth Failed! username or password is wrong")
                    count-=1
                if count == 0:
                    sleep(5)
                    print("Bye!")
                    break
                    raise KeyboardInterrupt
                    os.system("exit")
                    print("Attempts Finished, \npress1 to try again \npress 3 to exit")
                    '''
                    choice =  input("Enter your choice: ")

                    if choice == "1":
                        key = input("Enter your Key: ")
                        if key == keyauth(cursor, name, Pass):
                            Authen = True
                    '''
            if Authen == True:
                
                while Authen == True:
                    clear()
                    todaydate = datetime.datetime.today()
                    day = todaydate.day

                    print(f"Welcome {name}\nPress 1.> Add Expense\nPress 2. > View Expenses\nPress 3. > to get Total Money Spent \nPress 4 > to delete record \nPress 5 > Exit")
                    choice = input("Enter your choice: ")

                    if choice == "1":
                        ay = False
                        while ay == False:
                            
                            description = input("Enter expense description: ")
                            amount = float(input("Enter expense amount: "))
                            date = str(datetime.datetime.today()).split()[0]
                            print(f"Data to be registered: \nAmount   Description \n{amount}   {description}")
                            y = input("Register? (Y/N)> ")
                            
                            if y in "nN":
                                continue
                            else:
                                add_expense(cursor,name, description, amount, date)
                                ay = True
                        connection.commit()
                        print("Your Data is being registered, please wait ...")
                        sleep(5)
                        print("Expense added successfully.")
                        continue
                    elif choice == "2":
                        report(cursor, name)
                        i = input('>_')
                        if i != "":
                            continue
                        else:
                            continue
                    elif choice == "3":
                        sleep(5)
                        spent(cursor, name)
                        i = input('>_')
                        if i != "":
                            continue
                        else:
                            continue
                    elif choice == "4":
                        dele(cursor, name)
                        connection.commit()

                    elif choice == "5":
                        Authen = False
                    
                    else:
                        print("Invalid choice. Please try again.")
                    if Authen == False:
                        print("Authentication Error, please wait...")
                        sleep(2)
                        os.system("exit")
        connection.close()
            

if __name__ == "__main__":
    main()


