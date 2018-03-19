from flask import Flask, render_template, url_for, request
from flaskext.mysql import MySQL
from flask_mail import Mail, Message
import pymysql.cursors
import json
import config

app = Flask(__name__)
mail = Mail(app)

connection = pymysql.connect(host=config.DB_HOST,
                             user=config.DB_USER,
                             password=config.DB_PASSWORD,
                             db=config.DB,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
                             
                             
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/registration')
def registration():
    return render_template('registration.html')
    
@app.route('/register/<sport>', methods = ['GET', 'POST'])
def register(sport):
    if request.method == "POST":
        try:
            data = request.get_json()
            if sport == 'football':
                for i in data:
                    if i == 'membernames':
                        memlist = data[i]
                        for k in range(0, len(memlist)):
                            memlist[k] = connection.escape(memlist[k])
                        data[i] = memlist
                    else:
                        if isinstance(data[i], int):
                            data[i] = connection.escape(int(data[i]))
                        elif i != 'email':
                            data[i] = connection.escape(data[i])
                print(data)
                existflag = 0
                existflag2 = 0
                jerseyflag = 0
                with connection.cursor() as cursor:
                    existquery = '''SELECT * FROM footballregistrations WHERE TeamName="%s"'''
                    existquery2 = '''SELECT * FROM footballregistrations WHERE Email="%s"'''
                    cursor.execute(existquery % data['teamname'])
                    if len(cursor.fetchall()) > 0:
                        existflag = 1
                        
                    cursor.execute(existquery2 % data['email'])
                    if len(cursor.fetchall()) > 0:
                        existflag2 = 1
                    
                    allquery = '''SELECT * FROM footballregistrations'''
                    cursor.execute(allquery)
                    for i in cursor.fetchall():
                        if i['JerseyColor'] == data['jerseycolor'].lower():
                            jerseyflag = 1
                            break
            
                if existflag == 1:
                    return json.dumps({'Status':'Not Registered', 'Message': 'Error, that team name already exists'})
                elif existflag2 == 1:
                    return json.dumps({'Status':'Not Registered', 'Message': 'Error, that email already exists'})
                elif jerseyflag == 1:
                    return json.dumps({'Status':'Not Registered', 'Message': 'Error, that jersey color is taken'})
                else:
                    teamname = data['teamname']
                    membernames = ",".join(data['membernames'])
                    print(membernames)
                    registername = data['registername']
                    paymentmode = data['paymenttype']
                    mobileno = data['mobileno']
                    alternateno = data['alternateno']
                    email = data['email']
                    noofmembers = data['noofmembers']
                    jerseycolor = data['jerseycolor'].lower()
                    with connection.cursor() as cursor:
                        query = '''INSERT INTO footballregistrations (TeamName, MemberNames, RegistrationPerson, PaymentMode, MobileNo, AlternateNo, Email, NoOfMembers, JerseyColor) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''' #.format(teamname, membernames, registername, paymentmode, mobileno, alternateno, email, noofmembers)
                        print(query)
                        insertdata = (teamname, membernames, registername, paymentmode, mobileno, alternateno, email, noofmembers, jerseycolor)
                        cursor.execute(query, insertdata)
        
                    connection.commit()
            
                    msg = Message('We have a new registration under Football for Sports for Change', sender = config.MAIL_USERNAME, recipients = [config.RECIPIENT_1, config.RECIPIENT_2, config.RECIPIENT_3, config.RECIPIENT_4, config.RECIPIENT_5])
                    msg.body = "Team name: {} \nRegistration Person: {}\nNo. of members in the team: {}\nMember Names: {}\nMobile no: {}\nAlternate no: {} \nPayment mode chosen: {} \nJersey color: {}".format(teamname, registername, noofmembers, membernames, mobileno, alternateno, paymentmode, jerseycolor)
                    mail.send(msg)
            
                    msg2 = Message('Confirming your registration for Sports for Change', sender = config.MAIL_USERNAME, recipients = [data['email']])
                    paymsg = ''
                    if paymentmode == "payTM":
                        paymsg = "You have chosen to pay the registration fee through PayTM. To make the PayTM payment for the event, please pay Samaksh Goel of IBDP 1 studying in Oakridge International School. His mobile no. is +919036492611"
                    else:
                        paymsg = "You have chosen to pay the registration fee by cash. Please make the cash payment once you arrive at the venue on the event day"
                
                    msg2.body = "Thank you for registering under Football for Sports for Change. This is to confirm that you have registered for the event under the name of {} and under the team name of {}. {}".format(registername, teamname, paymsg)
                    mail.send(msg2)
            elif sport == 'chess':
                for i in data:
                    if i != 'email' and not isinstance(data[i], int):
                        data[i] = connection.escape(data[i])
                print(data)
                existflag = 0
                existflag2 = 0
                with connection.cursor() as cursor:
                    existquery = '''SELECT * FROM chessregistrations WHERE Name="%s"'''
                    cursor.execute(existquery % data['name'])
                    if len(cursor.fetchall()) > 0:
                        existflag = 1
                        
                    existquery2 = '''SELECT * FROM chessregistrations WHERE Email="%s"'''
                    cursor.execute(existquery2 % data['email'])
                    if len(cursor.fetchall()) > 0:
                        existflag2 = 1
                if existflag == 1:
                    return json.dumps({'Status':'Not Registered', 'Message': 'Error, that name has already registered'})
                elif existflag2 == 1:
                    return json.dumps({'Status':'Not Registered', 'Message': 'Error, that email has already registered'})
                else:
                    name = data['name']
                    age = data['age']
                    paymentmode = data['paymenttype']
                    mobileno = data['mobileno']
                    print(mobileno)
                    email = data['email']
                    category = data['category']
                    UKCAID = "true" if data['UKCAID'] == 1 else "false"
                    
                    with connection.cursor() as cursor:
                        query = '''INSERT INTO chessregistrations (Name, Email, MobileNo, Age, Category, PaymentMode, HasUKCA) VALUES (%s, %s, %s, %s, %s, %s, %s)'''
                        insertdata = (name, email, mobileno, age, category, paymentmode, data['UKCAID'])
                        cursor.execute(query, insertdata)
        
                    connection.commit()
            
                    msg = Message('We have a new registration under Chess for Sports for Change', sender = config.MAIL_USERNAME, recipients = [config.RECIPIENT_1, config.RECIPIENT_2, config.RECIPIENT_3, config.RECIPIENT_4, config.RECIPIENT_5])
                    msg.body = "Name: {} \nEmail: {} \nMobile no.: {}\n Age: {}\nCategory: {}\nPayment mode chosen: {}\nHas an UKCA ID: {}".format(name, email, mobileno, age, category, paymentmode, UKCAID)
                    mail.send(msg)
            
                    msg2 = Message('Confirming your registration for Sports for Change', sender = config.MAIL_USERNAME, recipients = [email])
                    paymsg = ''
                    msgcategory = ''
                    if category == 'u8':
                        msgcategory = "Under 8"
                    elif category == 'u12':
                        msgcategory = "Under 12"
                    elif category == "u16":
                        msgcategory = "Under 16"
                    if paymentmode == "payTM":
                        paymsg = "You have chosen to pay the registration fee through PayTM. To make the PayTM payment for the event, please pay Samaksh Goel of IBDP 1 studying in Oakridge International School. His mobile no. is +919036492611"
                    else:
                        paymsg = "You have chosen to pay the registration fee by cash. To make the cash payment, one of our representatives will get in touch with you soon. If the representative does not get in touch with you in the next 24 hours, please contact us through the contact number provided at the bottom of the website. Please do keep in mind that you must make the payment before 9th of April"
                
                    msg2.body = "Thank you for registering under Chess for Sports for Change. This is to confirm that you have registered for the event under the name of {} and under the {} category. {}".format(name, msgcategory, paymsg)
                    mail.send(msg2)
            
            elif sport == 'basketball':
                print("soon")
        finally:
            print("There was an attempt to register!")

        return json.dumps({'Status':'Registered', 'Message': 'Successfully registered'});
        
        
@app.route('/termsandconditions')
def t_and_c():
    return render_template('t&c.html')
    
@app.route('/confirmpayment')
def confirmpayment():
    return render_template('confirmpayment.html')
    
@app.route('/checkpass', methods = ['POST'])
def checkpass():
    if request.method == "POST":
        data = request.get_json()
        print(data)
        if data['passphrase'] == config.PASSPHRASE:
            return json.dumps({'correct': 'true'})
        else:
            return json.dumps({'correct':'false'})
            
            
@app.route('/getallregistrations')
def getallteams():
    return render_template('getallregistrations.html')
    
@app.route('/getteamsafterauth/<sport>', methods = ['GET', 'POST'])
def getteamsafterauth(sport):
    if request.method == "POST":
        data = request.get_json()
        if data['passphrase'] == config.PASSPHRASE2:
            with connection.cursor() as cursor:
                if sport == 'football':
                    cursor.execute('SELECT * FROM footballregistrations');
                    querydata = cursor.fetchall()
                    return json.dumps({'success':'true', 'teams': querydata})
                elif sport == 'chess':
                    cursor.execute('SELECT * FROM chessregistrations');
                    querydata = cursor.fetchall()
                    return json.dumps({'success':'true', 'data': querydata})
                elif sport == 'basketball':
                    cursor.execute('SELECT * FROM basketballregistrations');
                    querydata = cursor.fetchall()
                    return json.dumps({'success':'true', 'teams': querydata})
                    
        else:
            return json.dumps({'success': 'false'})

@app.route('/confirmpayment', methods = ['POST'])
def confirmteampayment():
    data = request.get_json()
    name = connection.escape(data['name'])
    sport = data['sport']
    repass = data['repass']
    if repass != config.PASSPHRASE:
        return json.dumps({'success': 'false', 'message': 'Error, incorrect pass phrase'})
    else:
        print(sport == 'chess')
        with connection.cursor() as cursor:
            if sport == 'football':
                query = '''SELECT * FROM footballregistrations WHERE TeamName="%s"''' % str(name)
            elif sport == 'chess':
                 query = '''SELECT * FROM chessregistrations WHERE Name="%s"''' % str(name)
                 print(query)
            elif sport == 'basketball':
                 query = '''SELECT * FROM basketballregistrations WHERE TeamName="%s"''' % str(name)
            cursor.execute(query)
            dbdata = cursor.fetchall()
            print(dbdata)
            if len(dbdata) == 0:
                notexistmessage = 'Error, that team does not exist' if (sport == 'football' or sport == 'basketball') else 'Error, a registration under that name does not exist'
                return json.dumps({'success': 'false', 'message': notexistmessage})  
            else:
                if dbdata[0]['HasPaid'] == 1:
                    returnmessage = 'Error, that team has already paid' if (sport == 'football' or sport == 'basketball') else 'Error, the registration under that name has already paid'
                    return json.dumps({'success': 'false', 'message': returnmessage})
                else:
                    insertquery = ''
                    if sport == 'football':
                        insertquery = '''UPDATE footballregistrations SET HasPaid=1 WHERE TeamName="%s"''' % str(name)
                    elif sport == 'basketball':
                        insertquery = '''UPDATE basketballregistrations SET HasPaid=1 WHERE TeamName="%s"''' % str(name)
                    elif sport == 'chess':
                        insertquery = '''UPDATE chessregistrations SET HasPaid=1 WHERE Name="%s"''' % str(name)
                    cursor.execute(insertquery)
                
                    connection.commit()
                    
                    if sport == 'football':
                        cursor.execute('''SELECT Email FROM footballregistrations WHERE TeamName="%s"''' % str(name))
                    elif sport == 'basketball':
                        cursor.execute('''SELECT Email FROM basketballregistrations WHERE TeamName="%s"''' % str(name))
                    elif sport == 'chess':
                        cursor.execute('''SELECT Email FROM chessregistrations WHERE Name="%s"''' % str(name))
                    
                    data = cursor.fetchall()
                    email = data[0]['Email']
                    
                    msg = Message('A registration has completed payment', sender = config.MAIL_USERNAME, recipients = [config.RECIPIENT_1, config.RECIPIENT_2, config.RECIPIENT_3, config.RECIPIENT_4, config.RECIPIENT_5])
                    msg.body = "The registration under the name {} has completed the payment successfully. Samaksh you better have the cash.".format(name)
                    mail.send(msg)
                    
                    msg2 = Message('Payment confirmation for the Sports for Change event', sender = config.MAIL_USERNAME, recipients = [email])
                    msg2.body = "Thank you for your payment for the Sports for Change event. This is to confirm that the payment has been completed successfully. You have been confirmed under {}. We hope to see you there :)".format(sport)
                    mail.send(msg2)
                    
                    return json.dumps({'success': 'true', 'message': 'Successfully updated!'})
    

@app.route('/contactus')
def contactus():
    return render_template('contact.html')
    
@app.route('/submitquery', methods = ['GET', 'POST'])
def submitquery():
    if request.method == "POST":
        data = request.get_json()
        print(data)
        name = data['name']
        email = data['email']
        question = data['question']
        detail = data['detail']
        
        msg = Message('A new query regarding Sports for Change', sender = config.MAIL_USERNAME, recipients = [config.RECIPIENT_1, config.RECIPIENT_2, config.RECIPIENT_3, config.RECIPIENT_4, config.RECIPIENT_5])
        msg.body = "Name: {} \nEmail: {} \nQuestion: {} \nQuery in detail: {} \n \nPlease reply to the above email to resolve the query".format(name, email, question, detail)
        mail.send(msg)
        
        msg = Message('Confirmation regarding your query for the Sports for Change event', sender = config.MAIL_USERNAME, recipients = [email])
        msg.body = "This is to confirm that you've submitted a query for the Sports for Change event asking {}. One of our representatives will get back to you shortly regarding the query. Please expect to receive a return mail to this email address".format(question)
        mail.send(msg)
        
        return json.dumps({'status':'true'})

@app.route('/sponsors')
def sponsors():
    return render_template('sponsors.html')
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)