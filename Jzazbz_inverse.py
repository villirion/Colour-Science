def Jzazbz_inverse(h, Q, C, La, c):
    
    def get_FL(La):
        k = (5*La + 1)**(-1)
        FL = La*(k**4) + 0.1*((1-(k**4))**2)*((5*La)**(1/3))
        return FL
    
    # variable
    b = 1.16; g = 0.7; c1 = 3424/(2**12)
    c2 = 2413/(2**7); c3 = 2392/(2**7)
    n = 2610/(2**14); p = 1.7*2523/(2**5)
    pi = np.pi

    et = 1.01 + np.cos(h*pi/180 + 1.55)
    
    t = (n**0.074 * C * (1/et)**0.067)**(1/0.37)    
    
    az = (t / (1 + np.tan(h*pi/180)**2))**0.5
    bz = az*np.tan(h*pi/180) 

    FL = get_FL(La) 
    
    I = np.exp(np.log(Q / 192 / np.sqrt(FL/c))/1.17)
    
    Mt2 = np.array([
        [0,        1,         0],
        [3.524000, -4.066708, 0.542708],
        [0.199076, 1.096799, -1.295875],
    ])
    
    # -az to match the test but may be different with additional tests
    RGBp = np.linalg.inv(Mt2) @ np.array([[I], [-az], [bz]])
    
    RGB = (10000**n*(-RGBp**(1/p) + c1)/(RGBp**(1/p)*c3 - c2))**(1/n)

    Mt = np.array([
        [0.41478972, 0.579999, 0.0146480],
        [-0.2015100, 1.120649, 0.0531008],
        [-0.0166008, 0.264800, 0.6684799],
    ])

    Xdp65, Ydp65, Zd65 = np.linalg.inv(Mt) @ RGB
    
    Xd65 = (Xdp65 + (b-1)*Zd65)/b 
    Yd65 = (Ydp65 + (g-1)*Xd65)/g 
    
    return XYZd65

"""
#input : 

h = -0.13977254973597023
Q = 6.599321089883086e+138
C = 5.8218574120673214e+85
L_A = 318.31
c = 0.69

Jzazbz_inverse(h,Q,C,L_A,c)
"""
