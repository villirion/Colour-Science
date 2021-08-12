import numpy as np

def Kim_Weyrich_Kautz_inverse(Xw,Yw,Zw, Q, M, h, La):
    
    Aj = 0.89 ; Bj = 0.24 ; Oj = 0.65 ; nj = 3.65
    Ak = 456.5 ; nk = 0.62 ; Am = 0.11 ; Bm = 0.61
    nc = 0.57; nq = 0.1308; pi = np.pi
    E = 1 #for test question how changing it
    
    MATRIX_XYZ_TO_LMS = np.array([
        [0.38971, 0.68898, -0.07868],
        [-0.22981, 1.18340, 0.04641],
        [0.00000, 0.00000, 1.00000],
    ])
    
    Lw,Mw,Sw = MATRIX_XYZ_TO_LMS @ np.array([[Xw],[Yw],[Zw]])
    
    Lwp = (Lw**nc)/(Lw**nc + La**nc)
    Mwp = (Mw**nc)/(Mw**nc + La**nc)
    Swp = (Sw**nc)/(Sw**nc + La**nc)
    
    Aw = (40*Lwp+20*Mwp+Swp)/61
    Aw = Aw.item(0)
    
    J = Q/(Lw)**nq

    Jp = (J/100 - 1)/(E + 1)
    Jp = Jp.item(0)
    
    A = Aw*((Aj * Jp**nj)/(Jp**nj + Aj**nj) + Bj)

    C = M/(Am*np.log(10)*Lw + Bm)
    
    a = np.cos(pi*h/180) * (C/Ak)**(1/nk)
    b = np.sin(pi*h/180) * (C/Ak)**(1/nk)
    
    Mt = np.array([
        [1.0000, 0.3215, 0.2053],
        [1.0000, -0.6351, -0.1860],
        [1.0000, -0.1568, -4.4904],
    ])

    Lp,Mp,Sp = Mt @ np.array([[A],a,b])
    
    L = ((-(La**nc)*Lp)/(Lp-1))**(1/nc)
    M = ((-(La**nc)*Mp)/(Mp-1))**(1/nc)
    S = ((-(La**nc)*Sp)/(Sp-1))**(1/nc)

    X,Y,Z = np.linalg.inv(MATRIX_XYZ_TO_LMS) @ np.array([L,M,S])
    
    return X,Y,Z

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
