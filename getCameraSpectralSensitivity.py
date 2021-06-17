import scipy.io
import glob ##Unix style pathname pattern expansion
import numpy as np

def getCameraSpectralSensitivity():

    prefix = 'camSpecSensitivity/cmf_'
    suffix = '.mat'
    listFiles = prefix + '*' + suffix
    matdict = []
    camName = []
    
    for file in glob.glob(listFiles):
        mat = scipy.io.loadmat(file)
        matdict.append({k:v for k, v in mat.items() if k[0] != '_'})
        camName.append(file[len(prefix):-len(suffix)])
        
        
    return matdict, camName
