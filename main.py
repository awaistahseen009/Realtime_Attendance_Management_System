import cv2 as cv
import pickle
import numpy as np
import face_recognition
from firebase_admin import credentials
from firebase_admin import db
import firebase_admin
import cvzone
from datetime import datetime
from test import test
from firebase_admin import storage
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL':'https://attendancemanagementsyst-de005-default-rtdb.firebaseio.com/',
    'storageBucket':'attendancemanagementsyst-de005.appspot.com'
})

reference = db.reference('Student') # Reference path of our db

cap = cv.VideoCapture(0)

# cap.set(3,1280)
# cap.set
encoding_with_ids=pickle.load(open('encoding_with_ids.pkl','rb'))
# print(encoding_with_ids[0])
# Destructuring the list
encodings , student_ids= encoding_with_ids
print(student_ids)
counter=0
id_=-1


def add_text_to_frame(frame, text, foreground_color='green', border_color='black', name=None):
    font = cv.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2

    # Get text size to calculate the position of the text box
    text_size = cv.getTextSize(text, font, font_scale, font_thickness)[0]

    # Calculate the position of the text box with padding
    text_x = int((frame.shape[1] - text_size[0]) / 2)
    text_y = int((frame.shape[0] + text_size[1]) / 2)

    # Draw white background
    cv.rectangle(frame, (text_x - 10, text_y - text_size[1] - 10), (text_x + text_size[0] + 10, text_y + 10),
                  (255, 255, 255), cv.FILLED)

    # Draw border
    cv.putText(frame, text, (text_x, text_y), font, font_scale, (0, 0, 0), font_thickness + 2, lineType=cv.LINE_AA)

    # Draw foreground with specified color
    if foreground_color.lower() == 'green':
        foreground_color = (0, 255, 0)  # Green color in BGR
    elif foreground_color.lower() == 'red':
        foreground_color = (0, 0, 255)  # Red color in BGR
    else:
        foreground_color = (0, 0, 0)  # Default to black

    cv.putText(frame, text, (text_x, text_y), font, font_scale, foreground_color, font_thickness, lineType=cv.LINE_AA)

    # Add name to the text
    if name:
        text_with_name = f"{text} {name}"
        text_size_with_name = cv.getTextSize(text_with_name, font, font_scale, font_thickness)[0]
        text_x_with_name = int((frame.shape[1] - text_size_with_name[0]) / 2)
        text_y_with_name = text_y + text_size[1] + 30  # Position below the existing text
        cv.putText(frame, text_with_name, (text_x_with_name, text_y_with_name), font, font_scale, foreground_color,
                    font_thickness, lineType=cv.LINE_AA)

    return frame


while True:
    success,image = cap.read()
    resized_image=cv.resize(image, (0,0), None , 0.25,0.25)
    resized_image=cv.cvtColor(resized_image, cv.COLOR_BGR2RGB)
    curr_face_location=face_recognition.face_locations(resized_image)
    curr_face_encodings=face_recognition.face_encodings(resized_image,curr_face_location)
    for cfe, cfl in zip(curr_face_encodings , curr_face_location):
        matched_faces=face_recognition.compare_faces(encodings, cfe)
        face_similarity_distance=face_recognition.face_distance(encodings,cfe)
        match_index=np.argmin(face_similarity_distance)
        if matched_faces[match_index]:
            if counter == 0:
                counter = 1
        else:
            print("Unknown face detected")
        y1,x2,y2,x1=cfl
        y1, x2, y2, x1=y1*4,x2*4,y2*4,x1*4
        bounding_box=x1,y1,x2-x1,y2-y1
        cvzone.cornerRect(image,bounding_box, rt=0 )
        id_=student_ids[match_index]
        if counter!=0:
            if counter==1:

                student_data=db.reference(f'Student/{id_}').get()
                last_time=datetime.strptime(student_data['Last Attendance'],"%Y-%m-%d %H:%M:%S")

                add_text_to_frame(image, 'Attendance Marked', 'green', name=student_data['Name'])
                cv.waitKey(3)
                if (datetime.now() - last_time  ).total_seconds() > 60:
                    student_data['Attendance']+=1
                    cv.waitKey(3)
                    ref=db.reference(f'Student/{id_}')
                    ref.child('Attendance').set(student_data['Attendance'])
                    ref.child('Last Attendance').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    cv.waitKey(3)
                    print('ATTENDANCE MARKED')
                else:
                    print('ALREADY MARKED')
                    cv.waitKey(3)
                    add_text_to_frame(image, 'Already Marked for today', 'red',name=student_data['Name'])

        counter+=1
        if counter >= 15:
            counter=0
    cv.imshow('Awais',image)
    cv.waitKey(1)
