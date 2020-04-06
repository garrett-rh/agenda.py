#! /usr/bin/python3

import sqlite3

conn = sqlite3.connect('/home/garrett/.agenda/agenda.db')
c = conn.cursor()
def main():
    start()
    menu()

def start():

    c.execute("""CREATE TABLE IF NOT EXISTS agenda(
        ID integer,
        date text,
        class text,
        assignment text,
        status text
        )"""
        )

def menu():
    choice = int(input("""Choose one of the following options:
    1) View by Date.
    2) View by Course.
    3) View by Status.
    4) Edit the Agenda.
    5) Manage the Agenda.
    6) Quit.
-->""")
    )
    print('\n')

    if choice == 1:
        date();input();menu();
    elif choice == 2:
        course();input();menu()
    elif choice == 3:
        status();input();menu()
    elif choice == 4:
        edit();input();menu()
    elif choice == 5:
        manage()
    elif choice == 6:
        quit()
    else:
        print("Invalid Choice")
        start()

def date():
    c.execute("SELECT * FROM agenda")
    data = c.fetchall()
    dateList = []

    for i in data:
        dateList.append(i)
   
    dateList.sort(key = lambda dateList: dateList[1])
    for i in dateList:
        print(f"{i[4]:15} {i[1]} {i[2]:10} {i[3]}")

def course():
    c.execute("SELECT * FROM agenda")
    data = c.fetchall()
    dateList = []

    for i in data:
        dateList.append(i)
   
    dateList.sort(key = lambda dateList: dateList[2])
    for i in dateList:
        print(f"{i[4]:15}{i[1]} {i[2]:10} {i[3]}")

def status():
    c.execute("SELECT * FROM agenda")
    data = c.fetchall()
    dateList = []

    for i in data:
        dateList.append(i)
    dateList.sort(key = lambda dateList: dateList[4])
    for i in dateList:
        print(f"{i[4]:15}{i[1]} {i[2]:10} {i[3]}")

def edit():
    c.execute("SELECT * FROM agenda")
    data = c.fetchall()
    for i in data:
        print(f"{i[0]} -- {i[4]:15}{i[1]} {i[2]:10} {i[3]}")

    editNum = int(input("Enter ID of Entry to Edit: "))
    inputEdit = int(input("""Which input to edit...
    1) Due Date
    2) Course
    3) Assignment
    4) Status
-->"""))
   
    if 0 > inputEdit > 5:
        print("Please enter a number 1-4")
        edit()

    if inputEdit == 1:
        new = str(input("Enter new due date: "))
        c.execute("UPDATE agenda SET date=(?) WHERE ID=(?)",(new,editNum))
    elif inputEdit == 2:
        new = str(input("Enter new course: "))
        c.execute("UPDATE agenda SET class=(?) WHERE ID=(?)",(new,editNum))

    elif inputEdit == 3:
        new = str(input("Enter new assignement: "))
        c.execute(f"UPDATE agenda SET assignment=(?) WHERE ID=(?)",(new,editNum))
    elif inputEdit == 4:
        new = str(input("Enter new status: "))
        c.execute(f"UPDATE agenda SET status=(?) WHERE ID=(?)",(new,editNum))

    else:
        print("Please enter a proper input.")
        edit()
    conn.commit()

    again = str(input("Would you like to edit another entry?"))
    if again.lower() in "y":
        edit()
    else:
        pass
def manage():
    
    def removeEntry():
        c.execute("SELECT * FROM agenda")
        toBeRemoved = c.fetchall()
        for i in toBeRemoved:
            print(f"{i[0]} -- {i[4]:15} {i[1]} {i[2]:10} {i[3]}")
    
        entry = int(input("Which entry would you like removed?"))
        print(type(entry))
        print(f"Are you sure you want to remove entry {entry} (y/n)? ")
        confirm = str(input("-->"))

        if "y" in confirm.lower():
            c.execute("DELETE FROM agenda where ID=(?)", (entry,))
            conn.commit()
            more = str(input("Delete more entries (y/n)?"))
            if "y" in more.lower():
                removeEntry()
            else:
                menu()
        else:
            menu()

    def addEntry():
        c.execute("SELECT ID FROM agenda")
        idNum = c.fetchall()
        if not idNum:
            newID = 0
        else:
            newID = max(idNum); newID = newID[0] + 1
        dueDate  = str(input("Enter due date: "))

        course = str(input("Enter course: "))
        assignment = str(input("Enter assignment: "))
        status = "Unfinished"
        c.execute("INSERT INTO agenda(ID, date, class, assignment, status) VALUES(?,?,?,?,?)", (newID, dueDate, course, assignment, status))
        conn.commit()

        again = str(input("Would you like to enter another entry?"))
        if "y" in again.lower():
            addEntry()
        else:
            menu()
    manageChoice = int(input("1)Add Entry\n2)Remove Entry\n3)Delete Table\n-->"))


    if manageChoice == 1:
        addEntry()
    elif manageChoice == 2:
        removeEntry()
    elif manageChoice ==3:
        yN = str(input("Are you sure you want to delete the agenda? (y/n)"))
        if "y" in yN.lower():
            c.execute("DELETE FROM agenda")
            conn.commit()
            print("Database deleted")
            main()
        else:
            manage()
    else:
        print("Please enter a proper answer")
        manage()

main()
