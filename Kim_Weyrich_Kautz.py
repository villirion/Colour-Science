import numpy as np

def Kim_Weyrich_Kautz(XYZ, XYZw, La, E="LCD"):
    
    Aj = 0.89 ; Bj = 0.24 ; Oj = 0.65 ; nj = 3.65
    Ak = 456.5 ; nk = 0.62 ; Am = 0.11 ; Bm = 0.61
    nc = 0.57 ; nq = 0.1308
    pi = np.pi
    
    if E == "LCD":
        E = 1.0
    if E == "media":
        E = 1.2175
    if E == "CRT":
        E = 1.4572
    if E == "paper":
        E = 1.7526
    
    MATRIX_XYZ_TO_LMS = np.array([
        [0.38971, 0.68898, -0.07868],
        [-0.22981, 1.18340, 0.04641],
        [0.00000, 0.00000, 1.00000],
    ])
    
    LMS = MATRIX_XYZ_TO_LMS @ XYZ
    LMSw = MATRIX_XYZ_TO_LMS @ XYZw
    
    LMSp = (LMS**nc)/(LMS**nc + La**nc)
    LMSwp = (LMSw**nc)/(LMSw**nc + La**nc)

    A = (40*LMSp[0]+20*LMSp[1]+LMSp[2])/61
    Aw = (40*LMSwp[0]+20*LMSwp[1]+LMSwp[2])/61

    Jp = ((-((A/Aw)-Bj)*Oj**nj)/((A/Aw)-Bj-Aj))**(1/nj)
 
    J = 100*(E*(Jp-1)+1)

    Q = J*(LMSw[0])**nq

    a = (1/11)*(11*LMSp[0]-12*LMSp[1]+LMSp[2])
    b = (1/9)*(LMSp[0]+LMSp[1]-2*LMSp[2])

    C = Ak*(np.sqrt(a**2+b**2)**nk)
    M = C*(Am*np.log10(LMSw[0])+Bm)
    s = 100*np.sqrt(M/Q)
    h = (180/pi)*np.arctan(b/a)

    # print("Lightness : ", J, "\nBrightness : ", Q, "\nChroma : ", C, 
    #       "\nColourfulness : ", M,"\nSaturation : ", s, "\nHue angle : ", h)

    return J,Q,C,M,s,h

"""
#input : 

XYZ = np.array([19.01, 20.00, 21.78])
X = XYZ[0]
Y = XYZ[1]
Z = XYZ[2]
XYZ_w = np.array([95.05, 100.00, 108.88])
Xw = XYZ_w[0]
Yw = XYZ_w[1]
Zw = XYZ_w[2]
L_A = 318.31

Kim_Weyrich_Kautz(X,Y,Z, Xw,Yw,Zw, L_A)
"""
