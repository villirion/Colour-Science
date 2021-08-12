import numpy as np

def Zhai_Luo_inverse(Xs,Ys,Zs, Xwb,Ywb,Zwb, Db, Xws,Yws,Zws, Ds, Xwo,Ywo,Zwo, CAT="CAT02"):
    
    if CAT == "CAT02":
        Mt = np.array([
            [0.7328, 0.4296, -0.1624],
            [-0.7036, 1.6975, 0.0061],
            [0.0030, 0.0136, 0.9834],
        ])
        
    if CAT == "CAT16":
        Mt = np.array([
            [0.401288, 0.650173, -0.051461],
            [-0.250268, 1.204414, 0.045854],
            [-0.002079, 0.048952, 0.953127],
        ])
        
    Rwb,Gwb,Bwb = Mt @ np.array([[Xwb], [Ywb], [Zwb]])
    Rws,Gws,Bws = Mt @ np.array([[Xws], [Yws], [Zws]])
    Rwo,Gwo,Bwo = Mt @ np.array([[Xwo], [Ywo], [Zwo]])

    Drb = Db * (Ywb/Ywo) * (Rwo/Rwb) + 1 - Db
    Dgb = Db * (Ywb/Ywo) * (Gwo/Gwb) + 1 - Db
    Dbb = Db * (Ywb/Ywo) * (Bwo/Bwb) + 1 - Db
    Drs = Ds * (Yws/Ywo) * (Rwo/Rws) + 1 - Ds
    Dgs = Ds * (Yws/Ywo) * (Gwo/Gws) + 1 - Ds
    Dbs = Ds * (Yws/Ywo) * (Bwo/Bws) + 1 - Ds
    
    Dr = (Drb/Drs)
    Dg = (Dgb/Dgs)
    Db = (Dbb/Dbs)
    
    Rs, Gs, Bs = Mt @  np.array([[Xs],[Ys],[Zs]])
    
    Rb = Rs/Dr
    Gb = Gs/Dg
    Bb = Bs/Db
    
    Rs = Dr*Rb
    Gs = Dg*Gb
    Bs = Db*Bb
    
    Xb,Yb,Zb = np.linalg.inv(Mt) @ np.array([Rb, Gb, Bb])
    
    return Xb.item(0),Yb.item(0),Zb.item(0)
    
"""
Zhai_Luo_inverse(40.374,43.694,20.517, 109.850,100,35.585, 0.9407, 95.047,100,108.883, 0.9800, 100,100,100, 'CAT16')
"""
