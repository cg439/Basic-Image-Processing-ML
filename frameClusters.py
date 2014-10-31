# -*- coding: utf-8 -*-
#   Clustering of frames in a video.
#   Author - Janu Verma
#   jv367@cornell.edu


import numpy as np 
from sklearn.cluster import KMeans
import frameFeatures
import cv2 



class FrameClustering:
    """
    Clusters the frames in a video.

    Parameters
    ----------
    videoFrames : Frames of the video expresses as a list of RGB arrays for each frame. 
                Length of the videoFrames is equal to the total number of frames in the video.

    numberOfClusters : Number of clusters to be created.             
    """

    def __init__(self, videoFrames, numberOfClusters):
        self.frames = {}
        for i,x in enumerate(videoFrames):
            self.frames[i] = x[0]

        self.k = numberOfClusters


    def featureVectors(self):
        """
        Extract the feature vectors of the frames.

        Returns
        -------
        An (numpy) array of feature vectors for all the frames.  
        """
        frameData = self.frames
        featuresData = []
        print "Calculating feature vectors for all frames"
        for indX in frameData.keys():
            img = frameData[indX]
            featVect = frameFeatures.FrameFeatures(img)
            featVect = featVect.frameFeatures()
            featuresData.append(featVect)
            print featVect
            print "Currently processing frame: " + str(indX)
        print "Extracted feature vectors on all frames"
        return np.array(featuresData)   



    def frameClusters(self):
        """
        Clusters the frames in the video.

        Returns
        -------
        A list of clusters. 
        """
        clusterDict = {}
        kmeans = KMeans(n_clusters=self.k)
        X = self.featureVectors()
        #print X
        clusters = kmeans.fit_predict(X)
        #print clusters
        for i,x in enumerate(clusters):
            clusterDict[i] = x
        print "Enumerated potential cluster targets"
        #print clusterDict
        allClusters = []
        for j in range(self.k):
            alpha = []
            allClusters.append(alpha)

        for i in clusterDict.keys():
            j = clusterDict[i]
            allClusters[j].append(i)

        return allClusters




        
