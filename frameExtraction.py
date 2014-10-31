import numpy as np
import cv2

import frameFeatures
import frameClusters

frameData = []

def readFrames(filename, max):
    print "Beginning to load file"
    cap = cv2.VideoCapture(filename)
    print "Attempted to load file"
    if not cap.isOpened():
        print "Could not open reference " + filename
        return
    frames = 0
    count = 0
    fps = cap.get(5)
    max = cap.get(7)/fps
    while(cap.isOpened()):
        #print count
        count += 1 
        ret, frame = cap.read()
        if ret and count/fps == 1:
       # if ret:
            frames += 1
            count = 0
            timestamp = cap.get(0)/1000
            #print str(timestamp)
            frameData.append((frame, timestamp))
           # cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        elif not ret:
            break
        elif frames > max:
            break
        #else:
           # break

    cap.release()
    cv2.destroyAllWindows()
    
    
def filterFrames(keyFrames, max, numClusters):
    currentFrame = -1
    frontier = []
    print "Max is " + str(max)
    currentFrame += 1
    while True:
        print str(currentFrame)
        for i in enumerate(keyFrames):
            if currentFrame in i[1]:
                #print "Found " + str(currentFrame)
                end = loopConsecutive(i[1], currentFrame)
                frontier.append((currentFrame, end-1))
               # frontier.append((currentFrame, end-1, i[0]))
                currentFrame = end
                #print currentFrame
        if currentFrame == max:
            return frontier;
                
    
def loopConsecutive(list, begin):
    target = begin
    while target in list:
        target += 1
    return target
    
numClusters = 8  
#max = 79
readFrames("UX1.mp4", max)
print "Read frames"
max = len(frameData)
print str(len(frameData))

frameClusters = frameClusters.FrameClustering(frameData, numClusters)

keyFrames = frameClusters.frameClusters()

#keyFrames = [[27, 66, 69, 70, 71, 72, 73, 74, 76], [4, 16, 17, 21, 35, 46, 47, 49, 62, 63],
#[22, 23, 25, 26, 36, 37, 48, 67], [28, 29, 30, 31, 32, 33, 75, 77, 78], [59, 60]
#, [2, 3, 5, 10, 11, 12, 13, 14, 15, 20, 53, 54, 55, 58, 61], [50], [0, 1, 6, 7,
#8, 9, 18, 19, 24, 34, 38, 39, 40, 41, 42, 43, 44, 45, 51, 52, 56, 57, 64, 65, 68
#]]
print keyFrames

frontier = filterFrames(keyFrames, max, numClusters)

#frontier = [(0, 1), (2, 4), (6, 16), (18, 26), (28, 29), (30, 30), (31, 31), (33, 34), (35,41), (43, 48), (49, 62), (64, 69), (70, 84), (85, 85), (87, 89), (90, 140), (142, 143), (145, 155), (156, 162), (164, 168), (169, 171), (172, 207), (209, 235), (237, 246), (247, 253), (255, 255), (257, 261), (262, 262), (264, 315), (316, 316), (318, 338), (339, 339), (341, 341), (343, 343), (344, 344), (346, 358), (360, 380), (381, 382), (384, 398), (399, 403), (405, 415), (416, 418), (419, 420), (422, 422), (424, 454), (455, 455), (457, 481), (482, 483), (484, 485), (487, 488), (490, 494), (495, 495), (497, 498), (499, 499), (501, 515)]

print frontier

np.savetxt("segments.txt", frontier)
string = ""
for i, data in enumerate(frontier):
	string += str(data[0]) + ", " + str(data[1]) + ", "
print string
