import scipy.io
import glob ##Unix style pathname pattern expansion
import numpy as np

def PCACameraSensitivity(numEV=1):
    
    matdict, camName = getCameraSpectralSensitivity()
    
    redCMF = np.array(matdict[0]['r'])
    greenCMF = np.array(matdict[0]['g'])
    blueCMF = np.array(matdict[0]['b'])

    for i in range(1,len(matdict)):
        if i != 16:
            redCMF = np.vstack((redCMF, matdict[i]['r']))
            greenCMF = np.vstack((greenCMF, matdict[i]['g']))
            blueCMF = np.vstack((blueCMF, matdict[i]['b']))
    
        
    # normalize to each curve
    
    for i in range(0,len(greenCMF)):
        redCMF[i] = redCMF[i]/redCMF[i].max()
        greenCMF[i] = greenCMF[i]/greenCMF[i].max()
        blueCMF[i] = blueCMF[i]/blueCMF[i].max()

    
    # do PCA on cmf

    
    eRed = GetEigenvector(redCMF,numEV);
    eGreen = GetEigenvector(greenCMF,numEV);
    eBlue = GetEigenvector(blueCMF,numEV);
    
    return eRed,eGreen,eBlue
