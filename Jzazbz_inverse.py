import numpy as np

def Jzazbz_inverse(h, Q, C, La, c):
    
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
    
    hi, hp, hip, Hi, ei, eip = get_val(h)
    et = 1.01+np.cos(1.55+(hp*pi)/180)
    t = (n**0.074 * C * (1/et)**0.067)**(1/0.37)    
    
    az = (t / (1 + np.tan(h*np.pi/180)**2))**0.5
    bz = az*np.tan(h*np.pi/180)
    
    FL = get_FL(La) 
    
    #tester equa I
    I = np.exp(np.log(Q / 192 / np.sqrt(FL/c))/1.17)
    I = 0.0111804810096925*(Q*(FL/c)**(-0.5))**(100/117)
    
    Mt2 = np.array([
        [0,        1,         0],
        [3.524000, -4.066708, 0.542708],
        [0.199076, 1.096799, -1.295875],
    ])
    
    Rp, Gp, Bp = np.linalg.inv(Mt2) @ np.array([[I], [az], [bz]])
    
    #retourner l'equation
    R = (10000**n*(-Rp**(1/p) + c1)/(Rp**(1/p)*c3 - c2))**(1/n)
    G = (10000**n*(-Gp**(1/p) + c1)/(Gp**(1/p)*c3 - c2))**(1/n)
    B = (10000**n*(-Bp**(1/p) + c1)/(Bp**(1/p)*c3 - c2))**(1/n)

    Mt = np.array([
        [0.41478972, 0.579999, 0.0146480],
        [-0.2015100, 1.120649, 0.0531008],
        [-0.0166008, 0.264800, 0.6684799],
    ])
    
    Xdp65, Ydp65, Zd65 = np.linalg.inv(Mt) @ np.array([R, G, B])
    
    Xd65 = (Xdp65 + (b-1)*Zd65)/b 
    Yd65 = (Ydp65 + (g-1)*Xd65)/g 
    
    return Xd65,Yd65,Zd65

"""
#input : 

h = -0.13977254973597023
Q = 6.599321089883086e+138
C = 5.8218574120673214e+85
L_A = 318.31
c = 0.69

Jzazbz_inverse(h,Q,C,L_A,c)
"""
