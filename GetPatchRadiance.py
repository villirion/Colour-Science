import numpy as np

def GetPatchRadiance(img,row,col,sampleSz):

    if(sampleSz%2):
        sampleSz+=1

    #save in row major order
    
    radiance = np.zeros((1,len(row)*len(col)))

    for i in range (0,len(row)):
        for j in range(0,len(col)):
            pixels = img[row[i]-sampleSz//2:row[i]+sampleSz//2 , col[j]-sampleSz//2:col[j]+sampleSz//2]
            radiance[0][i*len(col)+j] = np.mean(pixels)

    return radiance
