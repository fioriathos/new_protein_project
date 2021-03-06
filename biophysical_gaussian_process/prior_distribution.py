import numpy as np
from numpy import sqrt as Sqrt
from datetime import datetime
from numpy import pi as Pi
from numpy import exp as Exp
from scipy.special import erfi as Erfi
from scipy.integrate import dblquad,quad
#####################################################################################
############# STANDARD GAUSSIAN INTEGRALS ##########################################
####################################################################################
def zerotauint(a,b,c,t1,t0=0):
    """int_t0^t1 Exp[a*s**2+b*s+c]ds"""
    return (Exp(-b**2/(4.*a) + c)*Sqrt(Pi)*(-Erfi((b + 2*a*t0)/(2.*Sqrt(a))) + Erfi((b + 2*a*t1)/(2.*Sqrt(a)))))/(2.*Sqrt(a))
def onetauint(a,b,c,t1,t0=0):
    """int_t0^t1 s*Exp[a*s**2+b*s+c]ds"""
    return (Exp(-b**2/(4.*a) + c)*(-2*Sqrt(a)*Exp(b**2/(4.*a))*(Exp(t0*(b + a*t0)) - Exp(t1*(b + a*t1))) +\
           b*Sqrt(Pi)*Erfi((b + 2*a*t0)/(2.*Sqrt(a))) - b*Sqrt(Pi)*Erfi((b + 2*a*t1)/(2.*Sqrt(a)))))/(4.*a**1.5)
def twotauint(a,b,c,t1,t0=0):
    """int_t0^t1 s**2*Exp[a*s**2+b*s+c]ds"""
    return (Exp(-b**2/(4.*a) + c)*(-2*Sqrt(a)*Exp(b**2/(4.*a))*\
           (-(b*Exp(t0*(b + a*t0))) + b*Exp(t1*(b + a*t1)) + 2*a*Exp(t0*(b + a*t0))*t0 - 2*a*Exp(t1*(b + a*t1))*t1) +\
           (2*a - b**2)*Sqrt(Pi)*Erfi((b + 2*a*t0)/(2.*Sqrt(a))) + (-2*a + b**2)*Sqrt(Pi)*Erfi((b + 2*a*t1)/(2.*Sqrt(a)))))/(8.*a**2.5)
def treetauint(a,b,c,t1,t0=0):
    """int_t0^t1 s**3*Exp[a*s**2+b*s+c]ds"""
    return (Exp(-b**2/(4.*a) + c)*(-2*Sqrt(a)*Exp(b**2/(4.*a))*\
           (b**2*(Exp(t0*(b + a*t0)) - Exp(t1*(b + a*t1))) - 2*a*Exp(t0*(b + a*t0))*(2 + b*t0) + 2*a*Exp(t1*(b + a*t1))*(2 + b*t1) +\
            4*a**2*(Exp(t0*(b + a*t0))*t0**2 - Exp(t1*(b + a*t1))*t1**2)) + b*(-6*a + b**2)*Sqrt(Pi)*Erfi((b + 2*a*t0)/(2.*Sqrt(a))) -\
           b*(-6*a + b**2)*Sqrt(Pi)*Erfi((b + 2*a*t1)/(2.*Sqrt(a)))))/(16.*a**3.5)
######################################################################################
####### GIVEN P(z0) find P(zt) i.e. nm and nC using OU model.      ###################
####### Find also derivatives nm and nC w.r.t. hyperparameters     ###################
######################################################################################
def mean_x(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b):
    return bx+ml*t+(bl-ml)*(1-np.exp(-gl*t))/gl
def mean_g_num(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b):
    """Numerical integration over time not necessary"""
    return bg*Exp(-b*t) +quad(lambda tau:(Exp(bx + Cxx/2. + (b + bl + Cxl - gq)*tau + (Cll*tau**2)/2.)*(bq + Cxq - mq + Exp(gq*tau)*mq + Clq*tau))/Exp(b*t),0,t)[0]
def mean_g(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b):
    """Analytical integration over time not necessary"""
    return bg/Exp(b*t)+Clq*onetauint(Cll/2.,b+bl+Cxl-gq,bx+Cxx/2.-b*t,t)+mq*zerotauint(Cll/2.,b+bl+Cxl,bx+Cxx/2.-b*t,t) +\
        (bq+Cxq-mq)*zerotauint(Cll/2.,b+bl+Cxl-gq,bx+Cxx/2.-b*t,t)
def mean_l(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b):
    return ml+(bl-ml)*np.exp(-gl*t)
def mean_q(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b):
    return mq+(bq-mq)*np.exp(-gq*t)
def cov_xx(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b):
    vx = sl2/(2*gl**3)*(2*gl*t-3+4*Exp(-gl*t)-Exp(-gl*t)**2)
    return Cll*(1-Exp(-gl*t))**2/gl**2+2*Cxl*(1-Exp(-gl*t))/gl+Cxx+vx
def cov_xg_num(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b,nm):
    """Numerical integration over time not necessary"""
    return ((bg*bl + Cgl)/Exp(b*t) - (bg*bl + Cgl)/Exp((b + gl)*t) + ((bg*bx + Cxg)*gl)/Exp(b*t) - (bg*ml)/Exp(b*t) + (bg*ml)/Exp((b + gl)*t) + \
           (bg*gl*ml*t)/Exp(b*t) + quad(lambda tau: Exp(bx + Cxx/2. - b*t - gl*t + (b + bl + Cxl - gq)*tau + (Cll*tau**2)/2.)*\
           (-(bq*Cxl) - Cxl*Cxq + bq*Cxl*Exp(gl*t) + Cxl*Cxq*Exp(gl*t) + bq*bx*Exp(gl*t)*gl + Cxq*Exp(gl*t)*gl + bx*Cxq*Exp(gl*t)*gl + \
            bq*Cxx*Exp(gl*t)*gl + Cxq*Cxx*Exp(gl*t)*gl + bq*ml + Cxq*ml - bq*Exp(gl*t)*ml - Cxq*Exp(gl*t)*ml + Cxl*mq - Cxl*Exp(gl*t)*mq - \
            Cxl*Exp(gq*tau)*mq + Cxl*Exp(gl*t + gq*tau)*mq - bx*Exp(gl*t)*gl*mq - Cxx*Exp(gl*t)*gl*mq + bx*Exp(gl*t + gq*tau)*gl*mq + \
            Cxx*Exp(gl*t + gq*tau)*gl*mq - ml*mq + Exp(gl*t)*ml*mq + Exp(gq*tau)*ml*mq - Exp(gl*t + gq*tau)*ml*mq + bq*Exp(gl*t)*gl*ml*t + \
            Cxq*Exp(gl*t)*gl*ml*t - Exp(gl*t)*gl*ml*mq*t + Exp(gl*t + gq*tau)*gl*ml*mq*t - bq*Cll*tau - Cll*Cxq*tau + \
            bq*Cll*Exp(gl*t)*tau + Cll*Cxq*Exp(gl*t)*tau + bq*Cxl*Exp(gl*t)*gl*tau + Cxl*Cxq*Exp(gl*t)*gl*tau + Cll*mq*tau - \
            Cll*Exp(gl*t)*mq*tau - Cll*Exp(gq*tau)*mq*tau + Cll*Exp(gl*t + gq*tau)*mq*tau - Cxl*Exp(gl*t)*gl*mq*tau + \
            Cxl*Exp(gl*t + gq*tau)*gl*mq*tau + bl*(-1 + Exp(gl*t))*(bq + Cxq - mq + Exp(gq*tau)*mq + Clq*tau) + \
            Clq*(-1 - Cxl*tau + ml*tau - Cll*tau**2 + Exp(gl*t)*\
                (1 + bx*gl*tau + Cxx*gl*tau - ml*tau + gl*ml*t*tau + Cll*tau**2 + Cxl*tau*(1 + gl*tau)))),0,t)[0])/gl-nm[1,0]*nm[0,0]
def cov_xg(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b,nm):
	return (bg*bx)/Exp(b*t) + Cxg/Exp(b*t) + (bg*bl)/(Exp(b*t)*gl) + Cgl/(Exp(b*t)*gl) - (bg*bl)/(Exp((b + gl)*t)*gl) - \
        Cgl/(Exp((b + gl)*t)*gl) - (bg*ml)/(Exp(b*t)*gl) + (bg*ml)/(Exp((b + gl)*t)*gl) + (bg*ml*t)/Exp(b*t) + \
        (Cxl*mq + (Cll*mq)/gl)*onetauint(Cll/2.,b + bl + Cxl,bx + Cxx/2. - b*t,t) - \
        (Cll*mq*onetauint(Cll/2.,b + bl + Cxl,bx + Cxx/2. - b*t - gl*t,t))/gl + \
        (bx*Clq + bq*Cxl + Cxl*Cxq + Clq*Cxx + (bq*Cll)/gl + (bl*Clq)/gl + (Clq*Cxl)/gl + (Cll*Cxq)/gl - (Clq*ml)/gl - Cxl*mq - \
           (Cll*mq)/gl + Clq*ml*t)*onetauint(Cll/2.,b + bl + Cxl - gq,bx + Cxx/2. - b*t,t) + \
        (-((bq*Cll)/gl) - (bl*Clq)/gl - (Clq*Cxl)/gl - (Cll*Cxq)/gl + (Clq*ml)/gl + (Cll*mq)/gl)*\
         onetauint(Cll/2.,b + bl + Cxl - gq,bx + Cxx/2. - b*t - gl*t,t) + \
        (Clq*Cxl + (Cll*Clq)/gl)*twotauint(Cll/2.,b + bl + Cxl - gq,bx + Cxx/2.- b*t,t) - \
        (Cll*Clq*twotauint(Cll/2.,b + bl + Cxl - gq,bx + Cxx/2. - b*t - gl*t,t))/gl + \
        (bx*mq + Cxx*mq + (bl*mq)/gl + (Cxl*mq)/gl - (ml*mq)/gl + ml*mq*t)*zerotauint(Cll/2.,b + bl + Cxl,bx + Cxx/2. - b*t,t) + \
        (-((bl*mq)/gl) - (Cxl*mq)/gl + (ml*mq)/gl)*zerotauint(Cll/2.,b + bl + Cxl,bx + Cxx/2. - b*t - gl*t,t) + \
        (bq*bx + Cxq + bx*Cxq + bq*Cxx + Cxq*Cxx + (bl*bq)/gl + Clq/gl + (bq*Cxl)/gl + (bl*Cxq)/gl + (Cxl*Cxq)/gl - (bq*ml)/gl - \
           (Cxq*ml)/gl - bx*mq - Cxx*mq - (bl*mq)/gl - (Cxl*mq)/gl + (ml*mq)/gl + bq*ml*t + Cxq*ml*t - ml*mq*t)*\
         zerotauint(Cll/2.,b + bl + Cxl - gq,bx + Cxx/2. - b*t,t) + \
        (-((bl*bq)/gl) - Clq/gl - (bq*Cxl)/gl - (bl*Cxq)/gl - (Cxl*Cxq)/gl + (bq*ml)/gl + (Cxq*ml)/gl + (bl*mq)/gl + (Cxl*mq)/gl - \
           (ml*mq)/gl)*zerotauint(Cll/2.,b + bl + Cxl - gq,bx + Cxx/2. - b*t - gl*t,t)- nm[1,0]*nm[0,0]
def cov_xl(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b):
    cxl = sl2/(2*gl**2)*(1-Exp(-gl*t))**2
    return cxl+Cll*Exp(-gl*t)*(1-Exp(-gl*t))/gl+Cxl*Exp(-gl*t)
def cov_xq(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b):
    return Clq*(1-Exp(-gl*t))*Exp(-gq*t)/gl+Cxq*Exp(-gq*t)
def cov_gg_num(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b,nm):
    """Numerical integration over time and change variable r=t1-t2,s=t1+t2 and
    solve analytical over s already. Not necessary"""
    def vgtz0_(r):
        return Exp(2*bx+2*Cxx-2*b*t+(b+bl+2*Cxl)*(r)+(Cll*(r)**2)/2.)
    def mean_gtz0_part1(tau1):
        return  Exp(bx + (Cxx + tau1*(2*bl + 2*Cxl + Cll*tau1))/2.)*\
        (Exp(b*(-2*t + tau1))*mq*(bg + Cxg + Cgl*tau1) - Exp(-2*b*t + b*tau1 - gq*tau1)*mq*(bg + Cxg + Cgl*tau1) + \
          Exp(-2*b*t + b*tau1 - gq*tau1)*(Cgq + bg*(bq + Cxq + Clq*tau1) + (Cxg + Cgl*tau1)*(bq + Cxq + Clq*tau1)))
    def mean_gtz0_part_0t(r):
        return Exp(2*bx + 2*Cxx + b*r + bl*r + 2*Cxl*r - gq*r + (Cll*r**2)/2. - 2*b*t)*\
                (bq**2*r + Cqq*r + bq*((2*(-1 + Exp(gq*r))*mq)/gq + 2*r*(2*Cxq - mq + Clq*r)) +\
                 (Exp(gq*r)*mq*(4*Cxq + 2*Clq*r + mq*(-2 + gq*r)) + (2*Cxq - mq + Clq*r)*(gq*r*(2*Cxq + Clq*r) - mq*(2 + gq*r)))/gq)
    def mean_gtz0_part_t2t(r):
        return  Exp(2*bx + 2*Cxx + b*r + bl*r + 2*Cxl*r - gq*r + (Cll*r**2)/2. - 2*b*t)*\
                (-(bq**2*r) - Cqq*r + ((-2*Cxq + mq - Clq*r)*(2*Exp(gq*r)*mq - 2*Exp(2*gq*t)*mq + Exp(gq*t)*gq*(2*Cxq - mq + Clq*r)*(r - 2*t)) - \
            Exp(gq*(r + t))*gq*mq**2*(r - 2*t))/(Exp(gq*t)*gq) + \
	    (2*bq*(-(Exp(gq*(r - t))*mq) + Exp(gq*t)*mq - gq*(2*Cxq - mq + Clq*r)*(r - 2*t)))/gq + 2*bq**2*t + 2*Cqq*t)
    vgtz0 = sq2/(2*gq)*(quad(lambda r:\
                            ((1-Exp(-gq*r))/gq-r*Exp(-gq*r))*vgtz0_(r),0,t)[0]\
            + quad(lambda r:\
                   ((1-Exp(-gq*(2*t-r)))/gq-(2*t-r)*Exp(-gq*r))*vgtz0_(r),t,2*t)[0])
    m2gtz0 = (Cgg+bg**2)/Exp(2*b*t) +2*quad(mean_gtz0_part1, 0, t)[0] +\
              quad(mean_gtz0_part_0t, 0, t)[0]+\
              quad(mean_gtz0_part_t2t, t, 2*t)[0]
    return vgtz0 +m2gtz0-nm[1,0]**2
def cov_gg(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b,nm):
    return (bg**2 + Cgg)/Exp(2*b*t) + \
       2*Cgl*mq*onetauint(Cll/2.,b + bl + Cxl,bx + Cxx/2. - 2*b*t,t) + \
       (mq*(2*Clq + gq*mq)*onetauint(Cll/2.,b + bl + 2*Cxl,2*(bx + Cxx - b*t),t))/\
        gq + 2*(bq*Cgl + bg*Clq + Clq*Cxg + Cgl*Cxq - Cgl*mq)*\
        onetauint(Cll/2.,b + bl + Cxl - gq,bx + Cxx/2. - 2*b*t,t) + \
       ((bq**2*gq + Cqq*gq + 4*bq*Cxq*gq + 4*Cxq**2*gq - 2*Clq*mq - 2*bq*gq*mq - \
            4*Cxq*gq*mq + gq*mq**2)*\
          onetauint(Cll/2.,b + bl + 2*Cxl - gq,2*(bx + Cxx - b*t),t))/gq - \
       mq**2*onetauint(Cll/2.,b + bl + 2*Cxl,2*(bx + Cxx - b*t),2*t,t) - \
       (2*Clq*mq*onetauint(Cll/2.,b + bl + 2*Cxl,2*bx + 2*Cxx - (2*b + gq)*t,2*t,t))/\
        gq - (sq2*onetauint(Cll/2.,b + bl + 2*Cxl - gq,2*bx + 2*Cxx - 2*b*t,t,0))/\
        (2.*gq) + (sq2*onetauint(Cll/2.,b + bl + 2*Cxl - gq,2*bx + 2*Cxx - 2*b*t,2*t,\
           t))/(2.*gq) + (-bq**2 - Cqq - 4*bq*Cxq - 4*Cxq**2 + 2*bq*mq + 4*Cxq*mq - \
          mq**2 + 4*bq*Clq*t + 8*Clq*Cxq*t - 4*Clq*mq*t)*\
        onetauint(Cll/2.,b + bl + 2*Cxl - gq,2*(bx + Cxx - b*t),2*t,t) + \
       (2*Clq*mq*onetauint(Cll/2.,b + bl + 2*Cxl - gq,2*bx + 2*Cxx - 2*b*t + gq*t,2*t,\
           t))/gq + Clq**2*treetauint(Cll/2.,b + bl + 2*Cxl - gq,2*(bx + Cxx - b*t),\
         t) - Clq**2*treetauint(Cll/2.,b + bl + 2*Cxl - gq,2*(bx + Cxx - b*t),2*t,\
         t) + 2*Cgl*Clq*twotauint(Cll/2.,b + bl + Cxl - gq,bx + Cxx/2. - 2*b*t,t) + \
       (2*bq*Clq + 4*Clq*Cxq - 2*Clq*mq)*\
        twotauint(Cll/2.,b + bl + 2*Cxl - gq,2*(bx + Cxx - b*t),t) + \
       (-2*bq*Clq - 4*Clq*Cxq + 2*Clq*mq + 2*Clq**2*t)*\
        twotauint(Cll/2.,b + bl + 2*Cxl - gq,2*(bx + Cxx - b*t),2*t,t) + \
       (2*bg*mq + 2*Cxg*mq)*zerotauint(Cll/2.,b + bl + Cxl,bx + Cxx/2. - 2*b*t,t) + \
       ((2*bq*mq)/gq + (4*Cxq*mq)/gq - (2*mq**2)/gq)*\
        zerotauint(Cll/2.,b + bl + 2*Cxl,2*(bx + Cxx - b*t),t) + \
       (2*bg*bq + 2*Cgq + 2*bq*Cxg + 2*bg*Cxq + 2*Cxg*Cxq - 2*bg*mq - 2*Cxg*mq)*\
        zerotauint(Cll/2.,b + bl + Cxl - gq,bx + Cxx/2. - 2*b*t,t) + \
       ((-2*bq*mq)/gq - (4*Cxq*mq)/gq + (2*mq**2)/gq)*\
        zerotauint(Cll/2.,b + bl + 2*Cxl - gq,2*(bx + Cxx - b*t),t) + \
       (sq2*zerotauint(Cll/2.,b + bl + 2*Cxl,2*bx + 2*Cxx - 2*b*t,t,0))/(2.*gq**2) + \
       (sq2*zerotauint(Cll/2.,b + bl + 2*Cxl,2*bx + 2*Cxx - 2*b*t,2*t,t))/\
        (2.*gq**2) + 2*mq**2*t*zerotauint(Cll/2.,b + bl + 2*Cxl,2*(bx + Cxx - b*t),\
         2*t,t) + ((-2*bq*mq)/gq - (4*Cxq*mq)/gq + (2*mq**2)/gq)*\
        zerotauint(Cll/2.,b + bl + 2*Cxl,2*bx + 2*Cxx - (2*b + gq)*t,2*t,t) - \
       (sq2*zerotauint(Cll/2.,b + bl + 2*Cxl - gq,2*bx + 2*Cxx - 2*b*t,t,0))/\
        (2.*gq**2) - (sq2*t*zerotauint(Cll/2.,b + bl + 2*Cxl - gq,\
           2*bx + 2*Cxx - 2*b*t,2*t,t))/gq + \
       (2*bq**2*t + 2*Cqq*t + 8*bq*Cxq*t + 8*Cxq**2*t - 4*bq*mq*t - 8*Cxq*mq*t + \
          2*mq**2*t)*zerotauint(Cll/2.,b + bl + 2*Cxl - gq,2*(bx + Cxx - b*t),2*t,t)\
        + ((2*bq*mq)/gq + (4*Cxq*mq)/gq - (2*mq**2)/gq)*\
        zerotauint(Cll/2.,b + bl + 2*Cxl - gq,2*bx + 2*Cxx - 2*b*t + gq*t,2*t,t) - \
       (sq2*zerotauint(Cll/2.,b + bl + 2*Cxl + gq,2*bx + 2*Cxx - 2*b*t - 2*gq*t,2*t,\
           t))/(2.*gq**2)-nm[1,0]**2
def cov_gl_num(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b,nm):
    """Numerical integration over time no necessary"""
    return  (bg*bl + Cgl)/Exp((b + gl)*t) + (bg*ml)/Exp(b*t) - (bg*ml)/Exp((b + gl)*t) +\
            quad(lambda tau: Exp(bx + Cxx/2. - b*t - gl*t + (b + bl + Cxl - gq)*tau + (Cll*tau**2)/2.)*\
            ((bq + Cxq + (-1 + Exp(gq*tau))*mq)*(Cxl + (-1 + Exp(gl*t))*ml + Cll*tau) + bl*(bq + Cxq - mq + Exp(gq*tau)*mq + Clq*tau) +\
            Clq*(1 + Cxl*tau + (-1 + Exp(gl*t))*ml*tau + Cll*tau**2)),0,t)[0]-nm[1,0]*nm[2,0]
def cov_gl(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b,nm):
	return (bg*bl)/Exp((b + gl)*t) + Cgl/Exp((b + gl)*t) + (bg*ml)/Exp(b*t) - (bg*ml)/Exp((b + gl)*t) + \
        Cll*mq*onetauint(Cll/2.,b + bl + Cxl,bx + Cxx/2. - b*t - gl*t,t) + Clq*ml*onetauint(Cll/2.,b + bl + Cxl - gq,bx + Cxx/2. - b*t,t) + \
        (bq*Cll + bl*Clq + Clq*Cxl + Cll*Cxq - Clq*ml - Cll*mq)*onetauint(Cll/2.,b + bl + Cxl - gq,bx + Cxx/2. - b*t - gl*t,t) + \
        Cll*Clq*twotauint(Cll/2.,b + bl + Cxl - gq,bx + Cxx/2. - b*t - gl*t,t) + ml*mq*zerotauint(Cll/2.,b + bl + Cxl,bx + Cxx/2. - b*t,t) + \
        (bl*mq + Cxl*mq - ml*mq)*zerotauint(Cll/2.,b + bl + Cxl,bx + Cxx/2. - b*t - gl*t,t) + \
        (bq*ml + Cxq*ml - ml*mq)*zerotauint(Cll/2.,b + bl + Cxl - gq,bx + Cxx/2. - b*t,t) + \
        (bl*bq + Clq + bq*Cxl + bl*Cxq + Cxl*Cxq - bq*ml - Cxq*ml - bl*mq - Cxl*mq + ml*mq)*\
         zerotauint(Cll/2.,b + bl + Cxl - gq,bx + Cxx/2. - b*t - gl*t,t) - nm[1,0]*nm[2,0]
def cov_gq_num(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b,nm):
    """Numerical integration over time not necessary"""
    return  quad(lambda tau:(Exp(bx - b*t + b*tau + bl*tau + (Cxx + tau*(2*Cxl + Cll*tau))/2.)*(Exp(gq*(-t + tau)) - Exp(-(gq*(t + tau))))*sq2)/(2.*gq),0,t)[0]+\
            (bg*bq + Cgq)/Exp((b + gq)*t) + (bg*mq)/Exp(b*t) - (bg*mq)/Exp((b + gq)*t) + quad(lambda tau:\
            Exp(bx + Cxx/2. - b*t - gq*t + b*tau + bl*tau + Cxl*tau - gq*tau + (Cll*tau**2)/2.)*\
            (bq**2 + Cqq + (Cxq + (-1 + Exp(gq*t))*mq + Clq*tau)*(Cxq + (-1 + Exp(gq*tau))*mq + Clq*tau) +\
            bq*(2*Cxq + (-2 + Exp(gq*t) + Exp(gq*tau))*mq + 2*Clq*tau)),0,t)[0]-nm[1,0]*nm[3,0]
def cov_gq(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b,nm):
	return (bg*bq)/Exp((b + gq)*t) + Cgq/Exp((b + gq)*t) + (bg*mq)/Exp(b*t) - (bg*mq)/Exp((b + gq)*t) + \
        Clq*mq*onetauint(Cll/2.,b + bl + Cxl,bx + Cxx/2. - b*t - gq*t,t) + Clq*mq*onetauint(Cll/2.,b + bl + Cxl - gq,bx + Cxx/2. - b*t,t) + \
        (2*bq*Clq + 2*Clq*Cxq - 2*Clq*mq)*onetauint(Cll/2.,b + bl + Cxl - gq,bx + Cxx/2. - b*t - gq*t,t) + \
        Clq**2*twotauint(Cll/2.,b + bl + Cxl - gq,bx + Cxx/2. - b*t - gq*t,t) + mq**2*zerotauint(Cll/2.,b + bl + Cxl,bx + Cxx/2. - b*t,t) + \
        (bq*mq + Cxq*mq - mq**2)*zerotauint(Cll/2.,b + bl + Cxl,bx + Cxx/2. - b*t - gq*t,t) + \
        (bq*mq + Cxq*mq - mq**2)*zerotauint(Cll/2.,b + bl + Cxl - gq,bx + Cxx/2. - b*t,t) - \
        (sq2*zerotauint(Cll/2.,b + bl + Cxl - gq,-b*t + bx + Cxx/2. - gq*t,t))/(2.*gq) + \
        (bq**2 + Cqq + 2*bq*Cxq + Cxq**2 - 2*bq*mq - 2*Cxq*mq + mq**2)*zerotauint(Cll/2.,b + bl + Cxl - gq,bx + Cxx/2. - b*t - gq*t,t) + \
        (sq2*zerotauint(Cll/2.,b + bl + Cxl + gq,-b*t + bx + Cxx/2. - gq*t,t))/(2.*gq)- nm[1,0]*nm[3,0]
def cov_ll(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b):
    vl = sl2/(2*gl)*(1-Exp(-gl*t)**2)
    return Cll*Exp(-gl*t)**2 + vl
def cov_lq(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b):
    return  Clq*Exp(-gl*t)*Exp(-gq*t)
def cov_qq(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b):
    vq = sq2/(2*gq)*(1-Exp(-gq*t)**2)
    return vq + Cqq*Exp(-gq*t)**2
def mean_cov_model(m,C,t,ml,gl,sl2,mq,gq,sq2,b,num=False):
    """Given p(z0)=n(m,C) find p(z1) with no cell division"""
    nC = np.zeros((4,4))
    nm = np.zeros((4,1))
    bx=m[0,0]; bg=m[1,0]; bl=m[2,0]; bq=m[3,0]
    Cxx=C[0,0];Cxg=C[0,1];Cxl=C[0,2];Cxq=C[0,3];Cgg=C[1,1];Cgl=C[1,2];Cgq=C[1,3];Cll=C[2,2];Clq=C[2,3];Cqq=C[3,3]
    #####################
    ######   Mean     ###
    #####################
#    start = datetime.now()
    nm[0,0] = mean_x(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b)
    if num:
        nm[1,0] = mean_g_num(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b)
    else:
        nm[1,0] = mean_g(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b)
    nm[2,0] = mean_l(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b)
    nm[3,0] = mean_q(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b)
#    print("mean",datetime.now()-start)
    ####################
    ####### Cov ########
    ####################
#    start = datetime.now()
    nC[0,0] = cov_xx(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b)
    nC[0,2] = cov_xl(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b)
    nC[0,3] = cov_xq(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b)
    if num:
        nC[0,1] = cov_xg_num(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b,nm)
        nC[1,2] = cov_gl_num(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b,nm)
        nC[1,3] = cov_gq_num(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b,nm)
    else:
        nC[0,1] = cov_xg(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b,nm)
        nC[1,2] = cov_gl(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b,nm)
        nC[1,3] = cov_gq(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b,nm)
    nC[2,2] = cov_ll(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b)
    nC[2,3] = cov_lq(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b)
    nC[3,3] = cov_qq(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b)
#    print('cov',datetime.now()-start)
#    start = datetime.now()
    nC[1,1] = cov_gg(t,bx,bg,bl,bq,Cxx,Cxg,Cxl,Cxq,Cgg,Cgl,Cgq,Cll,Clq,Cqq,ml,gl,sl2,mq,gq,sq2,b,nm)
#    print('var',datetime.now()-start)
    ####################
    #### return     ####
    ####################
    nC[1,0]=nC[0,1];nC[2,0]=nC[0,2];nC[2,1]=nC[1,2];nC[3,0]=nC[0,3];nC[3,1]=nC[1,3];nC[3,2]=nC[2,3]
    return nm,nC
