def Zhai_Luo(Xb,Yb,Zb, Xwb,Ywb,Zwb, Db, Xws,Yws,Zws, Ds, Xwo,Ywo,Zwo, CAT="CAT02"):
    
    if CAT == "CAT02":
        Mt = np.matrix([[0.7328, 0.4296, -0.1624], [-0.7036, 1.6975, 0.0061], [0.0030, 0.0136, 0.9834]])
        
    if CAT == "CAT16":
        Mt = np.matrix([[0.401288, 0.650173, -0.051461], [-0.250268, 1.204414, 0.045854], [-0.002079, 0.048952, 0.953127]])
        
    # (4)&(5)&(6)&(7)
    M1 = Mt @ np.matrix([[Xb], [Yb], [Zb]])
    Rb,Gb,Bb = M1.item(0), M1.item(1), M1.item(2)
    M2 = Mt @ np.matrix([[Xwb], [Ywb], [Zwb]])
    Rwb,Gwb,Bwb = M2.item(0), M2.item(1), M2.item(2)
    M3 = Mt @ np.matrix([[Xws], [Yws], [Zws]])
    Rws,Gws,Bws = M3.item(0), M3.item(1), M3.item(2)
    M4 = Mt @ np.matrix([[Xwo], [Ywo], [Zwo]])
    Rwo,Gwo,Bwo = M4.item(0), M4.item(1), M4.item(2)
    
    # (8)&(9)&(10)&(11)&(12)&(13)
    Drb = Db * (Ywb/Ywo) * (Rwo/Rwb) + 1 - Db
    Dgb = Db * (Ywb/Ywo) * (Gwo/Gwb) + 1 - Db
    Dbb = Db * (Ywb/Ywo) * (Bwo/Bwb) + 1 - Db
    Drs = Ds * (Yws/Ywo) * (Rwo/Rws) + 1 - Ds
    Dgs = Ds * (Yws/Ywo) * (Gwo/Gws) + 1 - Ds
    Dbs = Ds * (Yws/Ywo) * (Bwo/Bws) + 1 - Ds
   
    # (14)&(15)&(16)
    Dr = (Drb/Drs)
    Dg = (Dgb/Dgs)
    Db = (Dbb/Dbs)
    
    # (17)&(18)&(19)
    Rs = Dr*Rb
    Gs = Dg*Gb
    Bs = Db*Bb
    
    # (20)
    Xs,Ys,Zs = (Mt**-1) @  np.matrix([[Rs] , [Gs] , [Bs]])
    
    return Xs.item(0),Ys.item(0),Zs.item(0)
  
"""
Zhai_Luo(48.900,43.620,6.250, 109.850,100,35.585, 0.9407, 95.047,100,108.883, 0.9800, 100,100,100, 'CAT16')
"""
