from email import message
from flask import Flask, redirect, url_for, request,render_template,flash,session
import numpy as np
import mysql.connector
from sympy import Id

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="SBME2024"
)


mycursor = mydb.cursor()
app = Flask(__name__,template_folder="templates")

@app.route('/')
def hello_name():
   return render_template('index.html')


@app.route('/doctor', methods = ['POST', 'GET'])
def doctorregistration():
   msg=" "
   if request.method == 'POST': ##check if there is post data
      Fname = request.form['First Name']
      Lname = request.form['Last Name']
      phonenumber = request.form['Mobile Number']
      Email = request.form['Email Address']
      Password = request.form['Password']
      mycursor.execute("SELECT * FROM Doctor WHERE Email  = (%s)", (Email,))
      checkdoctor = mycursor.fetchone()
      if checkdoctor:
         msg="the account already exsist"
         return render_template('doctors.html',msg=msg)
      else:
         sql = "INSERT INTO Doctor (Password,Fname, Lname, Email, Phonenumber) VALUES (%s, %s, %s, %s, %s)"
         val = (Password,Fname, Lname, Email, phonenumber)
         mycursor.execute(sql, val)
         mydb.commit() 
         session['loggedin'] = True
         mycursor.execute("SELECT * FROM Doctor WHERE Email = (%s) ", (Email,))
         checkdoctor = mycursor.fetchone()
         return render_template('eachdoctor.html',checkdoctor=checkdoctor)
   else:
      return render_template('doctors.html')

@app.route('/about')
def about():
   return render_template('about.html')


@app.route('/appointment',methods = ['POST', 'GET'])
def appointment():
   if request.method == 'POST': ##check if there is post data
      name = request.form['name']
      email = request.form['email']
      mobilenumber = request.form['number']
      selecteddoctor=request.form['DOCTORS']
      print(selecteddoctor)
      selecteddate= request.form['date']
      selectedtime=request.form['Time']
      mycursor.execute("SELECT * FROM BOOKING WHERE time= %s AND date= %s AND d_id= %s" , (selectedtime,selecteddate,selecteddoctor))
      checkappointment = mycursor.fetchone()
      if checkappointment:
         msg='This appointment is already booked'
         return render_template('appointment.html',msg=msg)
      else:   
         mycursor.execute("INSERT INTO patient (name, Email, phonenumber) VALUES (%s,%s,%s)", (name,email,mobilenumber))
         mydb.commit()
         sql="INSERT INTO BOOKING ( p_email,d_id, date, time) VALUES (%s,%s,%s,%s)"
         mycursor.execute(sql,(email,selecteddoctor, selecteddate, selectedtime))
         mydb.commit()
         msg='Your apointment is booked successfully'
         return render_template('appointment.html',msg=msg)
   else:
      mycursor.execute("SELECT Fname FROM Doctor")
      myresult = mycursor.fetchall()
      data={
         'rec':myresult,
      }
      
      return render_template('appointment.html',data=data)



@app.route('/cancel',methods = ['POST', 'GET'])
def cancel():
   if request.method == 'POST': ##check if there is post data
      email = request.form['email']
      selecteddoctor=request.form['Doctors']
      mycursor.execute("SELECT * FROM BOOKING WHERE d_id= %s AND p_email= %s" , (selecteddoctor,email))
      checkappointment = mycursor.fetchone()
      if checkappointment:
         sql = "DELETE FROM BOOKING where d_id= %s AND p_email= %s "
         val = (selecteddoctor,email)
         mycursor.execute(sql, val)
         mydb.commit()
         msg= 'Your appointment is canceled'
         return render_template('cancel.html', msg=msg)
      else:   
         msg= 'This appointment not found '
         return render_template('cancel.html', msg=msg)
   else:
      return render_template('cancel.html')


@app.route('/contact',methods = ['POST', 'GET'])
def contact():
   if request.method == 'POST':
      email = request.form['email']
      name=request.form['name']
      subject=request.form['subject']
      number=request.form['number']
      message=request.form['message']
      sql="insert into contact (name, Email, subject, message, number) VALUES (%s,%s,%s,%s,%s)"
      val=(name,email,subject,message,number)
      mycursor.execute(sql, val)
      mydb.commit()
      msg='your message is sent'
      return render_template('contact.html',msg=msg)
   else:   
      return render_template('contact.html')


@app.route('/dataofdoctor',methods = ['POST', 'GET'])
def dataofdoctor():
   if request.method == 'GET': ##check if there is post data
      result= mycursor.execute("SELECT * FROM Doctor")  
      myresult = mycursor.fetchall()
      return render_template('dataofdoctor.html',myresult=myresult)
   else: 
      return render_template('dataofdoctor.html')        

@app.route('/dataofpatient',methods = ['POST', 'GET'])
def dataofpatient():
   if request.method == 'GET': ##check if there is post data
      result= mycursor.execute("SELECT * FROM Patient")  
      myresult = mycursor.fetchall()
      return render_template('dataofpatient.html',myresult=myresult)
   else:
      return render_template('dataofpatient.html')
   
@app.route('/eachdoctor')
def eachdoctor():
    if 'loggedin' in session:
        mycursor.execute('SELECT * FROM Employee WHERE id = % s', (session['id'], ))
        checkdoctor = mycursor.fetchone()    
    return render_template('eachdoctor.html',checkdoctor = checkdoctor)

@app.route('/eachpatient')
def eachpatient():
   mycursor.execute("SELECT * FROM booking JOIN patient ON p_email=Email")
   myresult = mycursor.fetchall()
   return render_template('eachpatient.html',patientsData = myresult)

@app.route('/reviewpatient')
def reviewpatient():
    if 'loggedin' in session:
        mycursor.execute('SELECT Fname,date,time FROM booking JOIN Doctor ON d_id=id WHERE p_email = % s', (session['Email'],))
        checkpatient = mycursor.fetchall()    
        return render_template("reviewpatient.html",checkpatient=checkpatient)

   
@app.route('/employee')
def employee():
      if 'loggedin' in session:
        mycursor.execute('SELECT * FROM Employee WHERE id = % s', (session['id'], ))
        checkemployee = mycursor.fetchone()    
        return render_template("employee.html", checkemployee = checkemployee)


@app.route('/login', methods = ['POST', 'GET'])
def login():
   msg=""
   if request.method == 'POST': ##check if there is post data
      username = request.form['userid']
      Password = request.form['usrpsw']
      mycursor.execute("SELECT * FROM Doctor WHERE id = (%s) AND Password = (%s)", (username, Password))
      checkdoctor = mycursor.fetchone()
      mycursor.execute('SELECT * FROM booking WHERE d_id = (%s)', (username,))
      result = mycursor.fetchone()  
      if checkdoctor:
         session['loggedin'] = True
         return render_template('eachdoctor.html',checkdoctor=checkdoctor,result=result)
         
      else:
         mycursor.execute("SELECT * FROM Employee WHERE id = (%s) AND Password = (%s)", (username, Password))
         checkemployee = mycursor.fetchone()
         if checkemployee:
            session['loggedin'] = True
            return render_template('employee.html',checkemployee=checkemployee) 
         else:
            msg= 'wrong login'
            return render_template('login.html', msg= msg)
   else:
      return render_template('login.html')

@app.route('/patient')
def patient():
   return render_template('patient.html')


@app.route('/privacy')
def privacy():
   return render_template('privacy.html')
   

@app.route('/registration', methods = ['POST', 'GET'])
def registration():
   if request.method == 'POST': ##check if there is post data
      Fname = request.form['First Name']
      Lname = request.form['Last Name']
      phonenumber = request.form['Mobile Number']
      Email = request.form['Email Address']
      Password = request.form['Password']
      mycursor.execute("SELECT * FROM Employee WHERE Email  = (%s)", (Email,))
      checkemployee = mycursor.fetchone()
      if checkemployee:
         msg="the account already exsist"
         return render_template('registration.html',msg=msg)
      else:
         sql = "INSERT INTO Employee (Password,Fname, Lname, Email, Phonenumber) VALUES (%s, %s, %s, %s, %s)"
         val = (Password,Fname, Lname, Email, phonenumber)
         mycursor.execute(sql, val)
         mydb.commit() 
         session['loggedin'] = True
         mycursor.execute("SELECT * FROM Employee WHERE Email = (%s) ", (Email,))
         checkemployee = mycursor.fetchone()
         return render_template('employee.html',checkemployee=checkemployee)
   else:
      msg="You are already exsist"
      return render_template('registration.html')
@app.route('/review', methods = ['POST', 'GET'])
def review():
   if request.method == 'POST':
      name=request.form['name']
      email=request.form['email']
      number=request.form['number']
      mycursor.execute("SELECT * FROM Patient WHERE Email = (%s) ", (email,))
      checkpatient = mycursor.fetchone()
      if checkpatient:
         session['in'] = True
         result=mycursor.execute("SELECT Doctor.Fname,booking.date,booking.time FROM Doctor INNER JOIN booking ON id=d_id WHERE p_email = (%s) ", (email,))
         checkpatient = mycursor.fetchone()
         return render_template('reviewpatient.html',checkpatient=checkpatient)
      else:
         msg='This patient not found'
         return render_template('review.html',msg=msg)
   else:
         msg=" "
         return render_template('review.html')


@app.route('/setting')
def setting():
   return render_template('setting.html')

@app.route('/contact1')
def contact1():
   result= mycursor.execute("SELECT subject,message FROM contact")  
   myresult = mycursor.fetchall()
   return render_template('contact1.html',myresult=myresult)


@app.route('/terms')
def terms():
   return render_template('terms.html')


@app.route('/device',methods = ['POST', 'GET'])
def device():
    if request.method == 'POST': 
      name = request.form['name']
      code = request.form['code']
      company = request.form['company']
      Supervisor = request.form['Supervisor']
      maintenance = request.form['ma']
      work = request.form['work']
      mycursor.execute("SELECT * FROM Devices WHERE dcode = (%s)", (code,))
      checkdevice = mycursor.fetchone()
      if checkdevice:
         msg="Device already exsist please check the list"
         return render_template('device.html',msg=msg)
      else:   
         sql = "INSERT INTO Devices (dcode , supervisor , company , m_state , w_state , dname ) VALUES (%s, %s, %s, %s, %s, %s)"
         val = (code, Supervisor,company, maintenance,work,name)
         mycursor.execute(sql, val)
         mydb.commit() 
         msg="Your device is added"
         return render_template('device.html',msg=msg)
    else:  
     
     return render_template('device.html')


@app.route('/dataofdevice')
def dataofdevice():
    result= mycursor.execute("SELECT * FROM Devices")  
    myresult = mycursor.fetchall()
    return render_template('dataofdevice.html',myresult=myresult)

@app.route('/update',methods=['POST','GET'])
def update():
    if request.method == 'POST':
        code = request.form['code']
        maintenance = request.form['ma']
        work = request.form['work']
        mycursor.execute("SELECT * FROM Devices WHERE dcode = (%s)", (code,))
        checkdevice = mycursor.fetchone()
        if checkdevice:
         mycursor.execute("""
                  UPDATE Devices
                  SET w_state=%s, m_state=%s
                  WHERE dcode=%s
               """, (work, maintenance, code))
         mydb.commit() 
         msg="Your device is updated"
         return render_template('device.html',msg=msg)
        else:
           msg= 'Device does not exsist'
           return render_template('update.html', msg= msg)

    return render_template('update.html')


@app.route('/appointmentofdoctor')
def appointmentofdotor():
    if 'loggedin' in session:
        mycursor.execute('SELECT name, p_email, date,time FROM booking JOIN Patient ON p_email=Email WHERE d_id = % s', (session['id'],))
        myresult = mycursor.fetchall()    
        return render_template("appointmentofdoctor.html",myresult=myresult)



if __name__ == '__main__':
   app.secret_key = 'SECRET KEY FOR PROJECT'
   app.run(debug=True)
   
