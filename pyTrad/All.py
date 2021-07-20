import numpy as np
import matplotlib.pyplot as plt
import scipy.io
from PIL import Image
import os
import glob 
from scipy.interpolate import interp1d

def getCameraSpectralSensitivity():

    prefix = 'camSpecSensitivity/cmf_'
    suffix = '.mat'
    listFiles = prefix + '*' + suffix
    matdict = []
    camName = []
    
    for file in sorted(glob.glob(listFiles)):
        mat = scipy.io.loadmat(file)
        if len(mat['r'])==1:
            matdict.append({k:v[0] for k, v in mat.items() if k[0] != '_'})
        else:
            matdict.append({k:v.reshape(len(v)) for k, v in mat.items() if k[0] != '_'})
        camName.append(file[len(prefix):-len(suffix)])
        
    return matdict, camName

def GetEigenvector(refl,retainE=6):
    
    #A=refl @refl.conj().transpose() 
    A=refl.transpose()@refl
    v, e = np.linalg.eigh(A)

    ##v = np.diag(v)
    
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
##    redCMF = np.array([matdict[i]['r'].tolist() for i in range(0,len(matdict))])
    greenCMF = np.array(matdict[0]['g'])
##    greenCMF = np.array([matdict[i]['g'].tolist() for i in range(0,len(matdict))])
    blueCMF = np.array(matdict[0]['b'])
##    blueCMF = np.array([matdict[i]['b'].tolist() for i in range(0,len(matdict))])
    for i in range(1,len(matdict)):
##        if i != 16:
        redCMF = np.vstack((redCMF, matdict[i]['r']))
        greenCMF = np.vstack((greenCMF, matdict[i]['g']))
        blueCMF = np.vstack((blueCMF, matdict[i]['b']))

        
    # normalize to each curve
    
    for i in range(0,len(greenCMF)):
        redCMF[i]   = redCMF[i]/redCMF[i].max()
        greenCMF[i] = greenCMF[i]/greenCMF[i].max()
        blueCMF[i]  = blueCMF[i]/blueCMF[i].max()

    
    # do PCA on cmf

    
    eRed = GetEigenvector(redCMF,numEV);
    eGreen = GetEigenvector(greenCMF,numEV);
    eBlue = GetEigenvector(blueCMF,numEV);
    
    return eRed,eGreen,eBlue

def getDaylightScalars(CCT):

    if(CCT>=4000 and CCT<=7000):
        xD = -4.607*10**9/(CCT**3) + 2.9678*10**6/(CCT**2) + 0.09911*10**3/CCT + 0.244063
    else:
        xD = -2.0064*10**9/(CCT**3) + 1.9018*10**6/(CCT**2) + 0.24748*10**3/CCT + 0.23704

    yD = -3*xD**2 + 2.87*xD - 0.275

    M1 = (-1.3515-1.7703*xD+5.9114*yD)/(0.0241+0.2562*xD -.7341*yD)

    M2 = (0.03-31.4424*xD+30.0717*yD)/(0.0241+0.2562*xD -.7341*yD)

    daylightScalars  = np.loadtxt('daylightScalars.txt')

    S0 = daylightScalars[:,1]
    S1 = daylightScalars[:,2]
    S2 = daylightScalars[:,3]

    SD=S0+M1*S1+M2*S2

    return SD

def GetRGBdc(folder,bayerP,filename):
    
    ImgRaw = Image.open(folder+filename+'.pgm')
    img = np.asarray(ImgRaw)
    #img = double(img)
    ImgRaw2 = Image.open(folder+'./canon60d_black.pgm')
    imgDark = np.asarray(ImgRaw2)
    img2 = img-imgDark # original doucle(imgDark)
    img2[img2 < 0] = 0

    if bayerP == 'RGGB':
        imgR = img2[::2, ::2]
        imgG = img2[::2, 2::2]
        imgB = img2[2::2, 2::2]
    elif bayerP == 'GBRG':
        imgR = img2[2::2, ::2]
        imgG = img2[::2, ::2]
        imgB = img2[::2, 2::2]
    elif bayerP == 'BGGR':
        imgR = img2[2::2, 2::2]
        imgG = img2[::2, 2::2]
        imgB = img2[::2, ::2]
    elif bayerP == 'GRBG':
        imgR = img2[::2, 2::2]
        imgG = img2[::2, ::2]
        imgB = img2[2::2, ::2]
    
    
    """
    if not os.path.exists(folder+xyCornerFile):   
        plt.plot(imgG) # peut etre?
        xyCorner = plt.ginput(4)
        print(xyCorner)
        plt.savefig(folder+xyCornerFile+'/xyCorner.mat')
    else:
        scipy.io.loadmat(folder+xyCornerFile)
        
    xyCorner = round(xyCorner)    
    xyCorner = np.flip(xyCorner,2)
    """
    #xyCorner is always the same values so for now i take directly the values in order 
    #to test the other function who are related to this one
    
    xyCorner =  [[486 , 722],
                 [483 , 1433],
                 [915 , 1430],
                 [915 , 725]]

    rowRange = [i for i in range(min(xyCorner[0][0],xyCorner[1][0]),max(xyCorner[2][0],xyCorner[3][0])+1)]
    colRange = [i for i in range(min(xyCorner[0][1],xyCorner[3][1]),max(xyCorner[1][1],xyCorner[2][1])+1)]
    
    
    imgR = imgR[np.ix_(rowRange,colRange)]
    imgG = imgG[np.ix_(rowRange,colRange)]
    imgB = imgB[np.ix_(rowRange,colRange)]

    ##plt.plot(imgR)
    ##plt.show()
    ##mettre la grille
    
    nRow = 12
    nCol = 20

    patchSz = [imgR.shape[0]//nRow,imgR.shape[1]//nCol]

    col = [i for i in range(patchSz[1]//2,int(imgG.shape[1]),patchSz[1])]
    row = [i for i in range(patchSz[0]//2,int(imgG.shape[0]),patchSz[0])]

    #col = round(col)
    #row = round(row)

    ##plt.plot(col,np.tile(row,length(col),1),'ko')

    patchSamplingSz = 4
    radiance = np.zeros((3,nRow*nCol))

    radiance[0,:] = GetPatchRadiance(imgR,row,col,patchSamplingSz)
    radiance[1,:] = GetPatchRadiance(imgG,row,col,patchSamplingSz)
    radiance[2,:] = GetPatchRadiance(imgB,row,col,patchSamplingSz)

    return radiance

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

def RecoverCSS_singlePic():
    
    folder = './raw/'
    filename = 'img_0153'
    os.system('dcraw -4 -D -j -v -t 0' + folder + filename + '.cr2') 

    #img = plt.imread(folder+filename+'.pgm')
    #plt.savefig(folder+'rawData.mat')

    bayerP = 'RGGB'
   
   
    reflectance = scipy.io.loadmat('CCDC_meas.mat')

    glossyP = [79,99,119,139,159,179,199,219]
    darkP = [21,40,81,100,141,150,151,152,160,201,220]
    unwantedP = glossyP + darkP

    refl1 = reflectance['CCDC_meas']['spectra'][0][0][2:-1,:]
    
    wWanted = [i for i in range(400,730,10)]
    w = [i for i in range(400,730,10)]

    Range = [i for i in range(21,221)]

    refl2 = np.zeros((len(w),len(Range)-len(unwantedP)))

    idx = 0
    for i in Range:
        if i not in unwantedP:
            refl2[:,idx] = refl1[:,i]
            idx += 1

    refl = refl2

    radiance1 = GetRGBdc(folder,bayerP,filename)
    radiance1 = radiance1/(2**16)

    radiance2 = np.zeros((3,len(Range)-len(unwantedP)))
    
    idx = 0
    for i in Range:
        if i not in unwantedP:
            radiance2[:,idx]=radiance1[:,i]
            idx += 1

    radiance = radiance2
    radiance = radiance.conj().transpose() #conj() probablement inutile
    
    ill = scipy.io.loadmat(folder + 'daylight.mat')['ill']
    ill = ill.reshape(len(ill))
    w = [i for i in range(380,785,5)]
    
    ill_groundTruth = interp1d(w,ill)(wWanted)

    ill_groundTruth = ill_groundTruth * 100 / ill_groundTruth[wWanted.index(560)]

    w = wWanted

    camName='Canon60D'

    rgbCMF, camNameAll = getCameraSpectralSensitivity()
    
    for i in range(0,len(camNameAll)):
        if camNameAll[i] == camName:
            cmf = [rgbCMF[i]['r'] + rgbCMF[i]['g'] + rgbCMF[i]['b']]

    cmf = cmf/max(cmf)

    #plt.plot(w, cmf[:,0], 'r', w, cmf[:,1], 'g', w,  cmf[:,2], 'b')
    #plt.xlabel('Measured camera response function')
    #plt.show()

    numEV=2
    eRed, eGreen, eBlue = PCACameraSensitivity(numEV)

    CCTrange = [i for i in range(4000,27100,100)]
           
    #diff_b = np.zeros((1,len(CCTrange)))
    diff_b = []
    
    cmfHat1 = []
    
    for i in range(0,len(CCTrange)):
        ill = getDaylightScalars(CCTrange[i])
        deltaLamda=10
        
        cmfHat1.append(RecoverCMFev(ill,refl,w,radiance[:,0],eRed))         
        cmfHat1.append(RecoverCMFev(ill,refl,w,radiance[:,1],eGreen))        
        cmfHat1.append(RecoverCMFev(ill,refl,w,radiance[:,2],eBlue))    
        
        cmfHat = np.array((cmfHat1[0][0] , cmfHat1[1][0] , cmfHat1[2][0]))
        cmfHat = cmfHat.transpose()
        
        I_hat = refl.conj().transpose() @ np.diag(ill) @ cmfHat * deltaLamda  #conj() probablement inutile
        #diff_b[i] = np.linalg.norm(radiance-I_hat)
        diff_b.append(np.linalg.norm(radiance-I_hat))
        
    #plt.plot(CCTrange, diff_b, '-o')
    #plt.xlim(CCTrange[0],CCTrange[-1])
    #plt.xlabel('CCT')
    #plt.ylabel('norm of radiance difference')
    #plt.show()
    
    minDiff = min(diff_b)
    minDiffIdx = diff_b.index(minDiff)
    ill = getDaylightScalars(CCTrange[minDiffIdx])

    ill = ill/ill[w.index(560)] 

    w = wWanted
    
    ill_groundTruth = ill_groundTruth / ill_groundTruth[w.index(560)]  
    
    #plt.plot(w, ill_groundTrut, w, ill,'r-.')
    ##legend('measured daylight',label='our result');
    #plt.show()

    cmfHat1 = []
    
    cmfHat1.append(RecoverCMFev(ill,refl,w,radiance[:,0],eRed))         
    cmfHat1.append(RecoverCMFev(ill,refl,w,radiance[:,1],eGreen))        
    cmfHat1.append(RecoverCMFev(ill,refl,w,radiance[:,2],eBlue)) 
     
    cmfHat = np.array((cmfHat1[0][0] , cmfHat1[1][0] , cmfHat1[2][0]))
    cmfHat = cmfHat.transpose()
    
    cmfHat = cmfHat/cmfHat.max()
    #cmfHat = [0 if x<0 else x for x in cmfHat]
    cmfHat[cmfHat < 0] = 0
    
    w = [i for i in range(400,730,10)]
    
    #plt.plot(w, cmf[:,0], 'r', w, cmf[:,1], 'g', w, cmf[:,2], 'b' )
    #plt.plot(w, cmfHat[:,0], 'r-.', w, cmfHat[:,1], 'g-.', w, cmfHat[:,2], 'b-.')
    #plt.show()
    ##legend('r_m','g_m','b_m','r_e','g_e','b_e');
    #save (['cmf',camName,'.mat'], 'cmf', 'cmfHat');

    return cmfHat

def RecoverCMFev(ill,reflSet,w,XYZSet,e):

    numRefl = reflSet.shape[1]

    #A = np.zeros((numRefl,1)) # A = np.zeros((numRefl,e.shape[1]))
    #b = np.zeros((A.shape[0],1))
    
    A = []
    b = []
    
    deltaLambda = 10
    weight = 1 

    for i in range(0,numRefl):
        #weight=XYZSet(i)
        A.append(reflSet[:,i].transpose() @ np.diag(ill) @ e[0] * deltaLambda * weight) #test inversé les matrice
        b.append(XYZSet[i]*weight) #? if weight = 1 
    
    A = np.array(A)
    A.reshape(len(A),2)

    X = np.linalg.lstsq(A,b)[0]
    #X = lsqnonneg(A,b)[0]
    
    print(X)
    
    X = e[0] @ X
    
    return X,A,b
