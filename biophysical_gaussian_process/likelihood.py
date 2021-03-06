import numpy as np
from numpy import sqrt as Sqrt
from numpy import pi as Pi
from numpy import exp as Exp
from datetime import datetime
from biophysical_gaussian_process.prior_distribution import mean_cov_model as mean_cov_model
##############################################################################
#############################DIVISON, LIKELIHOOD AND POSTERIOR###############
##############################################################################
def division(m,C,sdx2,sdg2):
    """Given p(z_t) find division at t. Return mean and cov"""
    F = np.zeros((4,4))
    np.fill_diagonal(F,[1,1/2,1,1])
    f = np.array([-np.log(2),0,0,0]).reshape(4,1)
    D = np.zeros((4,4))
    np.fill_diagonal(D,[sdx2,sdg2,0,0])
    return F@m+f, D+F@C@F.T
def log_likelihood(y,m,C,sx2,sg2):
    """Given y_t=(x_t,g_t), p(z_t) and errors find p(y_t). Return log lik """
    D = np.zeros((2,2))
    D[0,0]=sx2;D[1,1]=sg2
    Si = np.linalg.inv(C[:2,:2]+D)
    S = C[:2,:2]+D
    y = y-m[:2,:]
    log_lik = -1/2*y.T@Si@y-1/2*np.log(np.linalg.det(S))-2*np.log(2*Pi)
    return log_lik
def posterior(y,m,C,sx2,sg2):
    """Given y_t and the p(z_t) prior, find p(z_t|y_t). Return mean and cov"""
    D = np.zeros((2,2))
    D[0,0]=sx2;D[1,1]=sg2
    Si = np.linalg.inv(C[:2,:2]+D)
    K = C[:2,:]
    y = y-m[:2,:]
    return m+K.T@Si@y, C-K.T@Si@K
def total_likelihood(Y,m,C,ml,gl,sl2,mq,gq,sq2,b,sx2,sg2,sdx2,sdg2,num=False):
    """Y=[x,g,time,cell_id] must be connected in genealogy, time ordered and
    maximun 1 division apart i.e. mother daugther relationship """
    log_lik=0
    XG = Y[:,:2].astype('float64');T=Y[:,2:3].astype('float64');ID=Y[:,3:4]
    T = T-T[0,0]
#    start = datetime.now()
    for i in range(T.shape[0]):
        #Initial condition
        if i==0:
            nm=m;nC=C
        # Cell division
        if i!=0 and ID[i,0]!=ID[i-1,0]:
#            sta1 = datetime.now()
            nm,nC = division(nm,nC,sdx2,sdg2)
#            print("div",datetime.now()-sta1)
        # Measure
        y = XG[i:i+1,:].T
        # COMPUTE LIKELIHOOD
#        sta1 = datetime.now()
        log_lik+=log_likelihood(y,nm,nC,sx2,sg2)
#        print('likelihood',datetime.now()-sta1)
        # COMPUTE POSTERIOR
#        sta1 = datetime.now()
        nm,nC= posterior(y,nm,nC,sx2,sg2)
#        print('posterior',datetime.now()-sta1)
        # NEXT TIME POINT PRIOR NO DIVISION
        if i<T.shape[0]-1:
            dt = T[i+1,0]-T[i,0]
            #sta1=datetime.now()
            nm,nC = mean_cov_model(nm,nC,dt,ml,gl,sl2,mq,gq,sq2,b,num)
#            print('update',datetime.now()-sta1)
#    print('total time',datetime.now()-start)
    return log_lik
