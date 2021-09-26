#---------SQLPLUS CONNECTION-----------
import cx_Oracle
dsn = cx_Oracle.makedsn('localhost','1521',service_name='orcl')
conn = cx_Oracle.connect(user='XDB',password='tiger',dsn=dsn)
cursor = conn.cursor()
#--------------------------------------

#---------FLASK INTEGRATION-----------
from flask import Flask,redirect,url_for,render_template,request,session,flash,send_file
from flask import json
app = Flask(__name__)
app.secret_key="MIT"
#----------------------------------------

#-----------FILE HANDLING------------
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "C:\\Users\Tanya\Desktop\VISFORCE"
ALLOWED_EXTENSIONS = {'csv'}


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

uploadedTAfiles=[]
uploadedPSfiles=[]
#------------------------------------

#------------FUNCTIONS-----------------------
from datetime import date
def getmonth(x):
    if x=="01":
        return "JAN"
    elif x=="02":
        return "FEB"
    elif x=="03":
        return "MAR"
    elif x=="04":
        return "APR"
    elif x=="05":
        return "MAY"
    elif x=="06":
        return "JUN"
    elif x=="07":
        return "JUL"
    elif x=="08":
        return "AUG"
    elif x=="09":
        return "SEP"
    elif x=="10":
        return "OCT"
    elif x=="11":
        return "NOV"
    elif x=="12":
        return "DEC"

    
def gethour(x):
    if int(x[0:2])>12:
        y=int(x[0:2])-12
        y=str(y)+x[2:]
        y=y+" pm"
        print("yinside=",y)
        return y
    else:
        if x[0:2]=='00':
            x[0:2]='12'
        x=x+" am"
        return x


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#------------CLASSES--------------------------
class User:
    def __init__(self,usertype,id,password):
        self.usertype=usertype
        self.id=id
        self.password=password

class Leave:
    def __init__(self,leaveid,dol,dor,reason,status,time,emp_id,name,department,admin_id):
        self.leaveid=leaveid
        self.dateofleave=dol
        self.dateofreturn=dor
        self.reason=reason
        self.status=status
        self.time=time
        self.emp_id=emp_id
        self.name=name
        self.department=department
        self.admin_id=admin_id

class Feedback:
    def __init__(self,feedbackid,dateofposting,timeofposting,message,comment,emp_id,admin_id):
        self.feedbackid=feedbackid
        self.dateofposting=dateofposting
        self.timeofposting=timeofposting
        self.message=message
        self.comment=comment
        self.emp_id=emp_id
        self.admin_id=admin_id

class Employee:
    def __init__(self,emp_id,phone,email,name,dob,department,admin_id,password):
        self.emp_id=emp_id
        self.phone=phone
        self.email=email
        self.name=name
        self.dob=dob
        self.department=department
        self.admin_id=admin_id
        self.password=password

class Announcement:
    def __init__(self,announcementid,dateofposting,timeofposting,message,admin_id,title):
        self.announcementid=announcementid
        self.dateofposting=dateofposting
        self.timeofposting=timeofposting
        self.message=message
        self.admin_id=admin_id
        self.title=title


##cursor.execute("""truncate table targetaudience_phone_visforce""")
##cursor.execute("""truncate table targetaudience_main_visforce""")
##cursor.execute("""commit""")
##cursor.execute("""truncate table pastsales_visforce""")
##cursor.execute("""commit""")
class Target_Audience:
    def __init__(self,serialno,name,phone,email,salary,location,gender,address,dob,age):
        self.serialno=serialno
        self.name=name
        self.phone=phone
        self.email=email
        self.salary=salary
        self.location=location
        self.gender=gender
        self.address=address
        self.dob=dob
        self.age=age

class Past_Sales:
    def __init__(self,dateofsale,buyername,address,product,orderid,price,status):
        self.dateofsale=dateofsale
        self.buyername=buyername
        self.address=address
        self.product=product
        self.orderid=orderid
        self.price=price
        self.status=status
    

#---------------------------------------------------------
@app.route('/download')
def download_file():
	#path = "html2pdf.pdf"
	#path = "info.xlsx"
	path = "mailinglistTA.txt"
	#path = "sample.txt"
	return send_file(path, as_attachment=True)
        
#---------------------------------------------------------
        
        
@app.route("/login",methods=["POST","GET"])
def login():
    if "id" in session and "usertype" in session:
        if session["usertype"]=='Admin':
            return redirect(url_for('admindashboard'))
        if session["usertype"]=='Employee':
            return redirect(url_for('empdashboard'))

    
    if request.method=="POST":
        input_usertype=request.form["usertype"]
        input_id=request.form["id"]
        input_password=request.form["password"]


        if input_id=="" or input_password=="":
            flash("Please complete the form","info")
            return render_template("login.html")

        
        if input_usertype=='Admin':
            cursor.execute("""select admin_id,password from admin_login_visforce where admin_id=:id""",[input_id])

        elif input_usertype=='Employee':
            cursor.execute("""SELECT emp_id,password FROM employee_login_visforce WHERE emp_id = :id""", [input_id])
        result = cursor.fetchall()
        print (result)

        if result:
            u=User(input_usertype,result[0][0],result[0][1])
            
            if input_password==u.password and u.usertype=='Admin':
                session["id"]=u.id
                session["usertype"]=u.usertype
                print("going to admindashboard")
                return redirect(url_for('admindashboard'))
        
            elif input_password==u.password and u.usertype=='Employee':
                session["id"]=u.id
                session["usertype"]=u.usertype
                print("going to employeedashboard")
                return redirect(url_for('empdashboard'))
            
            else:
                print ("password incorrect")
                flash("The password is incorrect","info")
                return render_template("login.html")
        else:
            flash("The username or usertype is incorrect","info")
            return render_template("login.html")



    else:
        return render_template("login.html")



@app.route("/admindashboard",methods=["POST","GET"])
def admindashboard():

    #-----------ACCESS RESTRICTIONS--------------
    if "id" in session and "usertype" in session:
        if session["usertype"]=='Admin':
            admin_id=session["id"]
            usertype=session["usertype"]
            print(admin_id,"has logged in")
        else:
            flash("Please login first")
            return redirect(url_for('login'))
    else:
        flash("Please login first")
        return redirect(url_for('login'))
    #---------------------------------------------

    return render_template("admindashboard.html",admin_id=admin_id)
    

@app.route("/empdashboard",methods=["POST","GET"])
def empdashboard():
    #--------ACCESS FEEDBACKS-----------------
    if "id" in session and "usertype" in session:
        if session["usertype"]=='Employee':
            emp_id=session["id"]
            usertype=session["usertype"]
        else:
            flash("Please login first")
            return redirect(url_for('login'))
            
    else:
        flash("Please login first")
        return redirect(url_for('login'))
    #-------------------------------------------
    cursor.execute("""select name from employee_phone_visforce where emp_id=:x1""",[emp_id])
    result=cursor.fetchall()
    user=[emp_id,result[0][0]]

    return render_template("empdashboard.html",user=user)












    
#-------------ADMIN SECTION--------------------------

@app.route("/seeleaverequests",methods=["POST","GET"])
def seeleaverequests():
    if request.method=="POST":
        #-----------ACCESS RESTRICTIONS--------------
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Admin':
                admin_id=session["id"]
                usertype=session["usertype"]
                print(admin_id,"has logged in")
            else:
                flash("Please login first")
                return redirect(url_for('login'))
        else:
            flash("Please login first")
            return redirect(url_for('login'))
        #---------------------------------------------
        
        querytabs=[None,None,None,""]
        info=[]

        try:
            status=request.form["status"]
            input_dateofleave=request.form["dateofleave"]
            input_dateofreturn=request.form["dateofreturn"]
            input_searchbox=request.form["searchbox"]
            #SAVING DATES FOR HTML FORMATS
            htmldate1=input_dateofleave
            htmldate2=input_dateofreturn
            #CHANGING DATE FORMATS
            if input_dateofleave:
                input_dateofleave=input_dateofleave[-2:]+"-"+getmonth(input_dateofleave[5:7])+"-"+input_dateofleave[2:4]
            if input_dateofreturn:
                input_dateofreturn=input_dateofreturn[-2:]+"-"+getmonth(input_dateofreturn[5:7])+"-"+input_dateofreturn[2:4]
            if input_searchbox==0:
                input_searchbox=""
            else:
                searchbox="%"+input_searchbox+"%"
              
            cursor.execute("""create or replace view temp1 as select leave_id,to_char(date_of_leave) dol,to_char(date_of_return) dor,reason,status,to_char(time_applied) time,leave_visforce.emp_id,name,department,admin_id from leave_visforce inner join employee_phone_visforce on leave_visforce.emp_id=employee_phone_visforce.emp_id""")
            cursor.execute("""commit""")
            
            if status=="pen":
                querytabs[0]=status
                
                cursor.execute("""create or replace view temp2 as select * from temp1 where status in ('PEN')""")
                cursor.execute("""commit""")
            elif status=="acc":
                querytabs[0]=status
                
                cursor.execute("""create or replace view temp2 as select * from temp1 where status in ('ACC')""")
                cursor.execute("""commit""")
            elif status=="rej":
                querytabs[0]=status
                
                cursor.execute("""create or replace view temp2 as select * from temp1 where status in ('REJ')""")
                cursor.execute("""commit""")
            elif status=="all":
                querytabs[0]=status
                
                cursor.execute("""create or replace view temp2 as select * from temp1 """)
                cursor.execute("""commit""")
            else:
                cursor.execute("""create or replace view temp2 as select * from temp1""")
                cursor.execute("""commit""")
            
            cursor.execute("""select * from temp2""")  
            result1=cursor.fetchall()
            result2=result1
            result3=result1
            
            
            if input_dateofleave:
                querytabs[1]=htmldate1
                cursor.execute("""select * from temp2 where Dol=:x1""", [input_dateofleave])
                result1 = cursor.fetchall()
                
                
            if input_dateofreturn:
                querytabs[2]=htmldate2
                cursor.execute("""select * from temp2 where Dor=:x1""", [input_dateofreturn])
                result2 = cursor.fetchall()

                
            if input_searchbox:
                querytabs[3]=input_searchbox
                cursor.execute("""select * from temp2 where upper(name) like upper(:x1) or upper(department) like upper(:x2) or upper(emp_id) like upper(:x3)""", [searchbox,searchbox,searchbox])
                result3 = cursor.fetchall()



            result = list(set(result1) & set(result2) & set(result3))

            for i in range(0,len(result)):         
                info.append(Leave(result[i][0],result[i][1],result[i][2],result[i][3],result[i][4],(result[i][5])[10:18]+(result[i][5])[-3:],result[i][6],result[i][7],result[i][8],result[i][9]))
            for i in info:
                print(i.dateofleave,i.dateofreturn,i.name,i.time)
            cursor.execute("""drop view temp1""")
            cursor.execute("""drop view temp2""")
            cursor.execute("""commit""")        
            return render_template("seeleaverequests.html",info=info,querytabs=querytabs,admin_id=admin_id)
        except:
            print ("we did not query")
    
            

        try:
            statuschange=request.form["statuschange"]
            leaveid=request.form["leaveid"]
            cursor.execute("""update leave_visforce set status=upper(:x1) where leave_id=:x2""",[statuschange,leaveid])
            cursor.execute("""commit""")
            cursor.execute("""create or replace view temp as select leave_id,to_char(date_of_leave) dol,to_char(date_of_return) dor,reason,status,to_char(time_applied) time,leave_visforce.emp_id,name,department,admin_id from leave_visforce inner join employee_phone_visforce on leave_visforce.emp_id=employee_phone_visforce.emp_id""")
            cursor.execute("""commit""")
            cursor.execute("""SELECT * FROM temp WHERE status in ('PEN') order by dol,time desc""")
            result = cursor.fetchall()
            info=[]
            querytabs=["pen",None,None,""]
            for i in range(0,len(result)):         
                info.append(Leave(result[i][0],result[i][1],result[i][2],result[i][3],result[i][4],(result[i][5])[10:18],result[i][6],result[i][7],result[i][8],result[i][9]))
            cursor.execute("""drop view temp""")
            cursor.execute("""commit""")  
            return render_template("seeleaverequests.html",info=info,querytabs=querytabs,admin_id=admin_id)
        except:
            print ("we did not have any change in status")
   
    else:
        #-----------ACCESS RESTRICTIONS--------------
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Admin':
                admin_id=session["id"]
                usertype=session["usertype"]
                print(admin_id,"has logged in")
            else:
                flash("Please login first")
                return redirect(url_for('login'))
        else:
            flash("Please login first")
            return redirect(url_for('login'))
        #---------------------------------------------
        cursor.execute("""create or replace view temp as select leave_id,to_char(date_of_leave) dol,to_char(date_of_return) dor,reason,status,to_char(time_applied) time,leave_visforce.emp_id,name,department,admin_id from leave_visforce inner join employee_phone_visforce on leave_visforce.emp_id=employee_phone_visforce.emp_id""")
        cursor.execute("""commit""")
        cursor.execute("""SELECT * FROM temp order by dol,time desc""")
        result = cursor.fetchall()
        print("results,get=",result)
        info=[]
        querytabs=["all",None,None,""]
        for i in range(0,len(result)):         
            info.append(Leave(result[i][0],result[i][1],result[i][2],result[i][3],result[i][4],(result[i][5])[10:18]+(result[i][5])[-3:],result[i][6],result[i][7],result[i][8],result[i][9]))
        print("get seeleaverequests querytabs=",querytabs)
        print ("info get seeleaverequests=")
        for i in info:
            print(type(i.dateofleave),i.dateofreturn,i.name,type(i.time))
        cursor.execute("""drop view temp""")
        cursor.execute("""commit""")  
        return render_template("seeleaverequests.html",info=info,querytabs=querytabs,admin_id=admin_id)#info is a list of objects AND pending checkbox will be checked


@app.route("/seefeedback",methods=["POST","GET"])
def seefeedback():
    if request.method=="POST":

        
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Admin':
                admin_id=session["id"]
                usertype=session["usertype"]
            else:
                flash("Please login first")
                return redirect(url_for('login'))
        else:
            flash("Please login first")


        import datetime
        from datetime import date
        today=date.today()
        date=today.strftime("%Y-%m-%d")
        querytabs=[None,"all"]
        info=[]
        
        try:#query
            input_date=request.form["date"]
            input_status=request.form["status"]
            cursor.execute("""create or replace view temp as select feedback_id,to_char(date_of_posting) dop,to_char(time_of_posting) time,feedback_message,admin_comment,admin_id from feedback_visforce""")
            cursor.execute("""commit""")
            
            if input_date:
                print("date given")
                htmldate=input_date
                input_date=input_date[-2:]+"-"+getmonth(input_date[5:7])+"-"+input_date[2:4]
                querytabs[0]=htmldate
                if input_status=="com":
                    querytabs[1]="com"
                    cursor.execute("""select * from temp where dop=:x1  and admin_comment is not null""",[input_date])
                    result = cursor.fetchall()
                elif input_status=="uncom":
                    querytabs[1]="uncom"
                    cursor.execute("""select * from temp where dop=:x1 and  and admin_comment is null""",[input_date])
                    result = cursor.fetchall()
                elif input_status=="all":
                    querytabs[1]="all"
                    cursor.execute("""select * from temp where dop=:x1""",[input_date])
                    result = cursor.fetchall()
            else:
                print("no date given")
                if input_status=="com":
                    querytabs[1]="com"
                    cursor.execute("""select * from temp where admin_comment is not null""")
                    result = cursor.fetchall()
                elif input_status=="uncom":
                    querytabs[1]="uncom"
                    cursor.execute("""select * from temp where admin_comment is null""")
                    result = cursor.fetchall()
                elif input_status=="all":
                    querytabs[1]="all"
                    cursor.execute("""select * from temp""")
                    result = cursor.fetchall()

            print(querytabs)
            for i in range(0,len(result)):
                info.append(Feedback(result[i][0],result[i][1],(result[i][2])[10:18]+(result[i][2])[-3:],result[i][3],result[i][4],None,result[i][5]))
            cursor.execute("""drop view temp""")
            cursor.execute("""commit""")

            return render_template("seefeedback.html",info=info,querytabs=querytabs,admin_id=admin_id)
        
                
        except:
            print("input_date never existed")


        try:#comment
            print("we see the comment added")
            input_comment=request.form["comment"]
            print("we see the comment added")
            input_feedbackid=request.form["feedbackid"]
            print("we see the comment added")
            cursor.execute("""update feedback_visforce set admin_comment=:x1,admin_id=:x2 where feedback_id=:x3""",[input_comment,session["id"],input_feedbackid])
            cursor.execute("""commit""")
            print("we see the comment added")
            flash("comment added")
            return redirect(url_for('seefeedback'))
        
        except:
            print("there was no comment ever added")


        
        
    else:
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Admin':
                admin_id=session["id"]
                usertype=session["usertype"]
     
            else:
                flash("Please login first")
                return redirect(url_for('login'))

        else:#get
            flash("Please login first")
            return redirect(url_for('login'))

        cursor.execute("""create or replace view temp as select feedback_id,to_char(date_of_posting) dop,to_char(time_of_posting) time,feedback_message,admin_comment,admin_id from feedback_visforce""")
        cursor.execute("""commit""")
        cursor.execute("""SELECT * FROM temp order by dop,time desc""")
        result = cursor.fetchall()
    
        info=[]
        
        import datetime
        from datetime import date
        today=date.today()
        date=today.strftime("%Y-%m-%d")
        querytabs=[None,"all"]
        
        for i in range(0,len(result)):         
            info.append(Feedback(result[i][0],result[i][1],(result[i][2])[10:18]+(result[i][2])[-3:],result[i][3],result[i][4],None,result[i][5]))
                                 
        cursor.execute("""drop view temp""")
        cursor.execute("""commit""")  
        return render_template("seefeedback.html",info=info,querytabs=querytabs,admin_id=admin_id)




@app.route("/myemployees",methods=["POST","GET"])
def myemployees():
    if request.method=="POST":
        #-----------ACCESS RESTRICTIONS--------------
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Admin':
                admin_id=session["id"]
                usertype=session["usertype"]
            else:
                flash("Please login first")
                return redirect(url_for('login'))
        else:
            flash("Please login first")
            return redirect(url_for('login'))
        #---------------------------------------------
        try:#we are trying to query
            print("oldleaf")
            input_department=request.form["department"]
            input_searchbox=request.form["searchbox"]
            cursor.execute("""create or replace view temp as select employee_phone_visforce.emp_id,employee_phone_visforce.phone,email,name,dob,department from employee_main_visforce inner join employee_phone_visforce on employee_main_visforce.emp_id=employee_phone_visforce.emp_id""")
            cursor.execute("""commit""")
            querytabs=["all",""]
            info=[]

            if input_searchbox:
                querytabs[1]=input_searchbox
                print("we have something in the search box")
                search="%"+input_searchbox+"%"
                cursor.execute("""select emp_id,phone,email,name,dob,department,admin_id,password from temp natural join employee_login_visforce where upper(emp_id) like upper(:x1) or upper(name) like upper(:x2)""",[search,search])
                result1=cursor.fetchall()
            else:
                querytabs[1]=""
                print("we have nothing in the search box")
                search="%"+input_searchbox+"%"
                cursor.execute("""select emp_id,phone,email,name,dob,department,admin_id,password from temp natural join employee_login_visforce """)
                result1=cursor.fetchall()
                
            if input_department=="all":
                querytabs[0]="all"
                cursor.execute("""select emp_id,phone,email,name,dob,department,admin_id,password from temp natural join employee_login_visforce """)
                result2=cursor.fetchall()
            elif input_department=="sal":
                querytabs[0]="sal"
                cursor.execute("""select emp_id,phone,email,name,dob,department,admin_id,password from temp natural join employee_login_visforce where department='SAL'""")
                result2=cursor.fetchall()
            elif input_department=="mar":
                querytabs[0]="mar"
                cursor.execute("""select emp_id,phone,email,name,dob,department,admin_id,password from temp natural join employee_login_visforce where department='MAR'""")
                result2=cursor.fetchall()
            elif input_department=="sup":
                querytabs[0]="sup"
                cursor.execute("""select emp_id,phone,email,name,dob,department,admin_id,password from temp natural join employee_login_visforce where department='SUP'""")
                result2=cursor.fetchall()

            result = list(set(result1) & set(result2))
            print(result)
            for i in range(0,len(result)):
                info.append(Employee(result[i][0],result[i][1],result[i][2],result[i][3],result[i][4],result[i][5],result[i][6],result[i][7]))

            cursor.execute("""drop view temp""")
            cursor.execute("""commit""")  
            return render_template("myemployees.html",info=info,querytabs=querytabs,admin_id=admin_id)
            
        except:
            print("we did not query")
            
        try:#if we delete an employee
            input_delete=request.form["delete"]
            input_emp_id=request.form["emp_id"]
            cursor.execute("delete from employee_login_visforce where emp_id=:x1",[input_emp_id])
            cursor.execute("commit")
            flash("An employee was deleted!")
            return redirect(url_for('myemployees'))

        except:
            print ("we did not delete any employee")

        try:#editing the employee
            print("edit")
            input_dob=request.form["dob"]
            print(input_dob)
            input_email=request.form["email"]
            input_mobile=request.form["mobile"]
            input_department=request.form["department"]
            input_password=request.form["password"]
            input_name=request.form["name"]
            opened_emp_id=request.form["emp_id"]

            cursor.execute("""update employee_main_visforce set phone=:x1 where emp_id=:x2""",[input_mobile,opened_emp_id])
            cursor.execute("""update employee_phone_visforce set phone=:x1 where emp_id=:x2""",[input_mobile,opened_emp_id])
            cursor.execute("""commit""")

            cursor.execute("""update employee_main_visforce set email=:x1 where emp_id=:x2""",[input_email,opened_emp_id])
            cursor.execute("""commit""")

            input_dob=input_dob[8:]+"-"+getmonth(input_dob[5:7])+"-"+input_dob[0:4]
            print("newdob=",input_dob)
            cursor.execute("""update employee_phone_visforce set dob=:x1 where emp_id=:x2""",[input_dob,opened_emp_id])
            cursor.execute("""commit""")
            
            cursor.execute("""update employee_phone_visforce set name=:x1 where emp_id=:x2""",[input_name,opened_emp_id])
            cursor.execute("""commit""")
            
            cursor.execute("""update employee_phone_visforce set department=:x1 where emp_id=:x2""",[input_department,opened_emp_id])
            cursor.execute("""commit""")
            
            cursor.execute("""update employee_login_visforce set password=:x1 where emp_id=:x2""",[input_password,opened_emp_id])
            cursor.execute("""commit""")

            flash("The information has been updated!")
            return redirect(url_for('myemployees'))

        except:
            print("newleafalsofailed")
            
            
        
    else:
        #-----------ACCESS RESTRICTIONS--------------
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Admin':
                admin_id=session["id"]
                usertype=session["usertype"]
            else:
                flash("Please login first")
                return redirect(url_for('login'))
        else:
            flash("Please login first")
            return redirect(url_for('login'))
        #---------------------------------------------

        info=[]
        querytabs=["all",""]

        cursor.execute("""create or replace view temp as select employee_phone_visforce.emp_id,employee_phone_visforce.phone,email,name,dob,department from employee_main_visforce inner join employee_phone_visforce on employee_main_visforce.emp_id=employee_phone_visforce.emp_id""")
        cursor.execute("""commit""")
        cursor.execute("""select emp_id,phone,email,name,dob,department,admin_id,password from temp natural join employee_login_visforce""")
        result=cursor.fetchall()
        print(result)
        for i in range(0,len(result)):
            info.append(Employee(result[i][0],result[i][1],result[i][2],result[i][3],result[i][4],result[i][5],result[i][6],result[i][7]))

        cursor.execute("""drop view temp""")
        cursor.execute("""commit""")  
        return render_template("myemployees.html",info=info,querytabs=querytabs,admin_id=admin_id)








@app.route("/announcements",methods=["POST", "GET"])
def announcements():
    if request.method=="POST":
        #-----------ACCESS RESTRICTIONS--------------
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Admin':
                admin_id=session["id"]
                usertype=session["usertype"]
                print(admin_id,"has logged in")
            else:
                flash("Please login first")
                return redirect(url_for('login'))
        else:
            flash("Please login first")
            return redirect(url_for('login'))
        #---------------------------------------------
        try:#if we query
            input_dateofposting=request.form["dateofposting"]
            info=[]
            querytabs=[None]

            if input_dateofposting:
                print("dategiven")
                htmldate=input_dateofposting
                querytabs[0]=htmldate
                input_dateofposting=input_dateofposting[-2:]+"-"+getmonth(input_dateofposting[5:7])+"-"+input_dateofposting[2:4]
                cursor.execute("""select announcement_id,to_char(date_of_posting) dop, to_char(time_of_posting) top,message,admin_id,title from announcement_visforce where to_char(date_of_posting)=:x1 order by date_of_posting desc,time_of_posting desc""",[input_dateofposting])
                result=cursor.fetchall()
                for i in range(0,len(result)):
                    info.append(Announcement(result[i][0],result[i][1],(result[i][2])[10:18]+(result[i][2])[-3:],result[i][3],result[i][4],result[i][5]))
                return render_template("announcements.html",querytabs=querytabs,info=info,admin_id=admin_id)
            else:
                return redirect(url_for('announcements'))
            
        except:
            print("they did not query")

        try:#if we delete
            input_delete=request.form["delete"]
            input_announcementid=request.form["announcementid"]
            cursor.execute("delete from announcement_visforce where announcement_id=:x1",[input_announcementid])
            cursor.execute("commit")
            flash("An announcement was deleted!")
            return redirect(url_for('announcements'))

        except:
            print ("we did not delete anything")

        try:#if we make an announcement
            input_title=request.form["title"]
            input_message=request.form["message"]
            import datetime
            from datetime import date
            today=date.today()
            date=today.strftime("%d-%m-%Y")
            sqldate=date[0:3]+getmonth(date[3:5])+date[5:]
            now = datetime.datetime.now()
            now=str(now)
            sqltime = sqldate+" "+gethour(now[11:19])
            cursor.execute("""select count(*) from announcement_visforce""")
            result = cursor.fetchall()
            print(result)
            if result[0][0]==0:
                print("i am generating AN1")
                input_announcementid="AN1"
            else:
                cursor.execute("""select max(announcement_id) from announcement_visforce""")
                result = cursor.fetchall()
                print (result)
                maxid=(result[0][0])[2:]
                print (maxid)
                maxid=int(maxid)
                print ("maxid=",maxid)
                input_announcementid=maxid+1
                print(input_announcementid)
                input_announcementid="AN"+str(input_announcementid)
            cursor.execute("""insert into announcement_visforce values (:x1,:x2,:x3,:x4,:x5,:x6)""",[input_announcementid,sqldate,sqltime,input_message,admin_id,input_title])
            cursor.execute("""commit""")
            flash("Announcement is posted!")
            return redirect(url_for('announcements'))
        except:
            print("we did not make an announcement")


            
    else:
        #-----------ACCESS RESTRICTIONS--------------
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Admin':
                admin_id=session["id"]
                usertype=session["usertype"]
                print(admin_id,"has logged in")
            else:
                flash("Please login first")
                return redirect(url_for('login'))
        else:
            flash("Please login first")
            return redirect(url_for('login'))
        #---------------------------------------------

        cursor.execute("""select  announcement_id,to_char(date_of_posting) dop, to_char(time_of_posting) top,message,admin_id,title from announcement_visforce order by date_of_posting desc,time_of_posting desc""")
        result=cursor.fetchall()
        info=[]
        querytabs=[None]

        for i in range(0,len(result)):
            info.append(Announcement(result[i][0],result[i][1],(result[i][2])[10:18]+(result[i][2])[-3:],result[i][3],result[i][4],result[i][5]))
        return render_template("announcements.html",querytabs=querytabs,info=info,admin_id=admin_id)


@app.route("/addemployee",methods=["POST", "GET"])
def addemployee():
    if request.method=="POST":
        #-----------ACCESS RESTRICTIONS--------------
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Admin':
                admin_id=session["id"]
                usertype=session["usertype"]
            else:
                flash("Please login first")
                return redirect(url_for('login'))
        else:
            flash("Please login first")
            return redirect(url_for('login'))
        #---------------------------------------------

        input_name=request.form["name"]
        input_dob=request.form["dob"]
        input_dob=input_dob[8:]+"-"+getmonth(input_dob[5:7])+"-"+input_dob[0:4]
        input_email=request.form["email"]
        input_mobile=request.form["mobile"]
        input_department=request.form["department"]
        input_password=request.form["password"]
        input_emp_id='E1'

        cursor.execute("""select count(*) from employee_main_visforce""")
        result = cursor.fetchall()
        print(result)
        if result[0][0]==0:
            print("i am generating E1")
            input_emp_id="E1"
        else:
            cursor.execute("""select max(emp_id) from employee_main_visforce""")
            result = cursor.fetchall()
            print (result)
            maxid=(result[0][0])[1:]
            print (maxid)
            maxid=int(maxid)
            print ("maxid=",maxid)
            input_emp_id=maxid+1
            print(input_emp_id)
            input_emp_id="E"+str(input_emp_id)
            print(input_emp_id)

        cursor.execute("""insert into employee_login_visforce values(:x1,:x2,:x3)""",[input_emp_id,input_password,admin_id])
        cursor.execute("""insert into employee_main_visforce values (:x1,:x2,:x3)""",[input_emp_id,input_mobile,input_email])
        cursor.execute("""insert into employee_phone_visforce values (:x1,:x2,:x3,:x4,:x5)""",[input_emp_id,input_mobile,input_name,input_dob,input_department])
     
        cursor.execute("""commit""")
        flash("Employee added!")
        return render_template("addemployee.html",admin_id=admin_id)
    else:
        #-----------ACCESS RESTRICTIONS--------------
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Admin':
                admin_id=session["id"]
                usertype=session["usertype"]
            else:
                flash("Please login first")
                return redirect(url_for('login'))
        else:
            flash("Please login first")
            return redirect(url_for('login'))
        #---------------------------------------------
        return render_template("addemployee.html",admin_id=admin_id)
        



@app.route("/admin_accessvisdatabases_targetaudience",methods=["POST", "GET"])
def admin_accessvisdatabases_targetaudience():
    if request.method=="POST":
        #-----------ACCESS RESTRICTIONS--------------
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Admin':
                admin_id=session["id"]
                usertype=session["usertype"]
            else:
                flash("Please login first")
                return redirect(url_for('login'))
        else:
            flash("Please login first")
            return redirect(url_for('login'))
        #---------------------------------------------

        querytabs=["","","","","ALL",None,None,None,None,[]]#please check
        
        input_name=request.form["name"]
        print(1,input_name)
        input_email=request.form["email"]
        print(2,input_email)
        input_phone=request.form["phone"]
        print(3,input_phone)
        input_location=request.form["location"]
        print(4,input_location)
        input_gender=request.form["gender"]
        print(5,input_gender)
        input_salary_lower=request.form["salary_lower"]
        print(6,input_salary_lower)
        input_salary_upper=request.form["salary_upper"]
        print(7,input_salary_upper)
        input_age_lower=request.form["age_lower"]
        print(8,input_age_lower)
        input_age_upper=request.form["age_upper"]
        print(9,input_age_upper)
        input_agenull=request.form.getlist("agenull")
        print(10,input_agenull)
        input_generate=request.form.getlist("generate")

        print(input_name,input_salary_lower,input_agenull)#to see default format
        
        cursor.execute("""create or replace view temp as select serialno,name,email,salary,location,gender,address,dob,TRUNC(TO_NUMBER(SYSDATE - TO_DATE(dob))/365.25) as age from targetaudience_main_visforce order by serialno asc""");
        cursor.execute("""select * from temp""")
        result=cursor.fetchall()

        result1=result2=result3=result4=result5=result6=result7=result8=result9=result10=result


        
        if input_name:
            print("OLOLOLOname")
            querytabs[0]=input_name
            input_name="%"+input_name+"%"
            cursor.execute("""select * from temp where upper(name) like upper(:x1) order by serialno asc""",[input_name])
            result1=cursor.fetchall()            
        if input_email:
            print("OLOLOLO")
            querytabs[1]=input_email
            input_email="%"+input_email+"%"
            cursor.execute("""select * from temp where upper(email) like upper(:x1) order by serialno asc""",[input_email])
            result2=cursor.fetchall()
        if input_phone:
            print("OLOLOLOphone")
            querytabs[2]=input_phone
            input_phone="%"+input_phone+"%"
            cursor.execute("""select * from temp where serialno in (select serialno from targetaudience_phone_visforce where phone like :x1) order by serialno asc""",[input_phone])
            result3=cursor.fetchall()            
        if input_location:
            print("OLOLOLOlocation")
            querytabs[3]=input_location
            input_location="%"+input_location+"%"
            cursor.execute("""select * from temp where upper(location) like upper(:x1) order by serialno asc""",[input_location])
            result4=cursor.fetchall()
            
        if input_gender=="F":
            querytabs[4]='F'
            cursor.execute("""select * from temp where upper(gender)='F' order by serialno asc""")
            result5=cursor.fetchall()
        elif input_gender=="M":
            querytabs[4]='M'
            cursor.execute("""select * from temp where upper(gender)='M' order by serialno asc""")
            result5=cursor.fetchall()
        else:#all
            querytabs[4]='ALL'
            cursor.execute("""select * from temp""")
            result5=cursor.fetchall()
            
        if input_salary_lower:
            print("OLOLOLOsallow")
            querytabs[5]=input_salary_lower
            cursor.execute("""select * from temp where salary>=:x1 order by serialno asc""",[input_salary_lower])
            result6=cursor.fetchall()
        if input_salary_upper:
            print("OLOLOLO")
            querytabs[6]=input_salary_upper
            cursor.execute("""select * from temp where salary<=:x1 order by serialno asc""",[input_salary_upper])
            result7=cursor.fetchall()       

        
        querytabs[9]=input_agenull
        if input_agenull==['0']:#include non dob entries
            print("OLOLOLO")
            
            if input_age_lower:
                querytabs[7]=input_age_lower
                cursor.execute("""SELECT * FROM temp where age >=:x1 OR DOB IS NULL order by serialno asc""",[input_age_lower])
                result8=cursor.fetchall()
            if input_age_upper:
                querytabs[8]=input_age_upper
                cursor.execute("""SELECT * FROM temp where age  <=:x1 OR DOB IS NULL order by serialno asc""",[input_age_upper])
                result9=cursor.fetchall()
        else:#do not include non dob entries
            if input_age_lower:
                querytabs[7]=input_age_lower
                cursor.execute("""SELECT * FROM temp where age >=:x1 order by serialno asc""",[input_age_lower])
                result8=cursor.fetchall()
            if input_age_upper:
                querytabs[8]=input_age_upper
                cursor.execute("""SELECT * FROM temp where age <=:x1 order by serialno asc""",[input_age_upper])
                result9=cursor.fetchall()
        
        result=list(set(result1) & set(result2) & set(result3) & set(result4) & set(result5) & set(result6) & set(result7) & set(result8) & set(result9))
                
                
            


        info=[]
        for i in range(0,len(result)):
            cursor.execute("""SELECT phone FROM targetaudience_phone_visforce where serialno=:x1""",[result[i][0]])
            resultsupp=cursor.fetchall()
            info.append(Target_Audience(result[i][0],result[i][1],resultsupp,result[i][2],result[i][3],result[i][4],result[i][5],result[i][6],str(result[i][7]),result[i][8]))

        #print(type(result[0][3]),result[0][5],type(result[0][8]))

        cursor.execute("select count(*) from targetaudience_main_visforce")
        count=cursor.fetchall()
        
        if len(result)!=0:
        #stats
            sal=[]
            age=[]
            email=[]
            countF=0
            countM=0
            for i in range(0,len(result)):
                sal.append(result[i][3])
                email.append(result[i][2])
                if result[i][8]!=None:               
                    age.append(result[i][8])
                if result[i][5]=="F":
                    countF=countF+1
                elif result[i][5]=='M':
                    countM=countM+1
            
            stats=[len(result),round(sum(sal)/len(sal),3),min(sal),max(sal),int(sum(age)/len(age)),min(age),max(age),countF,countM,count[0][0]]
        else:
            stats=[]
        print(stats)
        print(result[0][7])
        cursor.execute("""drop view temp""")
        cursor.execute("""commit""")
        print(len(info))

        if input_generate==['0']:#generate
            mailinglist=open("mailinglistTA.txt",'w+')
            for i in email:
                mailinglist.write(i+"; ")
            mailinglist.close()
        else:
            mailinglist=None
            
            
        print(stats)
        return render_template("admin_accessvisdatabases_targetaudience.html",info=info,querytabs=querytabs,admin_id=admin_id,stats=stats,mailinglist=mailinglist)
    
    else:
        #-----------ACCESS RESTRICTIONS--------------
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Admin':
                admin_id=session["id"]
                usertype=session["usertype"]
            else:
                flash("Please login first")
                return redirect(url_for('login'))
        else:
            flash("Please login first")
            return redirect(url_for('login'))
        #---------------------------------------------

        info=[]
        querytabs=["","","","","ALL",None,None,None,None,[]]
        stats=[]
        mailinglist=None
        return render_template("admin_accessvisdatabases_targetaudience.html",info=info,querytabs=querytabs,admin_id=admin_id,stats=stats,mailinglist=mailinglist)
        




@app.route("/admin_accessvisdatabases_pastsales",methods=["POST", "GET"])
def admin_accessvisdatabases_pastsales():
    if request.method=="POST":
        #-----------ACCESS RESTRICTIONS--------------
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Admin':
                admin_id=session["id"]
                usertype=session["usertype"]
            else:
                flash("Please login first")
                return redirect(url_for('login'))
        else:
            flash("Please login first")
            return redirect(url_for('login'))
        #---------------------------------------------
        querytabs=["","","","","ALL",None,None]
        input_buyername=request.form["buyername"]
        input_dateofsale=request.form["dateofsale"]
        input_product=request.form["product"]
        input_orderid=request.form["orderid"]
        input_status=request.form["status"]
        input_price_lower=request.form["price_lower"]
        input_price_upper=request.form["price_upper"]


        cursor.execute("""select * from pastsales_visforce""")
        result=cursor.fetchall()
        result0=result1=result2=result3=result4=result5=result6=result

        

        if input_buyername:
            print("OLOLOLOname")
            querytabs[0]=input_buyername
            input_buyername="%"+input_buyername+"%"
            cursor.execute("""select * from pastsales_visforce where upper(buyername) like upper(:x1)""",[input_buyername])
            result0=cursor.fetchall()
            
        if input_dateofsale!="": #dateofsale
            print("queryyyy[1]",querytabs[1])
            print("OLOLOLOdate")
            htmldate=input_dateofsale
            print("htmldate",htmldate)
            print("input_dateofsale=",input_dateofsale)
            querytabs[1]=htmldate
            input_dateofsale=input_dateofsale[-2:]+"-"+getmonth(input_dateofsale[5:7])+"-"+input_dateofsale[2:4]
            cursor.execute("""select * from pastsales_visforce where dateofsale=:x1""",[input_dateofsale])
            result1=cursor.fetchall()
            
        if input_product:
            print("OLOLOLOpro")
            querytabs[2]=input_product
            input_product="%"+input_product+"%"
            cursor.execute("""select * from pastsales_visforce where upper(product) like upper(:x1)""",[input_product])
            result2=cursor.fetchall()
        if input_orderid:
            print("OLOLOLOorder")
            querytabs[3]=input_orderid
            input_orderid="%"+input_orderid+"%"
            cursor.execute("""select * from pastsales_visforce where upper(orderid) like upper(:x1)""",[input_orderid])
            result3=cursor.fetchall()
            
        if input_status=="delivered":
            print("OLOLOLOstatus")
            querytabs[4]=input_status
            input_status="%"+input_status+"%"
            cursor.execute("""select * from pastsales_visforce where upper(status) like upper(:x1)""",[input_status])
            result4=cursor.fetchall()
        elif input_status=="picked":
            print("OLOLOLOsta")
            querytabs[4]=input_status
            input_status="%"+input_status+"%"
            cursor.execute("""select * from pastsales_visforce where upper(status) like upper(:x1)""",[input_status])
            result4=cursor.fetchall()
        else:#all
            print("OLOLOLOsta")
            querytabs[4]==input_status
            cursor.execute("""select * from pastsales_visforce """)
            result4=cursor.fetchall()

        if input_price_lower:
            print("OLOLOLOlow")
            querytabs[5]=input_price_lower
            cursor.execute("""select * from pastsales_visforce where price>=:x1 """,[input_price_lower])
            result5=cursor.fetchall()
            
        if input_price_upper:
            print("OLOLOLOhigh")
            querytabs[6]=input_price_upper
            cursor.execute("""select * from pastsales_visforce where price<=:x1""",[input_price_upper])
            result6=cursor.fetchall()
        


        result=list(set(result0) & set(result1) & set(result1) & set(result2) & set(result3) & set(result4) & set(result5) & set(result6))


            
        info=[]
        for i in range(0,len(result)):
            info.append(Past_Sales(str(result[i][0]),result[i][1],result[i][2],result[i][3],result[i][4],result[i][5],result[i][6]))
            
        cursor.execute("select count(*) from pastsales_visforce")
        count=cursor.fetchall()
        
        if len(result)!=0:
            delivered=0
            picked=0
            price=[]
            for i in range(0,len(result)):
                price.append(result[i][5])
                if "delivered".upper() in (result[i][6]).upper() :
                    delivered=delivered+1
                elif "picked".upper() in (result[i][6]).upper():
                    picked=picked+1

            stats=[len(result),delivered,picked,round(sum(price)/len(price),3),min(price),max(price),sum(price),count[0][0]]
        else:
            stats=[]
        print("stats=",stats)
        return render_template("admin_accessvisdatabases_pastsales.html",info=info,admin_id=admin_id,querytabs=querytabs,stats=stats)

            
    else:
        #-----------ACCESS RESTRICTIONS--------------
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Admin':
                admin_id=session["id"]
                usertype=session["usertype"]
            else:
                flash("Please login first")
                return redirect(url_for('login'))
        else:
            flash("Please login first")
            return redirect(url_for('login'))
        #---------------------------------------------
        info=[]
        querytabs=["","","","","ALL",None,None]
        stats=[]
        return render_template("admin_accessvisdatabases_pastsales.html",info=info,admin_id=admin_id,querytabs=querytabs,stats=stats)








@app.route("/accessdatabases_admin",methods=["POST", "GET"])
def accessdatabases_admin():
    if request.method=="POST":
        #-----------ACCESS RESTRICTIONS--------------
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Admin':
                admin_id=session["id"]
                usertype=session["usertype"]
            else:
                flash("Please login first")
                return redirect(url_for('login'))
        else:
            flash("Please login first")
            return redirect(url_for('login'))
        #---------------------------------------------
        return render_template("accessdatabases_admin.html",admin_id=admin_id)
    else:
        #-----------ACCESS RESTRICTIONS--------------
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Admin':
                admin_id=session["id"]
                usertype=session["usertype"]
            else:
                flash("Please login first")
                return redirect(url_for('login'))
        else:
            flash("Please login first")
            return redirect(url_for('login'))
        #---------------------------------------------
        return render_template("accessdatabases_admin.html",admin_id=admin_id)



@app.route("/updatedatabases",methods=["POST", "GET"])
def updatedatabases():
    if request.method=="POST":
        #-----------ACCESS RESTRICTIONS--------------
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Admin':
                admin_id=session["id"]
                usertype=session["usertype"]
            else:
                flash("Please login first")
                return redirect(url_for('login'))
        else:
            flash("Please login first")
            return redirect(url_for('login'))
        #---------------------------------------------
        print("here")
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for("updatedatabases"))
        print("here2")
        file = request.files['file']
        print("here3")
        if file.filename == '':
            print("no file name")
            flash('No selected file')
            return redirect(url_for("updatedatabases"))
        
        if file and allowed_file(file.filename):
            print ("file is csv")
            filename = secure_filename(file.filename)
            print(uploadedTAfiles)
            if file.filename in uploadedTAfiles or file.filename in uploadedPSfiles:
                flash("This file is already uploaded")
                print("This file is already uploaded")
                return redirect(url_for("updatedatabases"))
            
            print(uploadedTAfiles)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))#save  
            print("uploaded successfully")
            print(file.filename)

            if request.form["type"]=="TA":
                try:#TAdatabasemaker
                #------------------TAdatabasemaker             
                    import math
                    import csv
                    import numpy as np
                    import re

                    info=open(file.filename)
                    info_reader=csv.reader(info,delimiter=',')
                    info_array=list(info_reader)#converting into 2D list
                    info_array=np.array(info_array)#coverting list into numpy array

                    col_name={'name':1,'phone':3,'email':4,'salary':6,'city':7,'serialno':0,'dob':14,'gender':5,'address':15}
                    data_start=3
                    records=500
                    cursor.execute("""select count(*) from targetaudience_main_visforce""")
                    result=cursor.fetchall()
                    result=int(result[0][0])
                    serialno=result+1

                    for i in range(data_start,data_start+records):
                        name=info_array[i][col_name['name']]
                        email=info_array[i][col_name['email']]
                        location=info_array[i][col_name['city']]
                        address=info_array[i][col_name['address']]
                        temp1=info_array[i][col_name['phone']]
                        temp1=temp1.split('\n')
                        phone=[]
                        for j in temp1:
                            temp2=j.replace(' ','')
                            temp2=re.sub("[^0-9]", "", temp2)
                            phone.append(temp2)
                        temp1=info_array[i][col_name['gender']]
                        if 'M' in temp1:
                            gender='M'
                        else:
                            gender='F'
                        temp1=info_array[i][col_name['salary']]
                        temp1=re.findall('\d*\.?\d+',temp1)
                        salary=float(temp1[0])*100000
            
                        temp1=info_array[i][col_name['dob']]
                        temp1=re.findall(r'\(.*?\)', temp1)
                        if temp1:
                            temp1=temp1[0]
                            temp1=temp1.replace("(","")
                            temp1=temp1.replace(")","")
                            temp1=temp1.split()
                            day=temp1[0]
                            month=temp1[1]
                            year=temp1[2]
                            dob=day+'-'+month+'-'+year
                        else:
                            dob=None
                        cursor.execute("""insert into targetaudience_main_visforce values(:x1,:x2,:x3,:x4,:x5,:x6,:x7,:x8)""",[serialno,name,email,salary,location,gender,address,dob])
                        cursor.execute("""commit""")
                        for i in phone:
                            cursor.execute("""insert into targetaudience_phone_visforce values (:x1,:x2)""",[serialno,i])
                            cursor.execute("""commit""")
                        print(serialno,name)
                        serialno=serialno+1
                    uploadedTAfiles.append(file.filename)
                    #-----------TADATAABSEMAKER----------
                    flash("File uploaded,proper syntax")
                    return redirect(url_for("updatedatabases"))
                except:

                    print("file structure is not compatible to target audience")
                    flash("file structure is not compatible to target audience")
                    return redirect(url_for("updatedatabases"))

                
            elif request.form["type"]=="pastsales":
                print("iseepastsaleshas been selected")
                try:
                    #pastsalesDBmaker
                    import math
                    import csv
                    import numpy as np
                    import re

                    info=open(file.filename)
                    info_reader=csv.reader(info,delimiter=',')
                    info_array=list(info_reader)#converting into 2D list
                    info_array=np.array(info_array)


                    col_name={'dateofsale':0,'buyername':1,'address':2,'product':3,'orderid':4,'price':5,'status':6}
                    data_start=1
                    records=len(info_array)


                    for i in range(data_start,records):
                        dateofsale=info_array[i][col_name['dateofsale']]
                        dateofsale=dateofsale[0:3]+getmonth(dateofsale[3:5])+dateofsale[-5:]

                        
                        buyername=info_array[i][col_name['buyername']]
                        address=info_array[i][col_name['address']]
                        product=info_array[i][col_name['product']]
                        orderid=info_array[i][col_name['orderid']]
                        
                        price=info_array[i][col_name['price']]
                        price=int(re.sub("[^0-9]", "", price))
                        
                        status=info_array[i][col_name['status']]

                        
                        print(dateofsale,buyername,price,type(price))

                        
                        cursor.execute("""insert into pastsales_visforce values(:x1,:x2,:x3,:x4,:x5,:x6,:x7)""",[dateofsale,buyername,address,product,orderid,price,status])
                        cursor.execute("""commit""")
                        
                    uploadedPSfiles.append(file.filename)
                    flash("File uploaded,proper syntax")
                    return redirect(url_for("updatedatabases"))
                        
                except:
                    print("File structure is not compatible to pastsales database format")
                    flash("File structure is not compatible to pastsales database format")
                    return redirect(url_for("updatedatabases"))                  
  

            elif request.form["type"]=="supplier":
                print("not integrated yet")
                flash("not inegrated yet")
                return redirect(url_for("updatedatabases"))              
                    
                
        else:
            print("file not a csv")
            flash("This file was not csv file")
            return redirect(url_for("updatedatabases"))
        
            
    else:
        #-----------ACCESS RESTRICTIONS--------------
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Admin':
                admin_id=session["id"]
                usertype=session["usertype"]
            else:
                flash("Please login first")
                return redirect(url_for('login'))
        else:
            flash("Please login first")
            return redirect(url_for('login'))
        #---------------------------------------------
        return render_template("prac1.html",admin_id=admin_id)


#--------------------------------------------------
 
#--------------------------------------------------
    
#--------------------------------------------------
    
#------------EMPLOYEE SECTION----------------------
@app.route("/givefeedback",methods=["POST","GET"])
def givefeedback():
    if "id" in session and "usertype" in session:
        if session["usertype"]=='Employee':
            emp_id=session["id"]
            usertype=session["usertype"]
        else:
            flash("Please login first")
            return redirect(url_for('login'))
            
    else:
        flash("Please login first")
        return redirect(url_for('login'))
    
    if request.method=="POST":


        cursor.execute("""select count(*) from feedback_visforce""")
        result = cursor.fetchall()
        print(result)
        if result[0][0]==0:
            print("i am generating F1")
            input_feedbackid="F1"
        else:
            cursor.execute("""select max(feedback_id) from feedback_visforce""")
            result = cursor.fetchall()
            print (result)
            maxid=(result[0][0])[1:]
            print (maxid)
            maxid=int(maxid)
            print ("maxid=",maxid)
            input_feedbackid=maxid+1
            print(input_feedbackid)
            input_feedbackid="F"+str(input_feedbackid)


        import datetime
        from datetime import date
        today=date.today()
        date=today.strftime("%d-%m-%Y")
        print(date)
        sqldate=date[0:3]+getmonth(date[3:5])+date[5:]
        print(sqldate)
        
        now = datetime.datetime.now()
        now=str(now)
        print("now=",now)
        sqltime = sqldate+" "+gethour(now[11:19])
        print(sqltime)

        input_feedback=request.form["feedback"]
        input_dateofposting=sqldate
        input_timeofposting=sqltime
        input_comment=""
        input_emp_id=emp_id
        input_admin_id=""
        
        f=Feedback(input_feedbackid,input_dateofposting,input_timeofposting,input_feedback,input_comment,input_emp_id,input_admin_id)
        print("check1")
        print(input_dateofposting,input_timeofposting)
        cursor.execute("""insert into feedback_visforce (feedback_id,date_of_posting,time_of_posting,feedback_message,emp_id,admin_comment,admin_id) values (:x1,:x2,:x3,:x4,:x5,null,null)""",[f.feedbackid,f.dateofposting,f.timeofposting,f.message,f.emp_id])
        print("check2")
        cursor.execute("""commit""")
        print("check3")
        flash("Your feedback is recorded","info")
        cursor.execute("""select name from employee_phone_visforce where emp_id=:x1""",[emp_id])
        result = cursor.fetchall()
        user=[emp_id,result[0][0]]
        return redirect(url_for('seemyfeedback'))
    else:
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Employee':
                emp_id=session["id"]
                usertype=session["usertype"]
            else:
                flash("Please login first")
                return redirect(url_for('login'))    
        else:
            flash("Please login first")
            return redirect(url_for('login'))

        cursor.execute("""select name from employee_phone_visforce where emp_id=:x1""",[emp_id])
        result = cursor.fetchall()
        user=[emp_id,result[0][0]]
        return render_template("givefeedback.html",user=user)



@app.route("/seemyfeedback",methods=["POST","GET"])
def seemyfeedback():
    if request.method=="POST":
        #--------ACCESS FEEDBACKS-----------------
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Employee':
                emp_id=session["id"]
                usertype=session["usertype"]
            else:
                flash("Please login first")
                return redirect(url_for('login'))
                
        else:
            flash("Please login first")
            return redirect(url_for('login'))
        #-------------------------------------------

        try:#if we delete a feedback
            input_delete=request.form["delete"]
            input_feedbackid=request.form["feedbackid"]
            cursor.execute("delete from feedback_visforce where feedback_id=:x1",[input_feedbackid])
            cursor.execute("commit")
            flash("A feedback was deleted!")
            return redirect(url_for('seemyfeedback'))

        except:
            print ("we did not delete anything")


        
        input_date=request.form["date"]
        input_status=request.form["status"]
        info=[]
        
        import datetime
        from datetime import date
        today=date.today()
        date=today.strftime("%Y-%m-%d")
        querytabs=[None,"uncom"]
        cursor.execute("""create or replace view temp as select feedback_id,to_char(date_of_posting) dop,to_char(time_of_posting) time,feedback_message,admin_comment,admin_id,emp_id from feedback_visforce""")
        cursor.execute("""commit""")
        
        if input_date:
            print("date was eneterd")
            htmldate=input_date
            input_date=input_date[-2:]+"-"+getmonth(input_date[5:7])+"-"+input_date[2:4]
            querytabs[0]=htmldate
            if input_status=="com":
                querytabs[1]="com"
                cursor.execute("""select * from temp where dop=:x1 and emp_id=:x2 and admin_comment is not null""",[input_date,emp_id])
                result = cursor.fetchall()
            elif input_status=="uncom":
                querytabs[1]="uncom"
                cursor.execute("""select * from temp where dop=:x1 and emp_id=:x2 and admin_comment is null""",[input_date,emp_id])
                result = cursor.fetchall()
            elif input_status=="all":
                querytabs[1]="all"
                cursor.execute("""select * from temp where dop=:x1 and emp_id=:x2""",[input_date,emp_id])
                result = cursor.fetchall()
        else:
            print("noe date was enetered")
            if input_status=="com":
                querytabs[1]="com"
                cursor.execute("""select * from temp where  emp_id=:x2 and admin_comment is not null""",[emp_id])
                result = cursor.fetchall()
            elif input_status=="uncom":
                querytabs[1]="uncom"
                cursor.execute("""select * from temp where emp_id=:x2 and admin_comment is null""",[emp_id])
                result = cursor.fetchall()
            elif input_status=="all":
                querytabs[1]="all"
                cursor.execute("""select * from temp where emp_id=:x2""",[emp_id])
                result = cursor.fetchall()        
    
        for i in range(0,len(result)):
            info.append(Feedback(result[i][0],result[i][1],(result[i][2])[10:18]+(result[i][2])[-3:],result[i][3],result[i][4],None,result[i][5]))
        cursor.execute("""drop view temp""")
        cursor.execute("""commit""")
        
        cursor.execute("""select name from employee_phone_visforce where emp_id=:x1""",[emp_id])
        result = cursor.fetchall()
        user=[emp_id,result[0][0]]
        
        return render_template("seemyfeedback.html",info=info,querytabs=querytabs,user=user)
    else:
        #--------ACCESS FEEDBACKS-----------------
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Employee':
                emp_id=session["id"]
                usertype=session["usertype"]
            else:
                flash("Please login first")
                return redirect(url_for('login'))
                
        else:
            flash("Please login first")
            return redirect(url_for('login'))
        #-------------------------------------------
        print("entered get")
        cursor.execute("""create or replace view temp as select feedback_id,to_char(date_of_posting) dop,to_char(time_of_posting) time,feedback_message,admin_comment,admin_id,emp_id from feedback_visforce""")
        cursor.execute("""commit""")
        cursor.execute("""SELECT * FROM temp where emp_id=:x1 order by dop,time desc """,[emp_id])
        result = cursor.fetchall()
        info=[]
        import datetime
        from datetime import date
        today=date.today()
        date=today.strftime("%Y-%m-%d")
        querytabs=[None,"all"]
        for i in range(0,len(result)):         
            info.append(Feedback(result[i][0],result[i][1],(result[i][2])[10:18]+(result[i][2])[-3:],result[i][3],result[i][4],None,result[i][5]))
        cursor.execute("""drop view temp""")
        cursor.execute("""commit""")
        cursor.execute("""select name from employee_phone_visforce where emp_id=:x1""",[emp_id])
        result = cursor.fetchall()
        user=[emp_id,result[0][0]]
        return render_template("seemyfeedback.html",info=info,querytabs=querytabs,user=user)





@app.route("/seeannouncements",methods=["POST", "GET"])
def seeannouncements():

    if request.method=="POST":
        #--------ACCESS FEEDBACKS-----------------
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Employee':
                emp_id=session["id"]
                usertype=session["usertype"]
            else:
                flash("Please login first")
                return redirect(url_for('login'))
                
        else:
            flash("Please login first")
            return redirect(url_for('login'))
        #-------------------------------------------
        cursor.execute("""select name from employee_phone_visforce where emp_id=:x1""",[emp_id])
        result=cursor.fetchall()
        user=[emp_id,result[0][0]]

        
        input_dateofposting=request.form["dateofposting"]
        info=[]
        querytabs=[None]

        if input_dateofposting:
            print("dategiven")
            htmldate=input_dateofposting
            querytabs[0]=htmldate
            input_dateofposting=input_dateofposting[-2:]+"-"+getmonth(input_dateofposting[5:7])+"-"+input_dateofposting[2:4]
            cursor.execute("""select announcement_id,to_char(date_of_posting) dop, to_char(time_of_posting) top,message,admin_id,title from announcement_visforce where to_char(date_of_posting)=:x1 order by date_of_posting desc,time_of_posting desc""",[input_dateofposting])
            result=cursor.fetchall()
            for i in range(0,len(result)):
                info.append(Announcement(result[i][0],result[i][1],(result[i][2])[10:18]+(result[i][2])[-3:],result[i][3],result[i][4],result[i][5]))
            return render_template("seeannouncements.html",querytabs=querytabs,info=info,user=user)
        else:
            return redirect(url_for('seeannouncements'))
            
    else:
        #--------ACCESS FEEDBACKS-----------------
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Employee':
                emp_id=session["id"]
                usertype=session["usertype"]
            else:
                flash("Please login first")
                return redirect(url_for('login'))
                
        else:
            flash("Please login first")
            return redirect(url_for('login'))
        #-------------------------------------------
        cursor.execute("""select name from employee_phone_visforce where emp_id=:x1""",[emp_id])
        result=cursor.fetchall()
        user=[emp_id,result[0][0]]
        
        cursor.execute("""select  announcement_id,to_char(date_of_posting) dop, to_char(time_of_posting) top,message,admin_id,title from announcement_visforce order by date_of_posting desc,time_of_posting desc""")
        result=cursor.fetchall()
        info=[]
        querytabs=[None]

        for i in range(0,len(result)):
            info.append(Announcement(result[i][0],result[i][1],(result[i][2])[10:18]+(result[i][2])[-3:],result[i][3],result[i][4],result[i][5]))
        return render_template("seeannouncements.html",querytabs=querytabs,info=info,user=user)
                       







@app.route("/myleaves",methods=["POST", "GET"])
def myleaves():
    if request.method=="POST":
        #--------ACCESS FEEDBACKS-----------------
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Employee':
                emp_id=session["id"]
                usertype=session["usertype"]
            else:
                flash("Please login first")
                return redirect(url_for('login'))
                
        else:
            flash("Please login first")
            return redirect(url_for('login'))
        #-------------------------------------------

        cursor.execute("""select name from employee_phone_visforce where emp_id=:x1""",[emp_id])
        result=cursor.fetchall()
        user=[emp_id,result[0][0]]

        try:#querying
            status=request.form["status"]
            input_dateofleave=request.form["dateofleave"]
            input_dateofreturn=request.form["dateofreturn"]
          
            info=[]
      
            if input_dateofleave:
                htmldate1=input_dateofleave
                input_dateofleave=input_dateofleave[-2:]+"-"+getmonth(input_dateofleave[5:7])+"-"+input_dateofleave[2:4]
            if input_dateofreturn:
                htmldate2=input_dateofreturn
                input_dateofreturn=input_dateofreturn[-2:]+"-"+getmonth(input_dateofreturn[5:7])+"-"+input_dateofreturn[2:4]


            querytabs=["all",None,None,""]
            cursor.execute("""create or replace view temp1 as select leave_id,to_char(date_of_leave) dol,to_char(date_of_return) dor,reason,status,to_char(time_applied) time,leave_visforce.emp_id,name,department,admin_id from leave_visforce inner join employee_phone_visforce on leave_visforce.emp_id=employee_phone_visforce.emp_id""")
            cursor.execute("""commit""")
                
            if status=="pen":
                querytabs[0]=status
                cursor.execute("""create or replace view temp2 as select * from temp1 where status in ('PEN')""")
                cursor.execute("""commit""")
            elif status=="acc":
                querytabs[0]=status 
                cursor.execute("""create or replace view temp2 as select * from temp1 where status in ('ACC')""")
                cursor.execute("""commit""")
            elif status=="rej":
                querytabs[0]=status
                cursor.execute("""create or replace view temp2 as select * from temp1 where status in ('REJ')""")
                cursor.execute("""commit""")
            elif status=="all":
                querytabs[0]=status
                cursor.execute("""create or replace view temp2 as select * from temp1 """)
                cursor.execute("""commit""")
            else:
                cursor.execute("""create or replace view temp2 as select * from temp1""")
                cursor.execute("""commit""")

            cursor.execute("""select * from temp2 where emp_id=:x1""",[emp_id])  
            result1=cursor.fetchall()
            result2=result1
            result3=result1
            
            if input_dateofleave:
                querytabs[1]=htmldate1
                cursor.execute("""select * from temp2 where Dol=:x1""", [input_dateofleave])
                result1 = cursor.fetchall()    
            if input_dateofreturn:
                querytabs[2]=htmldate2
                cursor.execute("""select * from temp2 where Dor=:x1""", [input_dateofreturn])
                result2 = cursor.fetchall()
     
                
            result = list(set(result1) & set(result2))

            for i in range(0,len(result)):         
                info.append(Leave(result[i][0],result[i][1],result[i][2],result[i][3],result[i][4],(result[i][5])[10:18]+(result[i][5])[-3:],result[i][6],result[i][7],result[i][8],result[i][9]))

            cursor.execute("""drop view temp1""")
            cursor.execute("""drop view temp2""")
            cursor.execute("""commit""")        
     
            return render_template("myleaves.html",info=info,querytabs=querytabs,user=user)
            
        except:
            print ("error in query")
  


        try:#if we delete a leave req
            input_delete=request.form["delete"]
            input_leaveid=request.form["leaveid"]
            cursor.execute("delete from leave_visforce where leave_id=:x1",[input_leaveid])
            cursor.execute("commit")
            flash("A leave request was deleted!")
            return redirect(url_for('myleaves'))

        except:
            print ("we did not delete anything")



        try:
            print("adding a new leave")
            input_title=request.form['title']
            input_dateofleave=request.form['dateofleave']
            input_dateofreturn=request.form['dateofreturn']
            input_reason=request.form['reason']
            input_dateofleave=input_dateofleave[-2:]+"-"+getmonth(input_dateofleave[5:7])+"-"+input_dateofleave[2:4]
            input_dateofreturn=input_dateofreturn[-2:]+"-"+getmonth(input_dateofreturn[5:7])+"-"+input_dateofreturn[2:4]

            import datetime
            from datetime import date
            today=date.today()
            date=today.strftime("%d-%m-%Y")
            print(date)
            sqldate=date[0:3]+getmonth(date[3:5])+date[5:]
            print(sqldate)
            now = datetime.datetime.now()
            now=str(now)
            print("now=",now)
            sqltime = sqldate+" "+gethour(now[11:19])
            print(sqltime)

            cursor.execute("""select count(*) from leave_visforce""")
            result = cursor.fetchall()
            print(result)
            if result[0][0]==0:
                print("i am generating L1")
                input_leaveid="L1"
            else:
                cursor.execute("""select max(leave_id) from leave_visforce""")
                result = cursor.fetchall()
                print (result)
                maxid=(result[0][0])[1:]
                print (maxid)
                maxid=int(maxid)
                print ("maxid=",maxid)
                input_leaveid=maxid+1
                print(input_leaveid)
                input_leaveid="L"+str(input_leaveid)

            cursor.execute("insert into leave_visforce values (:x1,:x2,:x3,:x4,'PEN',:x5,:x6,null,:x6)",[input_leaveid,input_dateofleave,input_dateofreturn,input_reason,sqltime,emp_id,input_title])
            cursor.execute("commit")
            print("should be added now")                 
            return redirect(url_for('myleaves'))
        except:
            print("added a leave")
    else:
        #--------ACCESS FEEDBACKS-----------------
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Employee':
                emp_id=session["id"]
                usertype=session["usertype"]
            else:
                flash("Please login first")
                return redirect(url_for('login'))
                
        else:
            flash("Please login first")
            return redirect(url_for('login'))
        #-------------------------------------------
        cursor.execute("""select name from employee_phone_visforce where emp_id=:x1""",[emp_id])
        result=cursor.fetchall()
        user=[emp_id,result[0][0]]
        
        cursor.execute("""create or replace view temp as select leave_id,to_char(date_of_leave) dol,to_char(date_of_return) dor,reason,status,to_char(time_applied) time,leave_visforce.emp_id,name,department,admin_id from leave_visforce inner join employee_phone_visforce on leave_visforce.emp_id=employee_phone_visforce.emp_id""")
        cursor.execute("""commit""")
        cursor.execute("""SELECT * FROM temp where emp_id=:x1 order by dol,time desc""",[emp_id])
        result = cursor.fetchall()
        info=[]
        querytabs=["all",None,None,""]
        for i in range(0,len(result)):         
            info.append(Leave(result[i][0],result[i][1],result[i][2],result[i][3],result[i][4],(result[i][5])[10:18]+(result[i][5])[-3:],result[i][6],result[i][7],result[i][8],result[i][9]))
        print("length of info_leaves",len(info))
        cursor.execute("""drop view temp""")
        cursor.execute("""commit""")  
        return render_template("myleaves.html",info=info,querytabs=querytabs,user=user)#info is a list of objects AND pending checkbox will be checked





@app.route("/emp_accessvisdatabases_targetaudience",methods=["POST", "GET"])
def emp_accessvisdatabases_targetaudience():
    if request.method=="POST":
        #--------ACCESS FEEDBACKS-----------------
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Employee':
                emp_id=session["id"]
                usertype=session["usertype"]
            else:
                flash("Please login first")
                return redirect(url_for('login'))
                
        else:
            flash("Please login first")
            return redirect(url_for('login'))
        #-------------------------------------------
        cursor.execute("""select name from employee_phone_visforce where emp_id=:x1""",[emp_id])
        result=cursor.fetchall()
        user=[emp_id,result[0][0]]

        querytabs=["","","","","ALL",None,None,None,None,[]]#please check

        
        input_name=request.form["name"]
        print(1,input_name)
        input_email=request.form["email"]
        print(2,input_email)
        input_phone=request.form["phone"]
        print(3,input_phone)
        input_location=request.form["location"]
        print(4,input_location)
        input_gender=request.form["gender"]
        print(5,input_gender)
        input_salary_lower=request.form["salary_lower"]
        print(6,input_salary_lower)
        input_salary_upper=request.form["salary_upper"]
        print(7,input_salary_upper)
        input_age_lower=request.form["age_lower"]
        print(8,input_age_lower)
        input_age_upper=request.form["age_upper"]
        print(9,input_age_upper)
        input_agenull=request.form.getlist("agenull")
        print(10,input_agenull)
        input_generate=request.form.getlist("generate")

        print(input_name,input_salary_lower,input_agenull)#to see default format
        
        cursor.execute("""create or replace view temp as select serialno,name,email,salary,location,gender,address,dob,TRUNC(TO_NUMBER(SYSDATE - TO_DATE(dob))/365.25) as age from targetaudience_main_visforce""");
        cursor.execute("""select * from temp""")
        result=cursor.fetchall()

        result1=result2=result3=result4=result5=result6=result7=result8=result9=result10=result


        
        if input_name:
            print("OLOLOLOname")
            querytabs[0]=input_name
            input_name="%"+input_name+"%"
            cursor.execute("""select * from temp where upper(name) like upper(:x1)""",[input_name])
            result1=cursor.fetchall()            
        if input_email:
            print("OLOLOLO")
            querytabs[1]=input_email
            input_email="%"+input_email+"%"
            cursor.execute("""select * from temp where upper(email) like upper(:x1)""",[input_email])
            result2=cursor.fetchall()
        if input_phone:
            print("OLOLOLOphone")
            querytabs[2]=input_phone
            input_phone="%"+input_phone+"%"
            cursor.execute("""select * from temp where serialno in (select serialno from targetaudience_phone_visforce where phone like :x1)""",[input_phone])
            result3=cursor.fetchall()            
        if input_location:
            print("OLOLOLOlocation")
            querytabs[3]=input_location
            input_location="%"+input_location+"%"
            cursor.execute("""select * from temp where upper(location) like upper(:x1)""",[input_location])
            result4=cursor.fetchall()
            
        if input_gender=="F":
            querytabs[4]='F'
            cursor.execute("""select * from temp where upper(gender)='F'""")
            result5=cursor.fetchall()
        elif input_gender=="M":
            querytabs[4]='M'
            cursor.execute("""select * from temp where upper(gender)='M'""")
            result5=cursor.fetchall()
        else:#all
            querytabs[4]='ALL'
            cursor.execute("""select * from temp""")
            result5=cursor.fetchall()
            
        if input_salary_lower:
            print("OLOLOLOsallow")
            querytabs[5]=input_salary_lower
            cursor.execute("""select * from temp where salary>=:x1""",[input_salary_lower])
            result6=cursor.fetchall()
        if input_salary_upper:
            print("OLOLOLO")
            querytabs[6]=input_salary_upper
            cursor.execute("""select * from temp where salary<=:x1""",[input_salary_upper])
            result7=cursor.fetchall()       

        
        querytabs[9]=input_agenull
        if input_agenull==['0']:#include non dob entries
            print("OLOLOLO")
            
            if input_age_lower:
                querytabs[7]=input_age_lower
                cursor.execute("""SELECT * FROM temp where age >=:x1 OR DOB IS NULL""",[input_age_lower])
                result8=cursor.fetchall()
            if input_age_upper:
                querytabs[8]=input_age_upper
                cursor.execute("""SELECT * FROM temp where age  <=:x1 OR DOB IS NULL""",[input_age_upper])
                result9=cursor.fetchall()
        else:#do not include non dob entries
            if input_age_lower:
                querytabs[7]=input_age_lower
                cursor.execute("""SELECT * FROM temp where age >=:x1""",[input_age_lower])
                result8=cursor.fetchall()
            if input_age_upper:
                querytabs[8]=input_age_upper
                cursor.execute("""SELECT * FROM temp where age <=:x1""",[input_age_upper])
                result9=cursor.fetchall()
        
        result=list(set(result1) & set(result2) & set(result3) & set(result4) & set(result5) & set(result6) & set(result7) & set(result8) & set(result9))
        print(result)
        info=[]


        for i in range(0,len(result)):
            cursor.execute("""SELECT phone FROM targetaudience_phone_visforce where serialno=:x1""",[result[i][0]])
            resultsupp=cursor.fetchall()
            info.append(Target_Audience(result[i][0],result[i][1],resultsupp,result[i][2],result[i][3],result[i][4],result[i][5],result[i][6],str(result[i][7]),result[i][8]))

        if len(result)!=0:
        #stats
            sal=[]
            age=[]
            email=[]
            countF=0
            countM=0
            for i in range(0,len(result)):
                sal.append(result[i][3])
                email.append(result[i][2])
                if result[i][8]!=None:               
                    age.append(result[i][8])
                if result[i][5]=="F":
                    countF=countF+1
                elif result[i][5]=='M':
                    countM=countM+1
            cursor.execute("select count(*) from targetaudience_main_visforce")
            count=cursor.fetchall()
            count=count[0][0]
            stats=[len(result),sum(sal)/len(sal),min(sal),max(sal),sum(age)/len(age),min(age),max(age),countF,countM,count]
        else:
            stats=[]
        print(stats) 

        if input_generate==['0']:#generate
            mailinglist=open("mailinglistTA.txt",'w+')
            for i in email:
                mailinglist.write(i+"; ")
            mailinglist.close()
        else:
            mailinglist=None
            
        cursor.execute("""drop view temp""")
        cursor.execute("""commit""")
        print(len(info))
        return render_template("emp_accessvisdatabases_targetaudience.html",info=info,querytabs=querytabs,user=user,stats=stats,mailinglist=mailinglist)
    
    else:
        #--------ACCESS FEEDBACKS-----------------
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Employee':
                emp_id=session["id"]
                usertype=session["usertype"]
            else:
                flash("Please login first")
                return redirect(url_for('login'))
                
        else:
            flash("Please login first")
            return redirect(url_for('login'))
        #-------------------------------------------
        cursor.execute("""select name from employee_phone_visforce where emp_id=:x1""",[emp_id])
        result=cursor.fetchall()
        user=[emp_id,result[0][0]]

        info=[]
        querytabs=["","","","","ALL",None,None,None,None,[]]
        stats=[]
        mailinglist=None        
        return render_template("emp_accessvisdatabases_targetaudience.html",info=info,querytabs=querytabs,user=user,stats=stats,mailinglist=mailinglist)
        




@app.route("/emp_accessvisdatabases_pastsales",methods=["POST", "GET"])
def emp_accessvisdatabases_pastsales():
    if request.method=="POST":
        #--------ACCESS FEEDBACKS-----------------
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Employee':
                emp_id=session["id"]
                usertype=session["usertype"]
            else:
                flash("Please login first")
                return redirect(url_for('login'))
                
        else:
            flash("Please login first")
            return redirect(url_for('login'))
        #-------------------------------------------
        cursor.execute("""select name from employee_phone_visforce where emp_id=:x1""",[emp_id])
        result=cursor.fetchall()
        user=[emp_id,result[0][0]]

        
        querytabs=["","","","","ALL",None,None]
        input_buyername=request.form["buyername"]
        input_dateofsale=request.form["dateofsale"]
        input_product=request.form["product"]
        input_orderid=request.form["orderid"]
        input_status=request.form["status"]
        input_price_lower=request.form["price_lower"]
        input_price_upper=request.form["price_upper"]


        cursor.execute("""select * from pastsales_visforce""")
        result=cursor.fetchall()
        result0=result1=result2=result3=result4=result5=result6=result

        

        if input_buyername:
            print("OLOLOLOname")
            querytabs[0]=input_buyername
            input_buyername="%"+input_buyername+"%"
            cursor.execute("""select * from pastsales_visforce where upper(buyername) like upper(:x1)""",[input_buyername])
            result0=cursor.fetchall()
            
        if input_dateofsale!="": #dateofsale
            print("queryyyy[1]",querytabs[1])
            print("OLOLOLOdate")
            htmldate=input_dateofsale
            print("htmldate",htmldate)
            print("input_dateofsale=",input_dateofsale)
            querytabs[1]=htmldate
            input_dateofsale=input_dateofsale[-2:]+"-"+getmonth(input_dateofsale[5:7])+"-"+input_dateofsale[2:4]
            cursor.execute("""select * from pastsales_visforce where dateofsale=:x1""",[input_dateofsale])
            result1=cursor.fetchall()
            
        if input_product:
            print("OLOLOLOpro")
            querytabs[2]=input_product
            input_product="%"+input_product+"%"
            cursor.execute("""select * from pastsales_visforce where upper(product) like upper(:x1)""",[input_product])
            result2=cursor.fetchall()
        if input_orderid:
            print("OLOLOLOorder")
            querytabs[3]=input_orderid
            input_orderid="%"+input_orderid+"%"
            cursor.execute("""select * from pastsales_visforce where upper(orderid) like upper(:x1)""",[input_orderid])
            result3=cursor.fetchall()
            
        if input_status=="delivered":
            print("OLOLOLOstatus")
            querytabs[4]=input_status
            input_status="%"+input_status+"%"
            cursor.execute("""select * from pastsales_visforce where upper(status) like upper(:x1)""",[input_status])
            result4=cursor.fetchall()
        elif input_status=="picked":
            print("OLOLOLOsta")
            querytabs[4]=input_status
            input_status="%"+input_status+"%"
            cursor.execute("""select * from pastsales_visforce where upper(status) like upper(:x1)""",[input_status])
            result4=cursor.fetchall()
        else:#all
            print("OLOLOLOsta")
            querytabs[4]==input_status
            cursor.execute("""select * from pastsales_visforce """)
            result4=cursor.fetchall()

        if input_price_lower:
            print("OLOLOLOlow")
            querytabs[5]=input_price_lower
            cursor.execute("""select * from pastsales_visforce where price>=:x1 """,[input_price_lower])
            result5=cursor.fetchall()
            
        if input_price_upper:
            print("OLOLOLOhigh")
            querytabs[6]=input_price_upper
            cursor.execute("""select * from pastsales_visforce where price<=:x1""",[input_price_upper])
            result6=cursor.fetchall()
        


        result=list(set(result0) & set(result1) & set(result1) & set(result2) & set(result3) & set(result4) & set(result5) & set(result6))


            
        info=[]
        for i in range(0,len(result)):
            info.append(Past_Sales(str(result[i][0]),result[i][1],result[i][2],result[i][3],result[i][4],result[i][5],result[i][6]))
            
        cursor.execute("select count(*) from pastsales_visforce")
        count=cursor.fetchall()
        
        if len(result)!=0:
            delivered=0
            picked=0
            price=[]
            for i in range(0,len(result)):
                price.append(result[i][5])
                if "delivered".upper() in (result[i][6]).upper() :
                    delivered=delivered+1
                elif "picked".upper() in (result[i][6]).upper():
                    picked=picked+1

            stats=[len(result),delivered,picked,round(sum(price)/len(price),3),min(price),max(price),sum(price),count[0][0]]
        else:
            stats=[]
        print("stats=",stats)
        return render_template("emp_accessvisdatabases_pastsales.html",info=info,user=user,querytabs=querytabs,stats=stats)

            
    else:
        #--------ACCESS FEEDBACKS-----------------
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Employee':
                emp_id=session["id"]
                usertype=session["usertype"]
            else:
                flash("Please login first")
                return redirect(url_for('login'))
                
        else:
            flash("Please login first")
            return redirect(url_for('login'))
        #-------------------------------------------
        cursor.execute("""select name from employee_phone_visforce where emp_id=:x1""",[emp_id])
        result=cursor.fetchall()
        user=[emp_id,result[0][0]]

        
        info=[]
        querytabs=["","","","","ALL",None,None]
        stats=[]
        return render_template("emp_accessvisdatabases_pastsales.html",info=info,user=user,querytabs=querytabs,stats=stats)









@app.route("/accessdatabases_emp",methods=["POST", "GET"])
def accessdatabases_emp():
    if request.method=="POST":
        #--------ACCESS FEEDBACKS-----------------
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Employee':
                emp_id=session["id"]
                usertype=session["usertype"]
            else:
                flash("Please login first")
                return redirect(url_for('login'))
                
        else:
            flash("Please login first")
            return redirect(url_for('login'))
        #-------------------------------------------
        cursor.execute("""select name from employee_phone_visforce where emp_id=:x1""",[emp_id])
        result=cursor.fetchall()
        user=[emp_id,result[0][0]]
        
        return render_template("accessdatabases_emp.html",user=user)
    
    else:
        #--------ACCESS FEEDBACKS-----------------
        if "id" in session and "usertype" in session:
            if session["usertype"]=='Employee':
                emp_id=session["id"]
                usertype=session["usertype"]
            else:
                flash("Please login first")
                return redirect(url_for('login'))
                
        else:
            flash("Please login first")
            return redirect(url_for('login'))
        #-------------------------------------------
        cursor.execute("""select name from employee_phone_visforce where emp_id=:x1""",[emp_id])
        result=cursor.fetchall()
        user=[emp_id,result[0][0]]
        
        return render_template("accessdatabases_emp.html",user=user)





#-----------------------------------------------------
@app.route("/logout",methods=["POST", "GET"])
def logout():
    if "id" in session:
        print("there is someone logged in",session["id"])
        id=session["id"]
        session.pop("id",None)
        flash("You have logged out")
        return redirect(url_for('login'))


    

        
if __name__=="__main__":#TO RUN THE WEBAPAGES
    app.run()
