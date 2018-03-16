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
            existflag = 0
            with connection.cursor() as cursor:
                existquery = '''SELECT * FROM registrations WHERE TeamName="%s"'''
                cursor.execute(existquery % data['teamname'])
                if len(cursor.fetchall()) > 0:
                    existflag = 1
            
            if existflag == 1:
                return json.dumps({'Status':'Not Registered', 'Message': 'Error, that team name already exists'});
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
                with connection.cursor() as cursor:
                    query = '''INSERT INTO registrations (TeamName, MemberNames, RegistrationPerson, PaymentMode, MobileNo, AlternateNo, Email, NoOfMembers) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''' #.format(teamname, membernames, registername, paymentmode, mobileno, alternateno, email, noofmembers)
                    print(query)
                    insertdata = (teamname, membernames, registername, paymentmode, mobileno, alternateno, email, noofmembers)
                    cursor.execute(query, insertdata)
        
                connection.commit()
            
                msg = Message([])
                msg.body = "Team name: {} \n Registration Person: {} \n No. of members in the team: {} \n Member Names: {} \n Mobile no: {} \n Alternate no: {} \n Payment mode chosen: {}".format(teamname, registername, noofmembers, membernames, mobileno, alternateno, paymentmode)
                mail.send(msg)
            
                msg2 = Message('Confirming your registration for Ball of Duty', sender = 'ball.of.duty.bangalore@gmail.com', recipients = [config.RECIPIENT_1, config.RECIPEINT_2, config.RECIPIENT_3, config.RECIPIENT_4, config.RECIPIENT_5])
                paymsg = ''
                if paymentmode == "payTM":
                    paymsg = "You have chosen to pay the registration fee through PayTM. To make the PayTM payment for the event, please pay Samaksh Goel of IBDP 1 studying in Oakridge International School. His mobile no. is +919036492611"
                else:
                    paymsg = "You have chosen to pay the registration fee by cash. Please make the cash payment once you arrive at the venue on the event day"
                
                msg2.body = "Thank you for your registration for Ball of Duty. This is to confirm that you have registered for the event under the name of {} and under the team name of {}. {}".format(registername, teamname, paymsg)
                mail.send(msg2)
        finally:
            print("Possible registration!")

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
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)