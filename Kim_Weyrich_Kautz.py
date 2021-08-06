import numpy as np

def Kim_Weyrich_Kautz(L,M,S, Lw,Mw,Sw, La):
    # The adaptation level should ideally be the average luminance of the 10 degres
    # viewing field (it serves as an input parameter to our model).

    #The parameter nc is known only for primates, hence we have derived it from our experimental data as nc = 0.57.
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

    # A value of E = 1.0 corresponds to a high-luminance LCD display, transparent
    # advertising media yield E = 1.2175, CRT displays are E = 1.4572,
    # and reflective paper is E = 1.7526. These parameters were derived
    # from the LUTCHI data set as well as ours.
    
    E = 1 #for test question how changing it
    
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
    C = Ak*(sqrt(a**2+b**2)**nk)
    M = C*(Am*np.log(10)*Lw+Bm) #verifier log 

    # (12)
    S = 100*np.sqrt(M/Q)

    # (13)
    h = (180/pi)*np.tan(b/a)**(-1)
    
    print("Lightness : ", J, "\nBrightness : ", Q, "\nChroma : ", C, 
          "\nColourfulness : ", M,"\nSaturation : ", S, "\nHue angle : ", h)

    return J,Q,C,M,S,h
