import numpy as np

def RecoverCMFev(ill,reflSet,w,XYZSet,e):

    numRefl = reflSet.shape[1]

    A = np.zeros(numRefl,e.shape[1])
    b = np.zeros(A.shape[0],1)

    deltaLambda = 10
    weight = 1 
    
    for i in range(0,numRefl):
        #weight=XYZSet(i)
        A[i,:] = reflSet[:,i].conj().transpose() @ np.diag(ill) @ e * deltaLambda * weight #maybe different operator
        b[i] = XYZSet[i]*weight #? if weight = 1 

    X = linalg.lstsq(A,b)
    #X = lsqnonneg(A,b);

    X = e*X


    return X,A,b
