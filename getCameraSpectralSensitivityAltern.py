def getCameraSpectralSensitivity():

    prefix = 'camSpecSensitivity/cmf_'
    suffix = '.mat'
    listFiles = prefix + '*' + suffix
    matdict = {'r':np.array([]),'g':np.array([]),'b':np.array([])}
    camName = []
    Files = sorted(glob.glob(listFiles))
    for i in range(0, len(Files)):
        file = Files[i]
        mat = scipy.io.loadmat(file)
        if i == 0:
            matdict['r'] = np.array([v[0] for k, v in mat.items() if k[0] == 'r'])
            matdict['g'] = np.array([v[0] for k, v in mat.items() if k[0] == 'g'])
            matdict['b'] = np.array([v[0] for k, v in mat.items() if k[0] == 'b'])
        else:
            if len(mat['r'])==1:
                matdict['r'] = np.vstack((matdict['r'],np.array([v[0] for k, v in mat.items() if k[0] == 'r'])))
                matdict['g'] = np.vstack((matdict['g'],np.array([v[0] for k, v in mat.items() if k[0] == 'g'])))
                matdict['b'] = np.vstack((matdict['b'],np.array([v[0] for k, v in mat.items() if k[0] == 'b'])))
            else:
                matdict['r'] = np.vstack((matdict['r'],np.array([v.reshape(len(v)) for k, v in mat.items() if k[0] == 'r'])))
                matdict['g'] = np.vstack((matdict['g'],np.array([v.reshape(len(v)) for k, v in mat.items() if k[0] == 'g'])))
                matdict['b'] = np.vstack((matdict['b'],np.array([v.reshape(len(v)) for k, v in mat.items() if k[0] == 'b'])))
        camName.append(file[len(prefix):-len(suffix)])
        
        
    return matdict, camName
