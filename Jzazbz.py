import numpy as np

def Jzazbz(Xd65,Yd65,Zd65,Yb,Yw,La,c):
    
    def get_alpha(Yb,Yw):
        alpha = 1.2 + 1.7*np.sqrt(Yb/Yw)
        return alpha

    def get_FL(La):
        k = (5*La + 1)**(-1)
        FL = La*(k**4) + 0.1*((1-(k**4))**2)*((5*La)**(1/3))
        return FL
    
    # use for (5)
    def get_val(h): 
        #  Red        Yellow       Green       Blue        Red
        h1 = 33.44; h2 = 88.29; h3 = 146.30; h4 = 238.36; h5 = 393.44
        H1 = 0.0; H2 = 100.0; H3 = 200.0; H4 = 300.0; H5 = 400.0
        e1 = 0.68; e2 = 0.64; e3 = 1.52; e4 = 0.77; e5 = 0.68

        if h<33.44:
            hp = h + 360
        else:
            hp = h
        if h1<=hp<h2:
            return h1,hp,h2,H1,e1,e2
        if h2<=hp<h3:
            return h2,hp,h3,H2,e2,e3
        if h3<=hp<h4:
            return h3,hp,h4,H3,e3,e4
        if h4<=hp<h5:
            return h4,hp,h5,H4,e4,e5
    
    # variable
    b = 1.16; g = 0.7; c1 = 3424/(2**12)
    c2 = 2413/(2**7); c3 = 2392/(2**14)
    n = 2610/(2**14); p = 1.7*2523/(2**5)
    pi = np.pi
    
    #(1) 
    M1 = np.matrix([[b*Xd65],[g*Yd65]]) - np.matrix([[(b-1)*Zd65],[(g-1)*Xd65]])
    Xdp65,Ydp65 = M1.item(0), M1.item(1)
    
    #(2)
    Mt = np.matrix([[0.41478972, 0.579999, 0.0146480], [-0.2015100, 1.120649, 0.0531008], [-0.0166008, 0.264800, 0.6684799]])

    M2 = Mt @ np.matrix([[Xdp65], [Ydp65], [Zd65]])
    R,G,B = M2.item(0), M2.item(1), M2.item(2)
    
    #(3) 
    Rp = ((c1+c2*(R/10000)**n)/(1+c3*(R/10000)**n))**p
    Gp = ((c1+c2*(G/10000)**n)/(1+c3*(G/10000)**n))**p
    Bp = ((c1+c2*(B/10000)**n)/(1+c3*(B/10000)**n))**p

    # (4) 
    Mt2 = np.matrix([[0,        1,         0,], [3.524000, -4.066708, 0.542708,], [0.199076, 1.096799, -1.295875]])

    M3 = Mt2 @ np.matrix([[Rp], [Gp], [Bp]])
    I,az,bz = M3.item(0), M3.item(1), M3.item(2)

    #(5)
    h = np.arctan(bz/az) # 0<=h<=360
    hi, hp, hip, Hi, ei, eip = get_val(h)

    # (6) 
    et = 1.01+np.cos(1.55+(hp*pi)/180)
    H = Hi+ (100*(hp-hi)/ei)/(((hp-hi)/ei)+((hip-hp)/eip))

    # (7) La en input yb yw pas sur de ce que c'est
    FL = get_FL(La) 
    alpha = get_alpha(Yb,Yw)

    # c en input
    Q = 192 * I**1.17 * np.sqrt(FL/c)
    
    # (8) Qn = Q*n ?
    J = 89*(Q/(Q*n))**(0.72*c*alpha)

    # (9) 
    C = (1/n)**0.074*(az**2+bz**2)**0.37*(et)**0.067

    # (10) 
    M = 1.42*C*(FL)**0.25

    # (11) 
    S = 100*(M/Q)**0.5
    
    """
    # (12) L = J ? Cab = C ou Cab = M?
    Wab = 100 - np.sqrt((100-L)**2+(Cab)**2)

    # (13) 
    Kab = 100 - np.sqrt((L)**2+(Cab)**2)

    # (14) 
    Vab = np.sqrt((50-L)**2+(Cab)**2)

    # (15) 
    Chrom = 100 - Wab - Kab
    """
    
    print("Lightness : ", J, "\nBrightness : ", Q, "\nChroma : ", C, "\nColourfulness : ", M, "\nSaturation : ", S)

    return J,Q,C,M,S
  
"""
#input : 

XYZ = np.array([19.01, 20.00, 21.78])
X = XYZ[0]
Y = XYZ[1]
Z = XYZ[2]
XYZ_w = np.array([95.05, 100.00, 108.88])
Yw = XYZ_w[1]
L_A = 318.31
Y_b = 20.0
c = 0.69

Jzazbz(X,Y,Z,Y_b,Yw,L_A,c)
"""
