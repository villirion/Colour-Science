import numpy as np

def Jzazbz(XYZd65,Yb,Yw,La,c):
    
    def get_alpha(Yb,Yw):
        alpha = 1.2 + 1.7*np.sqrt(Yb/Yw)
        return alpha

    def get_FL(La):
        k = (5*La + 1)**(-1)
        FL = La*(k**4) + 0.1*((1-(k**4))**2)*((5*La)**(1/3))
        return FL
    
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
    
    b = 1.16; g = 0.7; c1 = (3424)/(2**12)
    c2 = (2413)/(2**7); c3 = (2392)/(2**7)
    n = (2610)/(2**14); p = (1.7*2523)/(2**5)
    pi = np.pi
    
    Xdp65,Ydp65 = np.array([[b*XYZd65[0]],[g*XYZd65[1]]]) - np.array([[(b-1)*XYZd65[2]],[(g-1)*XYZd65[0]]])
    
    Mt = np.array([
        [0.41478972, 0.579999, 0.0146480],
        [-0.2015100, 1.120649, 0.0531008], 
        [-0.0166008, 0.264800, 0.6684799],
    ])
    
    RGB = Mt @ np.array([Xdp65, Ydp65, [XYZd65[2]]])
    
    RGBp = ( ( c1 + c2*(RGB/10000)**n ) / ( 1 + c3*(RGB/10000)**n ) )**p

    Mt2 = np.array([
        [0,        1,         0],
        [3.524000, -4.066708, 0.542708],
        [0.199076, 1.096799, -1.295875],
    ])
    
    I,az,bz  = Mt2 @ RGBp

    h = np.arctan(bz.item(0)/az.item(0)) # 0<=h<=360
    h = -(h*180/pi)
    hi, hp, hip, Hi, ei, eip = get_val(h)

    et = 1.01+np.cos(1.55+(hp*pi)/180)
    H = Hi + (100*(hp-hi)/ei)/(((hp-hi)/ei)+((hip-hp)/eip))

    FL = get_FL(La) 
    alpha = get_alpha(Yb,Yw)

    Q = 192 * I.item(0)**1.17 * np.sqrt(FL/c)
    
    J = 89*(Q/(Q*n))**(0.72*c*alpha)

    C = (1/n)**0.074*(az.item(0)**2+bz.item(0)**2)**0.37*(et)**0.067

    M = 1.42*C*(FL)**0.25

    S = 100*(M/Q)**0.5
    
    # print("Lightness : ", J, "\nBrightness : ", Q, "\nChroma : ", C, 
    #"\nColourfulness : ", M, "\nSaturation : ", S, "\nHue angle :", h)

    return J,Q,C,M,S,h
  
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
