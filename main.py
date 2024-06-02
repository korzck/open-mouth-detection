import cv2 
import mediapipe as mp 

cam = cv2.VideoCapture(0)                     # start video capture object with camera

face_mesh_detector = mp.solutions.face_mesh   # to get face mesh result and landmarks
face_mesh = face_mesh_detector.FaceMesh(max_num_faces=1, 
										min_detection_confidence=0.5, 
										min_tracking_confidence=0.5)

# variables for lips
upper_lip = 12
lower_lip = 16

left_lip = 76
right_lip = 292

upper_loc = 0
lower_loc = 0

left_loc = 0
right_loc = 0

forhead_x = 0
forhead_y = 0

text = ''

count = 0

while True:
    count += 1
    ret, frame = cam.read()    # read from camera
    frame = cv2.flip(frame, 1) # mirror frame
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # change image color from BGR to RGB
    output = face_mesh.process(rgb_frame)               # output of detection
    landmark_points = output.multi_face_landmarks       # all landmark points

    if landmark_points:
        frame_height, frame_width, dimension = frame.shape  # get frame things, dimension is not needed in our application

        landmarks = landmark_points[0].landmark          # get all landmark points in values                                      # if landmarks are found
        for id, landmark in enumerate(landmarks):        # use enumerate to get index and values
            x, y = landmark.x, landmark.y                # ladnmark points
            x_on_frame = int(x*frame_width)              # relative to frame width
            y_on_frame = int(y*frame_height)             # relative to frame height

            # draw point(circle) on each landmark to show (Optional) 
            if id == upper_lip:
                upper_loc = y_on_frame
                cv2.circle(img=frame, center=(x_on_frame, y_on_frame), radius = 3, color=(0,255,0))

            elif id == lower_lip:
                lower_loc = y_on_frame
                cv2.circle(img=frame, center=(x_on_frame, y_on_frame), radius = 3, color=(0,255,0))

            elif id == left_lip:
                left_loc = x_on_frame
                cv2.circle(img=frame, center=(x_on_frame, y_on_frame), radius = 3, color=(0,255,0))

            elif id == right_lip:
                right_loc = x_on_frame
                cv2.circle(img=frame, center=(x_on_frame, y_on_frame), radius = 3, color=(0,255,0))

            elif id == 67:
                forhead_x = x_on_frame
                forhead_y = y_on_frame

            # else:
            #     # cv2.circle(img=frame, center=(x_on_frame, y_on_frame), radius = 3, color=(0,0,255))
            #     cv2.putText(img = frame, 
			# 		text = str(id), 
			# 		org = (x_on_frame, y_on_frame), 
			# 		fontFace = cv2.FONT_HERSHEY_DUPLEX, 
			# 		fontScale = 0.3, 
			# 		color = (125, 246, 55),
			# 		thickness = 1)

        y_diff = int(lower_loc - upper_loc)
        x_diff = int(right_loc - left_loc)
        print(y_diff/x_diff*100)

        #show diff/text
        if count % 10 == 0:
            if y_diff/x_diff*100 > 25 :
                text = 'Talking'
            else:
                text = 'Not talking'
        cv2.putText(img = frame, 
					text = text, 
					org = (forhead_x, forhead_y), 
					fontFace = cv2.FONT_HERSHEY_DUPLEX, 
					fontScale = 1, 
					color = (125, 246, 55),
					thickness = 2)
            
    
    cv2.imshow('img', frame)  # show image
    # wait a little also read input
    # if q pressed, break while loop and get out
    if cv2.waitKey(1) ==ord('q'):
        break

# after the job done
cam.release()             # release camera so that other apps can use it
cv2.destroyAllWindows()   # kill all windows created by opencv
