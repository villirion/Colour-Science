import scipy.io
import glob ##Unix style pathname pattern expansion
import numpy as np

def getCameraSpectralSensitivity():

    prefix = 'camSpecSensitivity/cmf_'
    suffix = '.mat'
    listFiles = prefix + '*' + suffix
    matdict = []
    camName = []
    
    for file in sorted(glob.glob(listFiles)):
        mat = scipy.io.loadmat(file)
        matdict.append({k:v for k, v in mat.items() if k[0] != '_'})
        camName.append(file[len(prefix):-len(suffix)])
        
    return matdict, camName

def GetEigenvector(refl,retainE=6):
    
    A= refl.transpose() @ refl
    
    v, e = np.linalg.eigh(A)

    v = np.diag(v)
    
    #v = v[len(v)-(retainE+1):len(v)]
    #e = e[:,len(e)-(retainE+1):len(e)]
    
    v = v[-(retainE):]
    e = e[:,-(retainE):]

    v = np.flipud(v)
    e = np.fliplr(e)
    
    return (e,v)

def PCACameraSensitivity(numEV=1):
    
    matdict, camName = getCameraSpectralSensitivity()
    
    redCMF = np.array(matdict[0]['r'])
    greenCMF = np.array(matdict[0]['g'])
    blueCMF = np.array(matdict[0]['b'])

    for i in range(1,len(matdict)):
        #there is a problem with the format of the 16th camera (cmf_Canon5D Mark II.mat I think)
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
    # do PCA on cmf

    
    eRed = GetEigenvector(redCMF,numEV);
    eGreen = GetEigenvector(greenCMF,numEV);
    eBlue = GetEigenvector(blueCMF,numEV);
    
    return eRed,eGreen,eBlue
