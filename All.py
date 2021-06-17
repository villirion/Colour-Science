import scipy.io
import glob ##Unix style pathname pattern expansion
import numpy as np
import matplotlib.pyplot as plt

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

    #v = np.diag(v)
    
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

def GetPatchRadiance(img,row,col,sampleSz):

    if(sampleSz%2):
        sampleSz+=1

    #save in row major order
    
    radiance = np.zeros(1,len(row)*len(col))

    for i in range (0,len(row)):
        for j in range(0,len(col)):
            pixels = img[row(i)-sampleSz/2:row(i)+sampleSz/2,col(j)-sampleSz/2:col(j)+sampleSz/2] #revoir plus tard
            radiance[(i-1)*len(col)+j] = numpy.mean(pixels)

    return radiance

def GetRGBdc(folder,bayerP):
    
    ##pas encore changer
    load([folder,'rawData.mat'])
    img = double(img)
    imgDark = imread([folder,'./canon60d_black.pgm'])


    img2 = img-double(imgDark)
    ##pas encore changer
    
    img2 = [0 if x<0 else x for x in img2]

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
   
    ## Pas encore changer
    
    xyCornerFile='xyCorner.mat'
    
    if not (dir([folder,xyCornerFile])):
        
        imagesc(imgG)
        grid on

        xyCorner=ginput(4)
        save ([folder,xyCornerFile], 'xyCorner')
    else:
        load([folder,xyCornerFile])


    xyCorner = round(xyCorner)
    xyCorner = np.flip(xyCorner,2)

    rowRange = min(xyCorner(1:2,1)):min(xyCorner(3:4,1))
    colRange = min(xyCorner([1,4],2)):max(xyCorner([2,3],2))
    
    ##pas encore changer

    imgR = imgR[rowRange,colRange]
    imgG = imgG[rowRange,colRange]
    imgB = imgB[rowRange,colRange]

    plt.plot(imgR)
    plt.show()

    nRow = 12
    nCol = 20

    patchSz = [imgR.shape[0]/nRow,imgR.shape[1]/nCol]

    col = [i for i in range(patchSz[1]/2,imgG.shape[1],patchSz[1])]
    row = [i for i in range(patchSz[0]/2,imgG.shape[0],patchSz[0])]

    col = round(col)
    row = round(row)

    plt.plot(col,np.tile(row,length(col),1),'ko')

    patchSamplingSz=4
    radiance = np.zeros(3,nRow*nCol)

    radiance[0,:] = GetPatchRadiance(imgR,row,col,patchSamplingSz)
    radiance[1,:] = GetPatchRadiance(imgG,row,col,patchSamplingSz)
    radiance[2,:] = GetPatchRadiance(imgB,row,col,patchSamplingSz)

    return radiance

def RecoverCMFev(ill,reflSet,w,XYZSet,e):

    numRefl = reflSet.shape[1]

    A = np.zeros(numRefl,e.shape[1])
    b = np.zeros(A.shape[0],1)

    deltaLambda = 10
    weight = 1 
    
    for i in range(0,numRefl):
        #weight=XYZSet(i)
        A[i,:] = reflSet[:,i].conj().transpose() @ np.diag(ill) @ e * deltaLambda * weight #maybe different operator
        b[i] = XYZSet[i]*weight #? if weight = 1 

    X = linalg.lstsq(A,b)
    #X = lsqnonneg(A,b);

    X = e*X


    return X,A,b

def RecoverCSS_singlePic():

    ##pas encore changer
    folder='./raw/'
    filename='img_0153'

    system(['./dcraw -4 -D -j -v -t 0 ', [folder,filename,'.CR2']])

    img = matplotlib.pyplot.imread([folder,filename,'.pgm'])
    save ([folder,'rawData.mat'], 'img')

    bayerP='RGGB'
    ##pas encore changer
   
    reflectance = scipy.io.loadmat('CCDC_meas.mat')

    glossyP = [79,99,119,139,159,179,199,219]
    darkP = [21,40,81,100,141,150,151,152,160,201,220]
    unwantedP = glossyP + darkP

    refl1 = reflectance['CCDC_meas']['spectra'][0][0][2:-1,:]
    
    wWanted = [i for i in range(400,730,10)]
    w = [i for i in range(400,730,10)]

    Range = [i for i in range(21,221)]

    refl2 = np.zeros(len(w),len(Range)-len(unwantedP))

    idx = 0
    for i in Range:
        if i not in unwantedP:
            refl2[:,idx] = refl1[:,i]
            idx += 1

    refl = refl2

    radiance1 = GetRGBdc(folder,bayerP)
    radiance1 = radiance1/(2**16)

    radiance2 = np.zeros(3,len(Range)-len(unwantedP))
    
    idx = 0
    for i in Range:
        if i not in unwantedP:
            radiance2[:,idx]=radiance1[:,i]
            idx += 1

    radiance = radiance2
    radiance = radiance.conj().transpose() #conj() probablement inutile
    
    ill = scipy.io.loadmat(folder + 'daylight.mat')['ill']
    w = [i for i in range(380,785,5)]
    
    ##pas encore changer
    ill_groundTruth = np.interp(w,ill,wWanted) 

    ill_groundTruth = ill_groundTruth * 100 / ill_groundTruth(find(wWanted==560)) #tester en matlab

    ##pas encore changer

    w = wWanted

    camName='Canon60D'

    rgbCMF, camNameAll = getCameraSpectralSensitivity()
    
    for i in range(0,len(camNameAll)):
        if camNameAll[i] == camName:
            cmf = [rgbCMF[0][:,i],rgbCMF[1][:,i],rgbCMF[2][:,i]]


    cmf = cmf/cmf.max()

    plt.plot(w, cmf[:,0], 'r', w, cmf[:,1], 'g', w,  cmf[:,2], 'b')
    plt.xlabel('Measured camera response function')
    plt.show()

    numEV=2
    eRed, eGreen, eBlue = PCACameraSensitivity(numEV)

    CCTrange = [i for i in range(4000,27100,100)]
           
    diff_b = np.zeros(1,len(CCTrange))
    
    for i in range(0,len(CCTrange)):
        ill = getDaylightScalars(CCTrange[i])
        deltaLamda=10
        
        cmfHat[:,0] = RecoverCMFev(ill,refl,w,radiance[:,0],eRed)
        cmfHat[:,1] = RecoverCMFev(ill,refl,w,radiance[:,1],eGreen)
        cmfHat[:,2] = RecoverCMFev(ill,refl,w,radiance[:,2],eBlue)

        I_hat=refl.conj().transpose() @ np.diag(ill) @ cmfHat @ deltaLamda  #conj() probablement inutile
        diff_b[i] = np.linalg.norm(radiance-I_hat)
    
    plt.plot(CCTrange, diff_b, '-o')
    plt.xlim(CCTrange[0],CCTrange[-1])
    plt.xlabel('CCT')
    plt.ylabel('norm of radiance difference')
    plt.show()
    
    minDiff = diff_b.min()
    minDiffIdx = diff_b[minDiff]
    ill = getDaylightScalars(CCTrange[minDiffIdx])

    ill = ill/ill(find(w==560)) #tester en matlab

    w = wWanted
    
    ill_groundTruth = ill_groundTruth / ill_groundTruth(find(w==560));  #tester en matlab
    
    plt.plot(w, ill_groundTrut, w, ill,'r-.')
    #legend('measured daylight',label='our result');
    plt.show()

    cmfHat[:,0] = RecoverCMFev(ill,refl,w,radiance[:,0],eRed)
    cmfHat[:,1] = RecoverCMFev(ill,refl,w,radiance[:,1],eGreen)
    cmfHat[:,2] = RecoverCMFev(ill,refl,w,radiance[:,2],eBlue)
     
    cmfHat = cmfHat/cmfHat.max()
    cmfHat = [0 if x<0 else x for x in cmfHat]

    w = [i for i in range(400,730,10)]
    
    plt.plot(w, cmf[:,0], 'r', w, cmf[:,1], 'g', w, cmf[:,2], 'b' )
    plt.plot(w, cmfHat[:,0], 'r-.', w, cmfHat[:,1], 'g-.', w, cmfHat[:,2], 'b-.')
    plt.show()
    #legend('r_m','g_m','b_m','r_e','g_e','b_e');
    #save (['cmf',camName,'.mat'], 'cmf', 'cmfHat');

    return cmfHat
