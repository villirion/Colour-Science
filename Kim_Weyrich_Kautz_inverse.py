import numpy as np

def Kim_Weyrich_Kautz_inverse(Lw,Mw,Sw, Q, M, h, La):
    
    
    Aj = 0.89 ; Bj = 0.24 ; Oj = 0.65 ; nj = 3.65
    Ak = 456.5 ; nk = 0.62 ; Am = 0.11 ; Bm = 0.61
    nc = 0.57; nq = 0.1308; pi = np.pi
    E = 1 #for test question how changing it
    
    Lwp = (Lw**nc)/(Lw**nc + La**nc)
    Mwp = (Mw**nc)/(Mw**nc + La**nc)
    Swp = (Sw**nc)/(Sw**nc + La**nc)
    
    Aw = (40*Lwp+20*Mwp+Swp)/61
    
    J = Q/(Lw)**nq

    Jp = (J/100 - 1)/(E + 1)
    
    A = Aw*((Aj * jp**nj)/(jp**nj + Aj**nj) + Bj)

    C = M/(Am*np.log(10)*Lw + Bm)
    
    a = np.cos(pi*h/180) * (C/Ak)**(1/nk)
    b = np.sin(pi*h/180) * (C/Ak)**(1/nk)
    
    Mt = np.matrix([[1.0000, 0.3215, 0.2053], [1.0000, -0.6351, -0.1860], [1.0000, -0.1568, -4.4904]])
    Mt2 = Mt @ np.matrix([[A],[a],[b]])
    Lp,Mp,Sp = Mt2.item(0),Mt2.item(1),Mt2.item(2)
    
    L = ((-(La**nc)*Lp)/(Lp-1))**(1/nc)
    M = ((-(La**nc)*Mp)/(Mp-1))**(1/nc)
    S = ((-(La**nc)*Sp)/(Sp-1))**(1/nc)

    return L,M,S
