#!/usr/bin/python3

import sqlite3

class Database:

    def __init__(self):
        self.conn = sqlite3.connect('/home/garrett/.agenda/agenda.db')
        self.c = self.conn.cursor()
        self.c.execute("SELECT * FROM agenda")
        self.query_in_list = self.c.fetchall()

    def create_table(self):
        self.c.execute("""CREATE TABLE IF NOT EXISTS agenda(
                ID integer,
                date text,
                class text,
                assignment text,
                status text
                )"""
                )
        self.commit()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.commit()
        self.conn.close()

class View(Database):

    def __init__(self): 
        super().__init__()
     
    def by_date(self):
        self.query_in_list.sort(key = lambda query_in_list: query_in_list[1])
        for i in self.query_in_list:
            print(f"{i[4]:15} {i[1]} {i[2]:10} {i[3]}")

    def by_course(self):
        self.query_in_list.sort(key = lambda query_in_list: query_in_list[2])
        for i in self.query_in_list:
            print(f"{i[4]:15}{i[1]} {i[2]:10} {i[3]}")

    def by_status(self):
        self.query_in_list.sort(key = lambda query_in_list: query_in_list[4])
        for i in self.query_in_list:
            print(f"{i[4]:15}{i[1]} {i[2]:10} {i[3]}")

class Edit(Database):

    def __init__(self):
        super().__init__()

    def edit_entries(self):
        self.query_in_list.sort(key = lambda query_in_list: query_in_list[2])
        for i in self.query_in_list:
            print(f"{i[0]:5} -- {i[3]:50}{i[2]:10} {i[1]:10} {i[4]}")
    
        editNum = int(input("Enter ID of Entry to Edit: "))
        inputEdit = int(input("""Which input to edit...
1) Due Date
2) Course
3) Assignment
4) Status
-->"""))
    
        if inputEdit == 1:
            new = str(input("Enter new due date: "))
            new = new.zfill(5)
            self.c.execute("UPDATE agenda SET date=(?) WHERE ID=(?)",(new,editNum))
        elif inputEdit == 2:
            new = str(input("Enter new course: "))
            self.c.execute("UPDATE agenda SET class=(?) WHERE ID=(?)",(new,editNum))
        elif inputEdit == 3:
            new = str(input("Enter new assignement: "))
            self.c.execute("UPDATE agenda SET assignment=(?) WHERE ID=(?)",(new,editNum))
        elif inputEdit == 4:
            new = str(input("Enter new status: "))
            self.c.execute("UPDATE agenda SET status=(?) WHERE ID=(?)",(new,editNum))
        else:
            print("Please enter a proper input.")
        self.commit()
        again = str(input("Would you like to edit another entry?"))
        if again.lower() in "y":
            Edit().edit_entries()
    
class Manage(Database):

    def __init__(self):
        super().__init__()
        choice = int(input("1)Add Entry\n2)Remove Entry\n3)Export Agenda\n4)Delete Table\n-->"))
        if choice == 1:
            self.adding_new_entries()
        elif choice == 2:
            self.remove_entries()
        elif choice == 3:
            self.exporting_agenda()
        elif choice == 4:
            self.delete_agenda()
        else:
            print("Please enter a proper answer")
            self.__init__()

    def adding_new_entries(self):
        self.c.execute("SELECT ID FROM agenda")
        id_num = self.c.fetchall()
        if 0 not in [i[0] for i in id_num]:
            new_id = 0
        else:
            new_id = 0
            while new_id in [i[0] for i in id_num]:
                new_id +=1
        dueDate = str(input("Enter due date: ")).zfill(5)
        course = str(input("Enter course: "))
        assignment = str(input("Enter assignment: "))
        status = "Unfinished"
        self.c.execute("INSERT INTO agenda(ID, date, class, assignment, status) VALUES(?,?,?,?,?)", (new_id, dueDate, course, assignment, status))
        self.commit()
        again = str(input("Would you like to enter another entry?"))
        if "y" in again.lower():
            self.adding_new_entries()

    def remove_entries(self):
        self.c.execute("SELECT * FROM agenda")
        self.query_in_list = self.c.fetchall()
        for i in self.query_in_list:
            print(f"{i[0]} -- {i[4]:15} {i[1]} {i[2]:10} {i[3]}")
        entry = int(input("Which entry would you like removed?"))
        confirm= str(input(f"Are you sure you want to remove entry {entry} (y/n)?\n-->"))
        if "y" in confirm.lower():
            self.c.execute("DELETE FROM agenda where ID=(?)", (entry,))
            self.commit()
            more = str(input("Delete more entries (y/n)?"))
            if "y" in more.lower():
                self.remove_entries()

    def exporting_agenda(self):
        with open('/home/garrett/schedule.txt', 'w') as f:
            for i in self.query_in_list:
                f.write(f"{i[4]:15} {i[1]} {i[2]:10} {i[3]}\n")
        print("Exported table to home folder...")

    def delete_agenda(self):
        delete_the_agenda = str(input("Are you sure you want to delete the agenda? (y/n)"))
        if "y" in delete_the_agenda.lower():
            keep_status_unfinished = str(input("Would you like to keep all items without a status of 'Finished'?"))
            if "y" in keep_status_unfinished.lower():
                self.c.execute("SELECT * FROM agenda WHERE status != 'Finished'")
                all_unfinished_entries = self.c.fetchall()
            self.c.execute("DELETE FROM agenda")
            self.create_table()
            self.commit()
            for a in all_unfinished_entries:
                delete_id = a
                (self.c.execute("INSERT INTO agenda(ID, date, class, assignment, status) VALUES(?,?,?,?,?)",
                    (delete_id, all_unfinished_entries[a][1], all_unfinished_entries[a][2], all_unfinished_entries[a][3], all_unfinished_entries[a][4])))
            self.commit()
            print("Database deleted")
            menu()
        else:
            self.__init__()

def menu():
    choice = int(input("""Choose one of the following options
1)  View by date.
2)  View by course.
3)  View by status.
4)  Edit the agenda.
5)  Manage the agenda.
99) Quit.
-->"""))
    
    if choice == 1:
        View().by_date()
    elif choice == 2:
        View().by_course()
    elif choice == 3:
        View().by_status()
    elif choice == 4:
        Edit().edit_entries()
    elif choice == 5:
        Manage()   
    elif choice == 99:
        quit()
    else:
        print("Not a proper input. Please try again.")
        menu()

menu()
#if __name__ == "__main__":
#    main()
