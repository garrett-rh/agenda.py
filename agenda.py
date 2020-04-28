#! /usr/bin/python3

import sqlite3

#Create the connection to the database & set cursor
conn = sqlite3.connect('/home/garrett/.agenda/agenda.db')
c = conn.cursor()

#Main function. Sets up DB & calls menu.

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
        conn.commit()

#Takes user input, then adds calls appropriate function, waits for "Enter" then returns to menu.
def menu():
    choice = int(input("""Choose one of the following options:
    1) View by Date.
    2) View by Course.
    3) View by Status.
    4) Edit the Agenda.
    5) Manage the Agenda.
    99) Quit.
-->""")
    )

    if choice == 1:
        date();input()
    elif choice == 2:
        course();input()
    elif choice == 3:
        status();input()
    elif choice == 4:
        edit();print()
    elif choice == 5:
        manage();print()
    elif choice == 99:
        conn.commit()
        conn.close()
        quit()
    else:
        print("Invalid Choice")
    menu()

#Function to display items organized by date.
def date():
    c.execute("SELECT * FROM agenda")
    data = c.fetchall()
    dateList = []

    for i in data:
        dateList.append(i)
   #sorts by the lambda set to look at the index 1.
    dateList.sort(key = lambda dateList: dateList[1])
    for i in dateList:
        print(f"{i[4]:15} {i[1]} {i[2]:10} {i[3]}")

#Function to display by course in A-Z order
def course():
    c.execute("SELECT * FROM agenda")
    data = c.fetchall()
    dateList = []

    for i in data:
        dateList.append(i)

    dateList.sort(key = lambda dateList: dateList[2])
    for i in dateList:
        print(f"{i[4]:15}{i[1]} {i[2]:10} {i[3]}")

#Sorts by status in alphabetic order
def status():
    c.execute("SELECT * FROM agenda")
    data = c.fetchall()
    dateList = []

    for i in data:
        dateList.append(i)
    dateList.sort(key = lambda dateList: dateList[4])
    for i in dateList:
        print(f"{i[4]:15}{i[1]} {i[2]:10} {i[3]}")

#Allows for editing the DB.
def edit():
    c.execute("SELECT * FROM agenda")
    data = c.fetchall()

    #Prints out info in the table via the course. I found this to be most useful
    #because I do my school work by course.
    data.sort(key = lambda dateList: dateList[2])
    for i in data:
        print(f"{i[0]:5} -- {i[3]:50}{i[2]:10} {i[1]:10} {i[4]}")

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
        new = new.zfill(5)
        c.execute("UPDATE agenda SET date=(?) WHERE ID=(?)",(new,editNum))
    elif inputEdit == 2:
        new = str(input("Enter new course: "))
        c.execute("UPDATE agenda SET class=(?) WHERE ID=(?)",(new,editNum))

    elif inputEdit == 3:
        new = str(input("Enter new assignement: "))
        c.execute("UPDATE agenda SET assignment=(?) WHERE ID=(?)",(new,editNum))
    elif inputEdit == 4:
        new = str(input("Enter new status: "))
        c.execute("UPDATE agenda SET status=(?) WHERE ID=(?)",(new,editNum))

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

    def delete():
        yN = str(input("Are you sure you want to delete the agenda? (y/n)"))
        if "y" in yN.lower():

            keepUnfinished = str(input("Would you like to keep all items without a status of 'Finished'?"))
            if "y" in keepUnfinished.lower():
                c.execute("SELECT * FROM agenda WHERE status != 'Finished'")
                data = c.fetchall()

            else:
                pass
            c.execute("DELETE FROM agenda")
            conn.commit()

            c.execute("""CREATE TABLE IF NOT EXISTS agenda(
                ID integer,
                date text,
                class text,
                assignment text,
                status text
                )"""
                )
            conn.commit()
            for a in range(len(data)):
                deleteID = a
                (c.execute("INSERT INTO agenda(ID, date, class, assignment, status) VALUES(?,?,?,?,?)",
                    (deleteID, data[a][1], data[a][2], data[a][3], data[a][4])))
#Moved conn.commit() outside of loop for efficiency.

            conn.commit()
            print("Database deleted")
            main()
        else:
            manage()

    def removeEntry():
        c.execute("SELECT * FROM agenda")
        toBeRemoved = c.fetchall()
        for i in toBeRemoved:
            print(f"{i[0]} -- {i[4]:15} {i[1]} {i[2]:10} {i[3]}")

        entry = int(input("Which entry would you like removed?"))
        print(f"Are you sure you want to remove entry {entry} (y/n)? ")
        confirm = str(input("-->"))

        if "y" in confirm.lower():
            c.execute("DELETE FROM agenda where ID=(?)", (entry,))
            conn.commit()
            more = str(input("Delete more entries (y/n)?"))
            if "y" in more.lower():
                removeEntry()
            else:
                pass
        else:
            pass

    def export():
        c.execute("SELECT * FROM agenda")
        with open('/home/garrett/schedule.txt', 'w') as f:
            for i in c:
                f.write(f"{i[4]:15} {i[1]} {i[2]:10} {i[3]}\n")
        print("Exported table to home folder...")

    def addEntry():
        c.execute("SELECT ID FROM agenda")
        idNum = c.fetchall()
        idList = []
        for i in idNum:
            for a in i:
                idList.append(a)
        if 0 not in idList:
                newID = 0
        else:
            newID = 0
            while newID in idList:
                newID +=1

        dueDate  = str(input("Enter due date: "))
        dueDate = dueDate.zfill(5)
        course = str(input("Enter course: "))
        assignment = str(input("Enter assignment: "))
        status = "Unfinished"
        c.execute("INSERT INTO agenda(ID, date, class, assignment, status) VALUES(?,?,?,?,?)", (newID, dueDate, course, assignment, status))
        conn.commit()

        again = str(input("Would you like to enter another entry?"))
        if "y" in again.lower():
            addEntry()
        else:
            pass
    manageChoice = int(input("1)Add Entry\n2)Remove Entry\n3)Export Agenda\n4)Delete Table\n-->"))


    if manageChoice == 1:
        addEntry()
    elif manageChoice == 2:
        removeEntry()
    elif manageChoice == 3:
        export()
    elif manageChoice == 4:
        delete()
    else:
        print("Please enter a proper answer")
        manage()

if __name__ == "__main__":
    main()
