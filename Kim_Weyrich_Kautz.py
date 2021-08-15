import numpy as np

def Kim_Weyrich_Kautz(X,Y,Z, Xw,Yw,Zw, La, E="LCD"):
    
    pi = np.pi
    
    MATRIX_XYZ_TO_LMS = np.array([
        [0.38971, 0.68898, -0.07868],
        [-0.22981, 1.18340, 0.04641],
        [0.00000, 0.00000, 1.00000],
    ])
    
    L,M,S = MATRIX_XYZ_TO_LMS @ np.array([[X],[Y],[Z]])
    Lw,Mw,Sw = MATRIX_XYZ_TO_LMS @ np.array([[Xw],[Yw],[Zw]])
    
    nc = 0.57

    # (2)
    Lp = (L**nc)/(L**nc + La**nc)
    Mp = (M**nc)/(M**nc + La**nc)
    Sp = (S**nc)/(S**nc + La**nc)
    
    #question does Aw is with Lwp or just Lw 
    Lwp = (Lw**nc)/(Lw**nc + La**nc)
    Mwp = (Mw**nc)/(Mw**nc + La**nc)
    Swp = (Sw**nc)/(Sw**nc + La**nc)
    
    # (3)
    A = (40*Lp+20*Mp+Sp)/61
    
    Aw = (40*Lwp+20*Mwp+Swp)/61

    # (4) & (5)
    Aj = 0.89 ; Bj = 0.24 ; Oj = 0.65 ; nj = 3.65
    Jp = ((-((A/Aw)-Bj)*Oj**nj)/((A/Aw)-Bj-Aj))**(1/nj)
    
    # (6)
    if E == "LCD":
        E = 1.0
    if E == "media":
        E = 1.2175
    if E == "CRT":
        E = 1.4572
    if E == "paper":
        E = 1.7526
        
    J = 100*(E*(Jp-1)+1)

    # (7)
    nq = 0.1308
    Q = J*(Lw)**nq

    # (8)
    a = (1/11)*(11*Lp-12*Mp+Sp)

    # (9)
    b = (1/9)*(Lp+Mp-2*Sp)
    
    # (10) & (11)
    Ak = 456.5 ; nk = 0.62 ; Am = 0.11 ; Bm = 0.61
    C = Ak*(np.sqrt(a**2+b**2)**nk)
    M = C*(Am*np.log10(Lw)+Bm) #verifier log 
    
    # (12)
    s = 100*np.sqrt(M/Q)

    # (13)
    h = (180/pi)*np.arctan(b/a)

    print("Lightness : ", J, "\nBrightness : ", Q, "\nChroma : ", C, 
          "\nColourfulness : ", M,"\nSaturation : ", S, "\nHue angle : ", h)

    return J,Q,C,M,S,h

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
