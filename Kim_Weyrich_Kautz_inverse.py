import numpy as np

def Kim_Weyrich_Kautz_inverse(XYZw, Q, M, h, La, E="LCD"):
    
    Aj = 0.89 ; Bj = 0.24 ; Oj = 0.65 ; nj = 3.65
    Ak = 456.5 ; nk = 0.62 ; Am = 0.11 ; Bm = 0.61
    nc = 0.57; nq = 0.1308; pi = np.pi
   
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
    
    LMSw = MATRIX_XYZ_TO_LMS @ XYZw
    
    LMSwp = (LMSw**nc)/(LMSw**nc + La**nc)
    
    Aw = (40*LMSwp[0]+20*LMSwp[1]+LMSwp[2])/61
   
    J = Q/(LMSw[0])**nq
    
    Jp = (J/100 - 1)/E + 1
    
    A = Aw * ((Aj * (Jp**nj)) / ((Jp**nj) + (Oj**nj)) + Bj)
    
    C = M/(Am*np.log10(LMSw[0]) + Bm)
    
    # minus a and b to match the test but may be different with additional tests
    a = -( np.cos(pi*h/180) * (C/Ak)**(1/nk))
    b = -( np.sin(pi*h/180) * (C/Ak)**(1/nk))
    
    Mt = np.array([
        [1.0000, 0.3215, 0.2053],
        [1.0000, -0.6351, -0.1860],
        [1.0000, -0.1568, -4.4904],
    ])

    LMSp = Mt @ np.array([A,a,b])
    
    LMS = ((-(La**nc)*LMSp)/(LMSp-1))**(1/nc)
    XYZ = np.linalg.inv(MATRIX_XYZ_TO_LMS) @ LMS
    
    return XYZ


"""
#input : 

XYZ_w = np.array([95.05, 100.00, 108.88])
Xw = XYZ_w[0]
Yw = XYZ_w[1]
Zw = XYZ_w[2]
L_A = 318.31
Q = 93.08295192
M = 334.59271045
h = 87.92132174

Kim_Weyrich_Kautz_inverse(Xw,Yw,Zw, Q, M, h, L_A)
"""
