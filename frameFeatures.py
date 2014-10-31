# -*- coding: utf-8 -*-
#   Clustering of frames in a video.
#   Author - Janu Verma
#   jv367@cornell.edu


import numpy as np 
import cv2 
import sys
import math
#from frameExtraction import FrameExtraction


class FrameFeatures:
    """
    Computes the features of a frame in a video.

    Parameters
    ----------
    videoFrame : A frame represented by the RGB vectors which is a 
                numpy array of shape (xPixels, yPixels, 3). 
    """
    def __init__(self, videoFrame):
        self.frame = videoFrame


    def splittingFrame(self, frame, nComps=4):
        """
        Split the frame into 4 parts. 

        Parameters
        ----------
        frame : A numpy array of RGB vectors for the frame.
        nComps : Number of components the frame is to be splitted. 
                Default is 4. 

        Returns
        -------
        Coordinates of the sub-frames.      
        """
        newCoordinates = []
        xPixels = frame.shape[0]
        yPixels = frame.shape[1]

        splittedFrameLength = xPixels/4
        splittedFrameWidth = yPixels/4
        newCoordinates.append(splittedFrameLength)
        newCoordinates.append(splittedFrameWidth)
        return newCoordinates



    def frameFeatures(self):
        """
        Computes the feature vectors. 

        Returns
        -------
        A numpy array of shape (nFeatures,) where nFeatures is equal to nComps times 9.
        """
        frame = self.frame
        allFeatures = []
        splits = self.splittingFrame(frame)
        k = splits[0]
        l = splits[1]

        for i in range(4):
            subFrame = frame[i*k:(i+1)*k, i*l:(i+1)*l]
            subFrameFeatures = self.colorMoments(subFrame)
            allFeatures.extend(subFrameFeatures)

        return np.array(allFeatures)    



    def BGRValues(self, img):
        """
        Extracts the RGB vectors from the frame. 

        Parameters
        ----------
        img :  A frame expressed as RGB vectors. 

        Returns
        -------
        A dictionary with Red, Blue and Green as keys and the corresponding vectors containing
        color values for each pixel as value. 
        """ 
        xPixels = img.shape[0]
        yPixels = img.shape[1]
        nPixels = xPixels * yPixels

        blueValues = []
        greenValues = []
        redValues = []

        for i in range(xPixels):
            for j in range(yPixels):
                alpha = img[i][j]
                blueValues.append(alpha[2])
                greenValues.append(alpha[1])
                redValues.append(alpha[0])
        
        blueValues = np.array(blueValues)
        greenValues = np.array(greenValues)
        redValues = np.array(redValues)

        BGRdict = {'Red':redValues, 'Blue':blueValues, 'Green':greenValues}
        return BGRdict



    def colorMoments(self, frame):
        """
        Compute the color moments of a frame. 

        Parameters
        ----------
        frame 

        Returns
        -------
        A list containing first, second and third color moments of the frame.
        """
        momentsList = []

        BGRdict = self.BGRValues(frame)

        redValues = BGRdict['Red']
        blueValues = BGRdict['Blue']
        greenValues = BGRdict['Green']

        moments1 = self.firstMoments(redValues, blueValues, greenValues)
        red1 = moments1['Red']
        momentsList.append(red1)
        blue1 = moments1['Blue']
        momentsList.append(blue1)
        green1 = moments1['Green']
        momentsList.append(green1)

        nPixels = frame.shape[0] * frame.shape[1]
        blueMeanArray = np.ndarray(nPixels)
        blueMeanArray.fill(blue1)

        greenMeanArray = np.ndarray(nPixels)
        greenMeanArray.fill(green1)

        redMeanArray = np.ndarray(nPixels)
        redMeanArray.fill(red1)

        moments2 = self.secondMoments(redValues, blueValues, greenValues, blueMeanArray, greenMeanArray, redMeanArray)
        red2 = moments2['Red']
        momentsList.append(red2)
        blue2 = moments2['Blue']
        momentsList.append(blue2)
        green2 = moments2['Green']
        momentsList.append(green2)

       # moments3 = self.thirdMoments(redValues, blueValues, greenValues, blueMeanArray, greenMeanArray, redMeanArray)
       # red3 = moments3['Red']
       # momentsList.append(red3)
       # blue3 = moments3['Blue']
       # momentsList.append(blue3)
       # green3 = moments3['Green']
       # momentsList.append(green3)

        return momentsList



    def firstMoments(self, redValues, blueValues, greenValues):
        """
        Computes first color moments. 

        Parameters
        ----------
        redValues : A list of Red values for every pixel. 
        blueValues : A list of Blue values for every pixel.
        greenValues : A list of Green values for every pixel.

        Returns
        -------
        A dictionary containing first moments of each color. 
        """
        blueMean = np.mean(blueValues)
        greenMean = np.mean(greenValues)
        redMean = np.mean(redValues)

        firstMomentsDict = {'Red':redMean, 'Blue':blueMean, 'Green':greenMean}
        return firstMomentsDict



    def secondMoments(self, redValues, blueValues, greenValues, blueMeanArray, greenMeanArray, redMeanArray):
        """
        Computes second color moments. 

        Parameters
        ----------
        redValues : A list of Red values for every pixel. 
        blueValues : A list of Blue values for every pixel.
        greenValues : A list of Green values for every pixel.
        redMeanArray: A list of length same as redValues where every element is the mean of red values. 
        blueMeanArray: A list of length same as blueValues where every element is the mean of blue values.
        greenMeanArray: A list of length same as greenValues where every element is the mean of green values.

        Returns
        -------
        A dictionary containing second moments of each color.
        """
        secondMomentBlue = math.sqrt(np.mean((blueValues - blueMeanArray)**2))
        secondMomentGreen = math.sqrt(np.mean((greenValues - greenMeanArray)**2))
        secondMomentRed = math.sqrt(np.mean((redValues - redMeanArray)**2))

        secondMomentsDict = {'Red':secondMomentRed, 'Blue':secondMomentBlue, 'Green':secondMomentGreen}
        return secondMomentsDict    



    def thirdMoments(self, redValues, blueValues, greenValues, blueMeanArray, greenMeanArray, redMeanArray):
        """
        Computes third color moments. 

        Parameters
        ----------
        redValues : A list of Red values for every pixel. 
        blueValues : A list of Blue values for every pixel.
        greenValues : A list of Green values for every pixel.
        redMeanArray: A list of length same as redValues where every element is the mean of red values. 
        blueMeanArray: A list of length same as blueValues where every element is the mean of blue values.
        greenMeanArray: A list of length same as greenValues where every element is the mean of green values.

        Returns
        -------
        A dictionary containing third moments of each color.
        """
        thirdMomentBlue = (np.mean((blueValues - blueMeanArray)**3))**(1/3.0)
        thirdMomentGreen = (np.mean((greenValues - greenMeanArray)**3))**(1/3.0)
        thirdMomentRed = (np.mean((redValues - redMeanArray)**3))**(1/3.0)

        thirdMomentsDict = {'Red':thirdMomentRed, 'Blue':thirdMomentBlue, 'Green':thirdMomentGreen}
        return thirdMomentsDict 
