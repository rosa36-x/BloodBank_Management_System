#!/usr/bin/env python
# coding: utf-8

# In[5]:


from datetime import datetime
from datetime import timedelta
from tabulate import tabulate
import getpass
import re
import csv
import uuid
import mysql.connector as mys
con=mys.connect(host="localhost",user="root",password="",database="bloodbank")
cur=con.cursor()
def main():
    print("*"*60)
    print()
    print("BLOODBANK")
    print()
    print("*"*60)
    print()
    print("Welcome to the login system.")
    print("1. Register")
    print("2. Login")
    c = input("Enter your choice: ")
    print()
    print("*"*60)
    if c == "1":
        register()
    elif c == "2":
        login()
    else:
        print("Invalid choice. Please try again.")
        main()
        
        
        
def pro():
    with open('bloodusers.csv','r')as f: 
        r = csv.reader(f)
        print("Please enter your login details.")
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        success=False
        for i in r: 
            if(i[0]==username and i[1]==password):
                success=True
        if(success==True):
            print("Login successful.")
        else:
            print("Invalid.")
            login()
            
            
            
def register():
    print("Please enter your details to register.")
    with open("bloodusers.csv","a",newline="") as f:
        w=csv.writer(f)
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        w.writerow([username,password])
    
    
    print("Registration successful.")
    print("Enter details to finish setting up account:")
    name = input('Please enter your name: ')
    DOB = input('Please enter your date of birth (yyyy-mm-dd): ')
    valid_blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    while True:
        blood_grp = input('Please enter your blood group: ')
        if blood_grp.upper() in valid_blood_groups:
            break
        else:
            print("Invalid blood group. Please try again.")
    gender = input('Please enter your gender (M/F/O): ')
    t="MmFfOo"
    while gender not in t:
        print("Invalid. Try again.")
        gender=input("Please enter your gender (M/F/O):")
    
    email = input('Please enter your email address: ')
    k=0
    
    while k==0:
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if re.fullmatch(regex, email):
            k=1
        else:
            k=0
            print("Invalid email id.")
            email = input('Please enter your email address: ')
    phone_no = input('Please enter your phone number: ')
    while len(phone_no)!=10:
        print("Invalid phone number.")
        phone_no = input('Please enter your phone number: ')
    address = input('Please enter your address: ')
    sql = "INSERT INTO reg(username, password, name,gender, DOB, blood_grp, phone_no,email, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (username, password, name,gender, DOB, blood_grp, phone_no,email, address)
    cur.execute(sql, val)
    con.commit()
    
    main()
    

            
def login():
    print()
    print("*"*60)
    print()
    print("Welcome to the login system.")
    print("1. Admin")
    print("2. General")
    l=int(input("Enter your choice:"))
    if l==1:
        pro()
        print()
        print("1. View")
        print("2. Edit")
        b=int(input("Enter your choice:"))
        if b==1:
            print()
            print("View database")
            print("1. Registeration details")
            print("2. Donor info")
            print("3. Patient info")
            print("4. Blood availability")
            o=int(input("Enter choice:"))
            if o==1:
                print()
                print("Registeration details")
                num=int(input("Enter number of records to be fetched: "))
                quer="select username, name,gender, cast(DOB as char), blood_grp, phone_no,email, address from reg"
                cur.execute(quer)
                data=cur.fetchmany(num)
                print(tabulate(data, headers=['Username', 'Name','Gender','DOB','Blood_grp','Phone_no','Email','Address'], tablefmt='psql'))
                
                login()
            
            elif o==2:
                print()
                print("Donor records")
                num=int(input("Enter number of records to be fetched: "))
                cur.execute("Select username, donor_ID, cast(unit_l as char), blood_grp, cast(appointment_date as char) from donor")
                data=cur.fetchmany(num)
                print(tabulate(data, headers=['Username', 'Donor_ID','Unit_l','Blood_grp','Appointment_Date'], tablefmt='psql'))
                login()
            elif o==3:
                print()
                print("Patient records")
                num=int(input("Enter number of records to be fetched: "))
                cur.execute("Select username, patient_ID, cast(unit_l as char), blood_grp, cast(appointment_date as char) from patient")
                data=cur.fetchmany(num)
                print(tabulate(data, headers=['Username', 'Patient_ID','Unit_l','Blood_grp','Appointment_Date'], tablefmt='psql'))
                
                login()
            elif o==4:
                print()
                print("Blood availability")
                print("Total:")
                cur.execute("SELECT CAST(SUM(unit_l) AS CHAR) FROM donor")
                total_donated = cur.fetchone()[0]
                print("Total litres of blood to be donated:", total_donated)
                cur.execute("SELECT CAST(SUM(unit_l)AS CHAR) FROM patient")
                total_received = cur.fetchone()[0]
                print("Total litres of blood to be received:", total_received)
                
                print("Group-wise:")
                don="SELECT  blood_grp, CAST(SUM(unit_l) AS CHAR) FROM donor group by blood_grp"
                cur.execute(don)
                total_donated = cur.fetchall()
                print("Total litres of blood to be donated :")
                print(tabulate(total_donated, headers=['Blood_grp','Unit_l'], tablefmt='psql'))
            
                pat="SELECT blood_grp, CAST(SUM(unit_l) AS CHAR) FROM patient group by blood_grp"
                cur.execute(pat)
                total_received = cur.fetchall()
                print("Total litres of blood to be received :")
                print(tabulate(total_received, headers=['Blood_grp','Unit_l'], tablefmt='psql'))
               
                    
                
                login()
    
            else:
                print("Invalid choice")
                login()     
        elif b==2:
            print()
            print("Edit database")
            print("1. To delete records")
            print("2. To view specific records")
            p=int(input("Enter choice: "))
            if p==1:
                print()
                print("1. Delete patient record")
                print("2. Delete donor record")
                d=int(input())
                if d==1:
                    e=input("Enter patient ID: ")
                    view="Select username, patient_ID, cast(unit_l as char),reason, blood_grp, cast(appointment_date as char) from patient where patient_ID= '"+str(e)+"'"
                    cur.execute(view)
                    data=cur.fetchall()
                    print(tabulate(data, headers=['Username', 'Patient_ID','Unit_l','Blood_grp','Appointment_Date'], tablefmt='psql'))
                    delete = "DELETE FROM patient WHERE patient_ID ='"+str(e)+"'"
                if d==2:
                    e=input("Enter donor ID: ")
                    view = "Select username, donor_ID, cast(unit_l as char),disease, blood_grp, cast(appointment_date as char) from donor where donor_ID= '"+str(e)+"'"
                    cur.execute(view)
                    data=cur.fetchall()
                    print(tabulate(data, headers=['Username', 'Donor_ID','Unit_l','Blood_grp','Appointment_Date'], tablefmt='psql'))
                    delete = "DELETE FROM donor WHERE donor_ID ='"+str(e)+"'"
                if cur:
                    f=input("Are you sure you want to delete this record(y/n)? ")
                    if f=="y" or "Y":
                        cur.execute(delete)
                        con.commit()
                        con.close()
                        print(cur.rowcount, "record(s) deleted")
                    elif f=="n" or "N":
                        print("The record was not deleted")
                    else:
                        print("Invalid Choice!!")
                login()
            
            elif p==2:
                print()
                print("1. View patient record")
                print("2. View donor record")
                d=int(input())
                if d==1:
                    e=input("Enter patient ID: ")
                    view="Select username, patient_ID, cast(unit_l as char),reason, blood_grp, cast(appointment_date as char) from patient where patient_ID= '"+str(e)+"'"
                    cur.execute(view)
                    data=cur.fetchall()
                    print(tabulate(data, headers=['Username', 'Patient_ID','Unit_l','Reason','Blood_grp','Appointment_Date'], tablefmt='psql'))
                    
                    con.close()
                elif d==2:
                    e=input("Enter donor ID: ")
                    view = "Select username, donor_ID, cast(unit_l as char),disease, blood_grp, cast(appointment_date as char) from donor where donor_ID= '"+str(e)+"'"
                    cur.execute(view)
                    data=cur.fetchall()
                    print(tabulate(data, headers=['Username', 'Donor_ID','Unit_l','Disease','Blood_grp','Appointment_Date'], tablefmt='psql'))
                   
                    con.close()
                else:
                    print("Invalid Choice!!")
                login()
            
           
            
        else:
            print("invalid")
        
        
    elif l==2:
        pro()
        print()
        print("1. Donate")
        print("2. Request")
        print("3. Change details")
        dor=int(input("Enter your choice:"))
        if dor==1:
            print()
            print("DONATE")
            
            print("Enter y for yes and n for no:")
            q=input("Are you at least 18 yrs old?")
            if q=='y' or q=='Y':
                a=input("Have you visited the dentist for a minor procedure in the last 24hrs?")
                if a=='n' or a=='N':
                    a=input("Have you suffered from cough,cold,etc. in the past 4 weeks?")
                    if a=='n' or a=='N':
                        print("You have met the basic requirements however this is just a preliminary evaluation.")
                        print("Kindly get a complete medical evaluation including blood and urine tests to find out if you are eligible for donation.")
                        print("These documents must be submitted before donating blood.")
                        
                    elif a=='y' or a=='Y':
                        print("You are not eligible")
                        login()
                       
                    else:
                        print("Enter a valid character.")
                elif a=='y' or a=='Y':
                    print("You are not eligible")
                    login()
                    
                else:
                    print("Enter a valid character.")
            else:
                print("You must be at least 18 yrs old.")
                login()
                
                
            print("Your donor ID is "+ str(uuid.uuid4 ())[0:4])
            print("Enter the necessary details:")
            username=input("Enter username: ")
            donor_ID = input('Please enter your donor ID: ')
            unit_l = float(input('Please enter the units (litres) of blood you are donating: '))
            while unit_l > 0.470:
                print("Quantity too large.")
                unit_l = float(input('Please enter the units (litres) of blood you are donating: '))
            disease = input('Please enter any relevant medical conditions or diseases: ')
            valid_blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
            while True:
                blood_grp = input('Please enter your blood group: ')
                if blood_grp.upper() in valid_blood_groups:
                    break
                else:
                    print("Invalid blood group. Please try again.")
            today = datetime.today()
            print("Today's date:", today)
            appointd = today + timedelta(days=7)
            print("Visit the nearest hospital on:")
            print(appointd)
            sql = "INSERT INTO donor (username,donor_ID, unit_l,disease, blood_grp,appointment_date) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (username,donor_ID,unit_l, disease, blood_grp, appointd)
            cur.execute(sql, val)
            con.commit()
            con.close()
            print('Your details have been successfully saved to the database!')
            login()
            
        elif dor==2:
            print()
            print("REQUEST")
            print("Your patient ID is "+ str(uuid.uuid4 ())[0:4])
            print("Enter the necessary details:")
            username=input("Enter username: ")
            patient_ID = input('Please enter your Patient ID: ')
            unit_l = float(input('Please enter the amount of blood to be received: '))
            reason = input('Please enter the reason for your blood request: ')
            valid_blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
            while True:
                blood_grp = input('Please enter your blood group: ')
                if blood_grp.upper() in valid_blood_groups:
                    break
                else:
                    print("Invalid blood group. Please try again.")
            today="%Y-%m-%d"
            today = datetime.today()
            print("Today's date:", today)
            appointd = today + timedelta(days=7)
            print("Visit the nearest hospital on:")
            print(appointd)
            sql = "INSERT INTO patient (username, patient_ID, unit_l, reason, blood_grp, appointment_date) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (username, patient_ID, unit_l, reason, blood_grp, appointd)
            cur.execute(sql, val)
            con.commit()
            con.close()
            print('Your details have been successfully saved to the database!')
            print("The patient should be ready for transfusion prior to picking up blood from the blood bank.","\n"," eg appropriate IV access, consent completed, pre-medication administered if required.")
            print("Neccessary blood reports, prescriptions, consent form and doctor's approval letter should be submitted.")
            login()
            
        elif dor==3:
            print()
            print("CHANGE DETAILS")
            user=input("Enter your username: ")
            sv="select username, name,gender, cast(DOB as char), blood_grp, phone_no,email, address from reg where username= '"+str(user)+"'"
            cur.execute(sv)
            data=cur.fetchall()
            print(tabulate(data, headers=['Username', 'Name','Gender','DOB','Blood_grp','Phone_no','Email','Address'], tablefmt='psql'))
            
            print("These are your current details, do you wish to make changes? Y/ N")
            an=input()
            if an=="Y" or an== "y":
                print("1. Change phone number")
                print("2. Change email id")
                print("3. Change address")
                n=int(input("Enter your choice: "))
                if n==1:
                    user = input("Enter username: ")
                    ph_no = input("Enter the new phone number: ")
                    s = """UPDATE reg SET phone_no = %s WHERE username= %s """
                    try:
                        cur.execute(s, (ph_no, user))
                        con.commit()
                        con.close()
                        print("Details updated successfully!")
                    except mysql.connector.Error as error:
                                    print("Error updating details: {}".format(error))

                elif n==2:
                    user = input("Enter username: ")
                    em = input("Enter the new email address: ")
                    s = """UPDATE reg SET email = %s WHERE username= %s """
                    try:
                        cur.execute(s, (em, user))
                        con.commit()
                        con.close()
                        print("Details updated successfully!")
                    except mysql.connector.Error as error:
                                    print("Error updating details: {}".format(error))
                elif n==3:
                    user = input("Enter username: ")
                    ad = input("Enter the new address: ")
                    s = """UPDATE reg SET address = %s WHERE username= %s """
                    try:
                        cur.execute(s, (ad, user))
                        con.commit()
                        con.close()
                        print("Details updated successfully!")
                    except mysql.connector.Error as error:
                                    print("Error updating details: {}".format(error))
                    
                else:
                    print("Invalid choice.")
            
        else:
            print("Enter a valid choice.")
main()      






