from mongoengine import *
from datetime import datetime
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_Secrete.json', scope)
client = gspread.authorize(creds)

# sheet = client.open("test for db").sheet1
# list_of_hashes = sheet.get_all_records()
# print(list_of_hashes)



def getGSheetsData():
    sheet = client.open("test for db").sheet1
    list_of_hashes = sheet.get_all_records()
    a = 0
    b = 0
    for dp in list_of_hashes:
        if (len(Lead.objects(Phone_number=str(dp["Phone number"]))) == 0):
            data_to_save = Lead(Timestamp=dp["Timestamp"],Name=str(dp["Name"]),Email=str(dp["Email"]),Phone_number=str(dp["Phone number"]),Village_Name=str(dp["Village Name"]),District=str(dp["District"]),PIN_Code=str(dp["PIN Code"]),State=str(dp["State"]),Highest_Qualification=str(dp["Highest Qualification"]))
            data_to_save.save()
            a = a+1
        else:
            b = b+1



connect('vreapCMS_test', host='localhost', port=27017)

class callData(Document):
    CallID = StringField(required=True)
    callNumber = StringField(required=True)
    Call_Status = StringField(required=True)
    Why_Register = StringField(required=True)
    Potantial = StringField(required=True)
    What_Discussed = StringField(required=True)
    Whatsapp_Number = StringField(required=True)
    Whatsapp_sent = StringField(required=True)
    is_Followup_Needed = StringField(required=True)
    FollowUp_Instructions = StringField(required=True)
    called_by = StringField(required=True)
    Date_Time = StringField(default=str(datetime.utcnow()))




class Lead(Document):
    Timestamp = StringField(required=True)
    Name = StringField(required=True)
    Email = StringField(required=True)
    Phone_number = StringField(required=True)
    Village_Name = StringField(required=True)
    District = StringField(required=True)
    PIN_Code = StringField(required=True)
    State = StringField(required=True)
    Highest_Qualification = StringField(required=True)
