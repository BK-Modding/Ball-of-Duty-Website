from flask import Flask, render_template, url_for, request
from flaskext.mysql import MySQL
import pymysql.cursors
import json

app = Flask(__name__)

connection = pymysql.connect(host='0.0.0.0',
                             user='root',
                             password='toor',
                             db='ballduty',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/registration')
def registration():
    return render_template('registration.html')
    
@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == "POST":
        try:
            data = request.get_json()
            for i in data:
                if i == 'membernames':
                    memlist = data[i]
                    for k in range(0, len(memlist)):
                        memlist[k] = connection.escape(memlist[k])
                    data[i] = memlist
                else:
                    if isinstance(data[i], int):
                        data[i] = connection.escape(int(data[i]))
            print(data)
            teamname = data['teamname']
            membernames = ",".join(data['membernames'])
            print(membernames)
            registername = data['registername']
            paymentmode = data['paymenttype']
            mobileno = data['mobileno']
            alternateno = data['alternateno']
            email = data['email']
            noofmembers = data['noofmembers']
            with connection.cursor() as cursor:
                query = '''INSERT INTO registrations (TeamName, MemberNames, RegistrationPerson, PaymentMode, MobileNo, AlternateNo, Email, NoOfMembers) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''' #.format(teamname, membernames, registername, paymentmode, mobileno, alternateno, email, noofmembers)
                print(query)
                insertdata = (teamname, membernames, registername, paymentmode, mobileno, alternateno, email, noofmembers)
                cursor.execute(query, insertdata)
        
            connection.commit()
        finally:
            connection.close()
            
        samakshdetails = ''
        if paymentmode == "'payTM'":
            samakshdetails = "To make the payTM payment for the event, please pay Samaksh Goel of IBDP 1 studying in Oakridge International School. His mobile no. is 9036492611"

        return json.dumps({'status':'Registered', 'samakshdetails':samakshdetails});
    
@app.route('/termsandconditions')
def t_and_c():
    return render_template('t&c.html')
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)