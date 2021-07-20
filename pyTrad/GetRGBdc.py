import numpy as np
import matplotlib.pyplot as plt
import scipy.io
from PIL import Image

def GetRGBdc(folder,bayerP):
    
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
