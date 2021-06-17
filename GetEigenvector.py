def GetEigenvector(refl,retainE=6):
    
    A = refl.conj().transpose()  @ refl 
  
    v, e = np.linalg.eigh(A)

    #v = np.diag(v)
    
    v = v[-(retainE):]
    e = e[:,-(retainE):]

    v = np.flipud(v)
    e = np.fliplr(e)
    
    return (e,v)
