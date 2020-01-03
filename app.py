from mongoengine import *
from datetime import datetime
import json
from flask import Flask, redirect, url_for, request,render_template
import jwt
import uuid
from flask_cors import CORS
import populateDB as popDB
from sendEmail import sendEmailQRcode

connect('vreapCMS_test', host='localhost', port=27017)

app = Flask(__name__)
CORS(app)


class User(Document):
    Name = StringField(required=True)
    Phone_No = StringField(required=True)
    Password = StringField(required=True)



class Admin(Document):
    Name = StringField(required=True)
    Phone_No = StringField(required=True)
    Email = StringField(required=True)
    Password = StringField(required=True)
    OTPValue = StringField(required=True)




def createAdmin(name, phoneNo, password, emailID):
    uuID = uuid.uuid4().hex
    data_to_save = Admin(Name=str(name),Phone_No=str(phoneNo),Email= str(emailID),OTPValue=uuID, Password=str(password))
    print("saving data of ",name)
    data_to_save.save()
    sendEmailQRcode(emailID, uuID)


def createUser(name, phoneNo, password):
    data_to_save = User(Name=str(name),Phone_No=str(phoneNo),Password=str(password))
    print("saving data of ",name)
    data_to_save.save()




@app.route('/')
def loginPage():
    return "server is up and runnning"


@app.route('/searchNo',methods = ['POST'])
def serch():
    reqData = request.get_json()
    cooky = reqData['cookie']
    phoneNo = reqData['searchPhoneNo']
    cookyDecoded = jwt.decode(cooky,'VRqqOFWEdA',algorithm='HS256')
    userList = User.objects(Phone_No = cookyDecoded['user_ID'])
    LeadData = popDB.Lead.objects(Phone_number = phoneNo)
    print(LeadData,phoneNo,type(phoneNo))
    LeadCallData = popDB.callData.objects(callNumber = phoneNo)
    if(len(userList) != 0 and userList[0]['Password'] == cookyDecoded['password']):
        if(len(LeadData)==0):
            return "No Entry"
        else:
            return render_template("SerchpageTemplate.html", leadData=LeadData[0], CallList=LeadCallData)
    else:
        return "relogin"


        


@app.route('/login',methods = ['POST'])
def login():
   if request.method == 'POST':
        content = request.get_json()
        print(str(content))
        userID = content['user_ID']
        password = content['userPassword']
        userList = User.objects(Phone_No = str(userID))

        if(len(userList) != 0):
            if(userList[0]['Password'] == password):
                encoded = jwt.encode({'user_ID': userID, 'password': password}, 'VRqqOFWEdA', algorithm='HS256')
                return encoded
            else:
                return "User phone number and Password dosent match"
        else:
            return "no user exists"



@app.route('/AdminLogin',methods = ['POST'])
def admin_login():
   if request.method == 'POST':
        content = request.get_json()
        print(str(content))
        adminID = content['admin_ID']
        password = content['userPassword']
        adminList = Admin.objects(Phone_No=str(adminID))

        if(len(adminList) != 0):
            if(adminList[0]['Password'] == password):
                encoded = jwt.encode({'admin_ID': adminID, 'password': password}, 'iceiceiceshroud', algorithm='HS256')
                return encoded
            else:
                return "Admion phone number and Password dosent match"
        else:
            return "no Admin exists"



@app.route('/getCallData_Admin',methods = ['POST'])
def admin_login():
    if request.method == 'POST':
        content = request.get_json()
        print(str(content))
        time_frame = content['temeFrame']
        date_month = content['dateMonth']
        call_user = content['callUser']

        if(time_frame != "" and date_month != "" and call_user != ""):
            if(time_frame == "day"):
                callData = popDB.callData.objects()



        else:
            return "retry With proper serch parameters"



@app.route('/userAuth',methods = ['POST'])
def userAuth():
    content = request.get_json()
    encoded_cookie = content['cookie']
    decoded_cookie = jwt.decode(encoded_cookie, 'VRqqOFWEdA', algorithms=['HS256'])
    print(decoded_cookie)
    userList = User.objects(Phone_No=str(decoded_cookie['user_ID']))
    CallList = popDB.callData.objects(called_by=userList[0]['Name'])
    if(len(userList)!=0):
        #render mainpage template
        return render_template("mainpageTemp.html",name=userList[0]['Name'],Call_List=CallList)
    else:
        return "login"


def getCallId():
    date = str(datetime.utcnow())
    outputStr = ""
    for n in date:
        outputStr = outputStr + numbers_to_strings(n)
    return outputStr

def numbers_to_strings(argument):
    switcher = {
        "0": "a",
        "1": "b",
        "2": "c",
        "3": "d",
        "4": "e",
        "5": "f",
        "6": "g",
        "7": "h",
        "8": "i",
        "9": "j",
        " ": "k",
        "-": "l",
        ".": "m",
        ":": "n"
    }
    return switcher.get(argument, "nothing")


@app.route('/addCallData',methods = ['POST'])
def addCallData():
    content = request.get_json()
    encoded_cookie = content['cooky']
    decoded_cookie = jwt.decode(encoded_cookie, 'VRqqOFWEdA', algorithms=['HS256'])
    userList = User.objects(Phone_No=str(decoded_cookie['user_ID']))
    if(len(userList)!=0):
        userName = userList[0]['Name']
        call_ID = getCallId()
        call_Number = content['callNumber']
        Call_Status = content['Call_Status']
        Why_Register = content['Why_Register']
        Potantial = content['Potantial']
        What_Discussed = content['What_Discussed']
        Whatsapp_Number = content['Whatsapp_Number']
        Whatsapp_sent = content['Whatsapp_sent']
        is_Followup_Needed = content['is_Followup_Needed']
        FollowUp_Instructions = content['FollowUp_Instructions']

        data_to_save = popDB.callData(CallID=call_ID,callNumber=call_Number,Call_Status=Call_Status,Why_Register=Why_Register,Potantial=Potantial,What_Discussed=What_Discussed,Whatsapp_Number=Whatsapp_Number,Whatsapp_sent=Whatsapp_sent,is_Followup_Needed=is_Followup_Needed,FollowUp_Instructions=FollowUp_Instructions,called_by=userName)
        data_to_save.save()

        return "Data Saved"
    else:
        return "login"


@app.route('/mainPage',methods = ['GET'])
def mainPage():
    return render_template('mainpage.html')





        



