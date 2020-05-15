#!/usr/bin/python3

import sqlite3

class Database:

    def __init__(self):
        self.conn = sqlite3.connect('/home/garrett/.agenda/agenda.db')
        self.c = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        if isinstance(exc_value, Exception):
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()

    def select_all(self):
        self.execute("SELECT * FROM agenda")
        return self.fetchall()
    
    def query(self, sql, params=None):
        self.c.execute(sql, params or ())
        return self.fetchall()
    
    def execute(self, sql, params=None):
        self.c.execute(sql, params or ())

    def fetchall(self):
        return self.c.fetchall()

    def commit(self):
        self.conn.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.conn.close()
        quit()

def View(choice):

    with Database() as db:
        query_in_list = db.select_all()
    if choice == 1:
        view_method = 1
    elif choice == 2:
        view_method = 2
    elif choice == 3:
        view_method = 4
    query_in_list.sort(key = lambda query_in_list: query_in_list[view_method])
    for i in query_in_list:
        print(f"{i[4]:15} {i[1]} {i[2]:10} {i[3]}")

def Edit():
    with Database() as db:
       query_in_list = db.select_all()
       query_in_list.sort(key = lambda query_in_list: query_in_list[2])
       for i in query_in_list:
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
           db.execute("UPDATE agenda SET date=(?) WHERE ID=(?)",(new,editNum))
       elif inputEdit == 2:
           new = str(input("Enter new course: "))
           db.execute("UPDATE agenda SET class=(?) WHERE ID=(?)",(new,editNum))
       elif inputEdit == 3:
           new = str(input("Enter new assignement: "))
           db.execute("UPDATE agenda SET assignment=(?) WHERE ID=(?)",(new,editNum))
       elif inputEdit == 4:
           new = str(input("Enter new status: "))
           db.execute("UPDATE agenda SET status=(?) WHERE ID=(?)",(new,editNum))
       else:
           print("Please enter a proper input.")
       db.commit()
       again = str(input("Would you like to edit another entry?"))
       if again.lower() in "y":
           Edit()
    
def Manage():
    choice = int(input("1)Add Entry\n2)Remove Entry\n3)Export Agenda\n4)Delete Table\n-->"))
    boolean_for_loop = True
    with Database() as db:
        query_in_list = db.select_all()
        if choice == 1:
            while boolean_for_loop is True:
                id_num = db.query("SELECT ID FROM agenda")
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
                db.execute("INSERT INTO agenda(ID, date, class, assignment, status) VALUES(?,?,?,?,?)", (new_id, dueDate, course, assignment, status))
                db.commit()
                again = str(input("Would you like to enter another entry?"))
                if "y" not in again.lower():
                    boolean_for_loop = False

        elif choice == 2:
            boolean_for_loop = True
            while boolean_for_loop is True:
               for i in query_in_list:
                   print(f"{i[0]} -- {i[4]:15} {i[1]} {i[2]:10} {i[3]}")
               entry = int(input("Which entry would you like removed?"))
               confirm= str(input(f"Are you sure you want to remove entry {entry} (y/n)?\n-->"))
               if "y" in confirm.lower():
                   db.execute("DELETE FROM agenda where ID=(?)", (entry,))
                   more = str(input("Delete more entries (y/n)?"))
                   if "y" not in more.lower():
                       boolean_for_loop = False

        elif choice == 3:
            with open('/home/garrett/schedule.txt', 'w') as f:
                for i in query_in_list:
                    f.write(f"{i[4]:15} {i[1]} {i[2]:10} {i[3]}\n")
            print("Exported table to home folder...")

        elif choice == 4:
            delete_the_agenda = str(input("Are you sure you want to delete the agenda? (y/n)"))
            if "y" in delete_the_agenda.lower():
                keep_status_unfinished = str(input("Would you like to keep all items without a status of 'Finished'?"))
                if "y" in keep_status_unfinished.lower():
                    all_unfinished_entries = db.query("SELECT * FROM agenda WHERE status != 'Finished'")
                db.execute("DELETE FROM agenda")
                db.create_table()
                db.commit()
                delete_id = -1
                for a in all_unfinished_entries:
                    delete_id +=1
                    db.execute("INSERT INTO agenda(ID, date, class, assignment, status) VALUES(?,?,?,?,?)",(delete_id, a[1], a[2], a[3], a[4]))
                db.commit()
                print("Database deleted")

def main():
    choice = int(input("""Choose one of the following options
1)  View by date.
2)  View by course.
3)  View by status.
4)  Edit the agenda.
5)  Manage the agenda.
99) Quit.
-->"""))
    
    if choice == 1:
        View(choice)
    elif choice == 2:
        View(choice)
    elif choice == 3:
        View(choice)
    elif choice == 4:
        Edit()
    elif choice == 5:
        Manage()
    elif choice == 99:
        Database().close()
    else:
        print("Not a proper input. Please try again.")
    input()
    main()

if __name__ == "__main__":
    main()
