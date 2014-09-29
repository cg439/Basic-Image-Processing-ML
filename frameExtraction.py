import numpy as np
import cv2

frameData = []

def readFrames(filename):
    print "Beginning to load file"
    cap = cv2.VideoCapture(filename)
    print "Attempted to load file"
    if not cap.isOpened():
        print "Could not open reference " + filename
        return
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            frameData.append(frame)
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()
    
    
readFrames("sample.avi")

print str(len(frameData))
