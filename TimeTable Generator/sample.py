'''
Done :
1)Map Classes to the teacher say each teacher has n classes
2)Before alloting to subjects in assign_slots_to_each_sec() every time teachers table should be checked if there is no clash
3)Teachers TimeTable should be acc. to his/her constraints or a global Constraint should be defined for all teachers.
TODOS:
1)Handling openElectives
2)CAT LAB segmentations
'''

from flask import Flask, render_template, request, url_for, redirect
import sys
import sqlite3 as sql
import pandas as pd
import numpy as np
import os
import Controller

new_table_list = []

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("autotimetable.html")

@app.route("/trial")
def trial():
    return render_template("trial.html")

@app.route("/login")
def login_page():
    return render_template("login.html", msg="")


@app.route('/login_validation', methods=['POST', 'GET'])
def login_validation():
    valid = 0
    if request.method == 'POST':
        user = request.form['user_id']
        pswd = request.form['password']
        if user == 'abc' and pswd == 'xyz':
            valid = 1
    else:
        user = request.args.get('user_id')
        pswd = request.args.get('password')
        if user == 'abc' and pswd == 'xyz':
            valid = 1
    if valid:
        return redirect(url_for('entrypoint'))
    else:
        msg = "Wrong Credentials..Retry!!"
        return render_template('login.html', msg=msg)

@app.route("/index")
def entrypoint():               #create empty tables in database and open add section/teacher form
    try:
        database = Controller.DataBaseBuilder()
        database.createTeacherTable()
        database.createSectionTable()
        database.createRoomTable()
    except:
        msg = "There was some Error while table creation"
    finally:
        return render_template("index.html")
        #con.close()


@app.route("/section_entry", methods=['POST', 'GET'])
def section_details():
    if request.method == 'POST':
    #try:
        data = request.form
        database = Controller.DataBaseBuilder()
        msg=database.insertSectionDetailsFromPage(data)
    #except:
        #msg = "Failed to Insert"
    #finally:
        return render_template('result.html', msg=msg)


@app.route("/remove_section", methods=['POST', 'GET'])
def remove_section():
    try:
        data = request.form
        database=Controller.DataBaseBuilder()
        database.remove_section(data)
    except:
        msg = "Failed"
    finally:
        return redirect(url_for('display'))
        #con.close()



@app.route("/teacher_entry", methods=['POST', 'GET'])
def teacher_details():      #Inserting teacher details from form to database
    if request.method == 'POST':
        try:
            data = request.form
            database = Controller.DataBaseBuilder()
            msg = database.insertTeacherDetailsFromPage(data)

        except:
            msg = "Failed to Insert"
        finally:
            return render_template('result.html', msg=msg)
            #con.close()



@app.route("/remove_teacher", methods=['POST', 'GET'])
def remove_teacher():
    try:
        data = request.form
        database=Controller.DataBaseBuilder()
        database.remove_teacher(data)
    except:
        msg = "Failed"
    finally:
        return redirect(url_for('display'))
        #con.close()


@app.route("/room_entry", methods=['POST', 'GET'])
def room_details():  # Inserting room details from form to database
    if request.method == 'POST':
        try:
            data = request.form
            database = Controller.DataBaseBuilder()
            msg = database.insertRoomDetailsFromPage(data)

        except:
            msg = "Failed to Insert"
        finally:
            return render_template('result.html', msg=msg)
            # con.close()


@app.route("/remove_room", methods=['POST', 'GET'])
def remove_room():
    try:
        data = request.form
        database = Controller.DataBaseBuilder()
        database.remove_room(data)
    except sql.Error as e:
        msg = "Room deletion Failed"
        print(msg)
        print("Error: " +  str(e))
    finally:
        return redirect(url_for('display'))
        # con.close()


@app.route('/display')
def display():              # shows entries in Database
    try:
        database = Controller.DataBaseBuilder()
        rows1,rows2,rows3 = database.displayDatabase()

    except:
        msg = "Can't access database"
    finally:
        return render_template("display.html", rows1=rows1, rows2=rows2, rows3=rows3)
        #con.close()

'''
def assignTeachersToTheSubjects(Teachers,Sections):
    for section in Sections:
        secSubjects = [sub[0] for sub in section.subjects_with_credit]
        i = 0
        while i < len(secSubjects):
            for teacher in Teachers:
                if secSubjects[i] in teacher.subjects.keys() and section not in teacher.sectionsAlloted.keys() and teacher.canAssignSec:
                    if teacher.subjects[secSubjects[i]] != 0:
                        teacher.sectionsAlloted[section] = secSubjects[i]
                        section.teachersAlloted[secSubjects[i]] = teacher
                        teacher.classesAlloted += 1
                        teacher.subjects[secSubjects[i]] -= 1
                        if teacher.classesAlloted == Controller.constraints.maximumClassesToAllot or sum(teacher.subjects.values()) == 0:
                            teacher.canAssignSec = False
                        i+=1
                        break


# --------------------------------------------------------------------------------------------
#                         Check For teachers Constraint
# ---------------------------------------------------------------------------------------------

def validSlot(teacher,i,j): #for the constraint of continous classes
    if Controller.constraints.continousClass == 0:
        if j != 0 and j != 8:
            if teacher.teachers_table[i,j+1] == '' and teacher.teachers_table[i,j-1] == '':
                return True
        elif j == 0:
            if teacher.teachers_table[i,j+1] == '':
                return True
        else:
            if teacher.teachers_table[i,j-1] == '':
                return True
    return False

def check(teacher,section,i,j):
    if teacher.teachers_table[i,j] == '' and validSlot(teacher,i,j): #check if slot available
        print(teacher.name)
        teacher.teachers_table[i,j] = section.name + '(' + teacher.sectionsAlloted[section] + ')'
        return True
    return False

# --------------------------------------------------------------------------------------------
#                         GENERATING EXCEL
# ---------------------------------------------------------------------------------------------
def generateExcel(time_table,fname,name):
    global list_of_timetables  # will be used later while displaying the table

    days = ['MON', 'TUE', 'WED', 'THURS', 'FRI']
    period = ['8-9', '9-10', '10-11', '11-12', '12-1', '1-2', '3-4', '4-5', '5-6']
    time_table_sec1_formatted = pd.DataFrame(data=time_table, index=days, columns=period)
        #sec1.class_table = time_table_sec1_formatted
    list_of_timetables.append(time_table_sec1_formatted)
    for time in period:
        time_table_sec1_formatted[time] = time_table_sec1_formatted[time].replace([''], '-')

    print(time_table_sec1_formatted)
    if not os.path.isfile(fname):
        time_table_sec1_formatted.to_excel(fname, sheet_name=name)
    else:
        from openpyxl import load_workbook
        book = load_workbook(fname)
        writer = pd.ExcelWriter(fname, engine='openpyxl')
        writer.book = book
        time_table_sec1_formatted.to_excel(writer, sheet_name=name)
        writer.save()
        writer.close()



# --------------------------------------------------------------------------------------------
#                         GENERATING TIME - TABLE
# ---------------------------------------------------------------------------------------------


def assignNoClass(time_table_sec1,all_slots):
    random_numbers = np.random.randint(low=1, high=4, size=5)
    for i in range(5):
        if random_numbers[i] == 1:
            time_table_sec1[i][0] = time_table_sec1[i][1] = time_table_sec1[i][2] = 'No class'
            all_slots[i][0] = 3
        elif random_numbers[i] == 2:
            time_table_sec1[i][3] = time_table_sec1[i][4] = time_table_sec1[i][5] = 'No class'
            all_slots[i][1] = 3
        else:
            time_table_sec1[i][6] = time_table_sec1[i][7] = time_table_sec1[i][8] = 'No class'
            all_slots[i][2] = 3


def assignLabs(sec1,time_table_sec1,all_slots):
    count = 0
    slot = [0, 3, 6]
    lab_days = [0] * 5
    # Assigning Labs
    while count < len(sec1.labs):
        i = np.random.randint(0, 5)  # Choose random day
        j = np.random.randint(0, 3)  # Choose random slot out of 3 slots
        if time_table_sec1[i][slot[j]] != 'No class' and lab_days[
            i] != 1:  # That slot should be available and no other labs should have been taken that day
            lab_days[i] = 1
            time_table_sec1[i][slot[j]] = time_table_sec1[i][slot[j] + 1] = time_table_sec1[i][slot[j] + 2] = sec1.labs[
                count]
            all_slots[i][j] = 3  # Representing all 3 periods of that slot is full
            count = count + 1

def assign_slots_to_each_sec(Sections,Teachers):
    global list_of_sec_names  # will be used later while displaying the table
    list_of_sec_names = []  # will be used later while displaying the table
    global list_of_timetables  # will be used later while displaying the table
    list_of_timetables = []  # will be used later while displaying the table
    for sec1 in Sections:
        list_of_sec_names.append(sec1.name)  # to be used later to display the tables
        all_slots = np.zeros((5, 3),dtype = "int32")
        time_table_sec1 = np.zeros((5, 9), dtype="S10")
        time_table_sec1=assignNoClass(time_table_sec1,all_slots)
        time_table_sec1=assignLabs(sec1,time_table_sec1,all_slots)
        slot = [0, 3, 6]
        total_credits = 0
        sec1_subjects = []
        available_slots = 45 - (5*3 + len(sec1.labs)*3)
        for i in range(len(sec1.subjects_with_credit)):
            total_credits = total_credits + sec1.subjects_with_credit[i][1]


        if total_credits > available_slots: #if not enogh slots
            print("Total credits : ", total_credits)
            print('Available Slots : ',available_slots)
            print('Not enough slots')
            continue

        count = 0
        days = np.random.choice(range(5),5,replace = False)
        sec1_subjects_temp = sec1.subjects_with_credit
        for i in days:
            js = [j for j in range(3) if all_slots[i][j] == 0] #get all empty slots for that day
            at = 0
            while all_slots[i][js[0]] != 3 and at < 10 and len(sec1_subjects_temp) != 0:
                at += 1#maximum 10 attempts as dataset is small later maybe 50.!
                if sec1_subjects_temp[count][0] not in time_table_sec1[i]: # avoid repetition
                    teacher = sec1.teachersAlloted[sec1_subjects_temp[count][0]]
                    if check(teacher,sec1,i,(slot[js[0]] + all_slots[i][js[0]])):  #check if teacher can allow that class
                        time_table_sec1[i][slot[js[0]]+all_slots[i][js[0]]] = sec1_subjects_temp[count][0]
                        at = 0
                        sec1_subjects_temp[count][1] -= 1
                        if sec1_subjects_temp[count][1] == 0: # remove the subject once class assigned
                            del sec1_subjects_temp[count]
                        all_slots[i][js[0]] += 1
                if len(sec1_subjects_temp) != 0:
                    count = (count + 1) % len(sec1_subjects_temp)
            if len(js) == 2 and len(sec1_subjects_temp) != 0: #if there are two slots and  we have atleast one subject available
                count = (count + 1) % len(sec1_subjects_temp)
                while all_slots[i][js[1]] != 3 and at < 10:
                    at += 1
                    if sec1_subjects_temp[count][0] not in time_table_sec1[i]:
                        teacher = sec1.teachersAlloted[sec1_subjects_temp[count][0]]
                        if check(teacher,sec1,i,(slot[js[1]] + all_slots[i][js[1]])):
                            time_table_sec1[i][slot[js[1]]+all_slots[i][js[1]]] = sec1_subjects_temp[count][0]
                            at = 0
                            sec1_subjects_temp[count][1] -= 1
                            if sec1_subjects_temp[count][1] == 0:
                                del sec1_subjects_temp[count]
                            all_slots[i][js[1]] += 1
                    if len(sec1_subjects_temp) != 0:
                        count = (count + 1) % len(sec1_subjects_temp)

            if len(sec1_subjects_temp) == 0:
                break
        generateExcel(time_table_sec1,"section_timetable.xlsx",sec1.name)

    for teacher in Teachers:
        list_of_sec_names.append(teacher.name)  # will be used later while displaying the table
        generateExcel(teacher.teachers_table,"teacher_timetable.xlsx",teacher.name)


'''
@app.route('/generate')
def generate():
    global new_table_list
# try:
    controller = Controller.timetableGenerator()
    while (True):        
        controller.loadDB()
        controller.assignTeacherstoSections()
        if (controller.build_timeTable()):
            # controller.printDetails()
            break
    new_table_list = controller.generateExcel()

    msg = "TimeTable generated successfully in Excel file"
# except:
#     msg = "Failed to generate time-table"

# finally:
    return render_template('generate.html', msg=msg)
    #con.close()

@app.route('/table')
def table():
    global new_table_list
    #print(new_table_list)
    htm = "<br>"

    for name, table in new_table_list:
        htm = htm + "<h2>" + name + "</h2>" + table.to_html(header="true") + "<br><br>"

    htm = "<u><center><h1>Time Table</h1><center></u>" + htm + "<form action='/index'><button>Home Page</button></form>"
    return htm


if __name__ == "__main__":
    app.run(debug=True)
