import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
from firebase_admin import storage
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL':'https://attendancemanagementsyst-de005-default-rtdb.firebaseio.com/',
    'storageBucket':'attendancemanagementsyst-de005.appspot.com'
})

reference = db.reference('Student') # Reference path of our db

data = {
    '103':{
        'Name' : "Awais Tahseen",
        'Department': "DCIS",
        'Last Attendance': '2023-02-14 12:22:45',
        'Attendance':4
    },
    '104':{
            'Name' : "Elizbeth Olsen",
            'Department': "MCU",
            'Last Attendance': '2023-02-14 14:22:45',
            'Attendance':10
        },
    '105':{
            'Name' : "Robert Downy Jr",
            'Department': "MCU",
            'Last Attendance': '2023-02-16 02:12:45',
            'Attendance': 15
        }
}

# Uploading details
for key, value in data.items():
    reference.child(key).set(value)

# Uploading images
folder_path='Images'
for image in os.listdir(folder_path):
    filename=folder_path+'/'+image
    bucket=storage.bucket()
    blob=bucket.blob(filename)
    blob.upload_from_filename(filename)