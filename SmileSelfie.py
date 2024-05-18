

#this will take a picture of you everytime you smile

#first import cv2 and mediapipe pyatuogui and playsound

import cv2
import mediapipe as mp
import pyautogui
from playsound import playsound


x1 = 0
y1 = 0
x2 = 0
y2 = 0

#here we will identify if we are smiling or not so we have to use the smile detection module
#we have to get the face landmarks so we will use the face mesh module
#the ending will get the all the face landmarks and store it into facemesh
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)

#initialize the webcam
#this is how we use the camera the 0 means the first camera we use 0 because we only have 1 camera it uses index values
camera = cv2.VideoCapture(0)

# Get the frame width and height
fw = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
fh = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

#this is how we show the captured face in the camera
while True: #we are going to read the camera content
    #what this does is it reads the camera content and stores it in the variable camera
    _,image = camera.read() # this will need to variables but we are only using the image one so we use a dash 

    #here we are going to flip the image because our camera is inverted
    #we use 1 because this is how we flip the image horizontally
    # if we use 0 that does not flip the image and goes x axis
    image = cv2.flip(image,1) #this will flip the image horizontally

    #from facemesh we have to get he landmarks and we need to convert it to an rgb image 
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    #this will process the rgb image and store it in output
    output = face_mesh.process(rgb_image) 

    #here how you get all the landmark points
    landmark_points = output.multi_face_landmarks

    #we will only be capturing one landmark
    if landmark_points:
        #here we are capturing the first landmark point
        landmarks = landmark_points[0].landmark
        #now from the landmarks we want to capture the smile points
        # Iterate through each landmark point in the list of landmarks
        for id, landmark in enumerate(landmarks):
            # Convert the normalized landmark coordinates to pixel coordinates
            x = int(landmark.x * fw)
            y = int(landmark.y * fh)

            # Check if the current landmark is the one with ID 43 (left corner of the mouth)
            if id == 43:
                 # Store the x and y coordinates of the left corner of the mouth
                x1 = x
                y1 = y

            # Check if the current landmark is the one with ID 287 (right corner of the mouth)
            if id == 287:
                # Store the x and y coordinates of the right corner of the mouth
                x2 = x
                y2 = y

        # Calculate the Euclidean distance between the two landmark points (corners of the mouth)
        dist = int(((x2-x1)**2 + (y2-y1)**2)**(0.5))

        # Print the calculated distance to the console
        print(dist)
        # Check if the distance exceeds the threshold value of 99 (indicating a smile)
        if dist > 99:
            # Save the current frame as an image file named "selfie.jpg"
            cv2.imwrite("selfie.jpg", image)
    
            # Play a beep sound to indicate that a picture has been taken
            playsound("/Users/ameshajid/Documents/VisualStudioCode/SmileSelfie/beep-01a.mp3")
    
            # Wait for 100 milliseconds to avoid rapid consecutive captures
            cv2.waitKey(100)
    cv2.imshow("Auto Selfie",image) #this will show the camera content in a window called camera
    key = cv2.waitKey(100) #this will wait for a key to be pressed
    #now we will check if they clicked the escape key
    #27 is the ascii value for the escape key
    if key == 27:
        break #this will break the loop and close the camera window if they press escape
camera.release() #this will release the camera
cv2.destroyAllWindows() #this will close the camera window








