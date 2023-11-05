import cv2 as cv
import pickle
import face_recognition
import os
student_images=list()
student_ids=list()
folder_path='Images/'
for image in os.listdir(folder_path):
    student_images.append(cv.imread(folder_path+image))
    student_ids.append(os.path.splitext(image)[0])
# for ids in student_ids:
#     print(ids)
def encode_image(image_list):
    encoded_images=list()
    for img in image_list:
        img=cv.cvtColor(img,cv.COLOR_BGR2RGB)
        encod_image=face_recognition.face_encodings(img)[0]
        encoded_images.append(encod_image)
    return encoded_images

# Lets test the encoding function

encodings = encode_image(student_images)
# print(encodings)
encoding_with_ids=[
    encodings,
    student_ids
]
pickle.dump(encoding_with_ids,open('encoding_with_ids.pkl','wb'))

