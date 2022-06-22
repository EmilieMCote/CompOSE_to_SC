import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rc
import scipy.constants as const
from scipy.optimize import root as root
from scipy.special import sph_harm
import matplotlib
from matplotlib import rcParams
import pylab
import os
from scipy.interpolate import griddata
import h5py
import scipy as sp
import warnings


def plot_EOS(filename_CO):
    f2 = h5py.File(filename_CO, 'r')

    keys2 = list(f2.keys())
    possible_varnames=['Abar','Xa','Xh','Xn','Xp','Zbar','cs2','dedt','dpderho','dpdrhoe','energy_shift','entropy',
                   'gamma','logenergy','logpress','logrho','logtemp','mu_e','mu_n','mu_p','muhat','munu',
                   'pointsrho','pointstemp','pointsye','ye']

    CO_EOS=[]
    for i in range(0, len(keys2)):
        print("%d: %s" %(i, keys2[i]))
        CO_EOS.append(np.array(f2.get(keys2[i])))
    
    #Get the closest entry in the temperature that corresponds to 0.1 MeV
    T_target=0.1

    Tcold_index_CO=list(10.**CO_EOS[keys2.index('logtemp')]-T_target).index(np.min(np.abs(10.**CO_EOS[keys2.index('logtemp')] - T_target)))

    print(Tcold_index_CO, 10.**CO_EOS[keys2.index('logtemp')][Tcold_index_CO])

    logRho_CO=[]
    Yebeta_CO=[]
    logPressbeta_CO=[]
    logEnergybeta_CO=[]
    dedt_CO=[]
    dpderho_CO=[]
    dpdrhoe_CO=[]
    mu_e_CO=[]
    mu_n_CO=[]
    mu_p_CO=[]
    entropy_CO=[]
    cs2_CO=[]


    for rho_index in range(0, len(CO_EOS[keys2.index('logrho')])):
        #at each value of the rest mass density, calculate mu_beta as the absolute value of mu_n - mu_p - mu_e = 0
        #find the closest value of mu_beta to zero (minimum), and get its index
        mu_betaCO = list(np.abs(CO_EOS[keys2.index('mu_n')][:,Tcold_index_CO,rho_index] - CO_EOS[keys2.index('mu_p')][:,Tcold_index_CO,rho_index] - CO_EOS[keys2.index('mu_e')][:,Tcold_index_CO,rho_index]))

        #beta-equilibrium corresponds to the closest value of mu_beta to zero, find the index
        Yebeta_index_CO = list(mu_betaCO).index(np.min(mu_betaCO))
        #print(CO_EOS[keys2.index('logrho')][rho_index], np.min(mu_betaCO), Yebeta_index_CO)
    
        #keep the current value of rho, the value of Ye that corresponds to beta-equilibrium,
        #and the Pressure at this rho and Ye (temperature has been fixed to 0.1 MeV)
        #do the same for the energy density
        logRho_CO.append(CO_EOS[keys2.index('logrho')][rho_index])
        Yebeta_CO.append(CO_EOS[keys2.index('ye')][Yebeta_index_CO])
        logPressbeta_CO.append(CO_EOS[keys2.index('logpress')][Yebeta_index_CO][Tcold_index_CO][rho_index])
        logEnergybeta_CO.append(CO_EOS[keys2.index('logenergy')][Yebeta_index_CO][Tcold_index_CO][rho_index])
        dedt_CO.append(CO_EOS[keys2.index('dedt')][Yebeta_index_CO][Tcold_index_CO][rho_index])
        dpderho_CO.append(CO_EOS[keys2.index('dpderho')][Yebeta_index_CO][Tcold_index_CO][rho_index])
        dpdrhoe_CO.append(CO_EOS[keys2.index('dpdrhoe')][Yebeta_index_CO][Tcold_index_CO][rho_index])
        mu_e_CO.append(CO_EOS[keys2.index('mu_e')][Yebeta_index_CO][Tcold_index_CO][rho_index])
        mu_n_CO.append(CO_EOS[keys2.index('mu_n')][Yebeta_index_CO][Tcold_index_CO][rho_index])
        mu_p_CO.append(CO_EOS[keys2.index('mu_p')][Yebeta_index_CO][Tcold_index_CO][rho_index])
        entropy_CO.append(CO_EOS[keys2.index('entropy')][Yebeta_index_CO][Tcold_index_CO][rho_index])
        cs2_CO.append(CO_EOS[keys2.index('cs2')][Yebeta_index_CO][Tcold_index_CO][rho_index])
    
    #make a figure of size 15,10 with 2 rows and 3 columns
    fig, ax= plt.subplots(nrows=3, ncols=4,figsize=(11,7), tight_layout=True)
    #define the subplot for this figure, we are only doing one subplot for now
    #set the value of the line width and font size
    universal_linewidth=2
    universal_fontsize=11
    
    fig.suptitle("EOS Variables wrt restmass density Corresponding to Beta-Equilibrium")
    
    #SECOND EOS PLOTS
    ax[0][0].plot(logRho_CO, Yebeta_CO, color='pink')
    ax[0][0].set_xlabel(r'$\log(\rho \rm{ (g/cm^3)})$', fontsize=universal_fontsize)
    ax[0][0].set_ylabel(r'$Y_{e}^\beta$', fontsize=universal_fontsize)

    ax[0][1].plot(logRho_CO, logPressbeta_CO, color='skyblue')
    ax[0][1].set_xlabel(r'$\log(\rho \rm{ (g/cm^3)})$', fontsize=universal_fontsize)
    ax[0][1].set_ylabel(r'$\log(P \rm{ (dyn/cm^2)})$', fontsize=universal_fontsize)

    ax[0][2].plot(logRho_CO, logEnergybeta_CO, color='lightgreen')
    ax[0][2].set_xlabel(r'$\log(\rho \rm{ (g/cm^3)})$', fontsize=universal_fontsize)
    ax[0][2].set_ylabel(r'$\log(\epsilon \rm{ (erg/g)})$', fontsize=universal_fontsize)

    ax[0][3].plot(logRho_CO, dedt_CO, color='pink')
    ax[0][3].set_xlabel(r'$\log(\rho \rm{ (g/cm^3)})$', fontsize=universal_fontsize)
    ax[0][3].set_ylabel(r'$dedt$', fontsize=universal_fontsize)

    #ax[1][0].semilogy(logRho_CO, dpderho_CO, color='pink')
    ax[1][0].plot(logRho_CO, dpderho_CO, color='pink')
    ax[1][0].set_xlabel(r'$\log(\rho \rm{ (g/cm^3)})$', fontsize=universal_fontsize)
    ax[1][0].set_ylabel(r'$dpde\rho$', fontsize=universal_fontsize)

    #ax[1][1].semilogy(logRho_CO, dpdrhoe_CO, color='skyblue')
    ax[1][1].plot(logRho_CO, dpdrhoe_CO, color='skyblue')
    ax[1][1].set_xlabel(r'$\log(\rho \rm{ (g/cm^3)})$', fontsize=universal_fontsize)
    ax[1][1].set_ylabel(r'$dpd\rho e$', fontsize=universal_fontsize)

    ax[1][2].plot(logRho_CO, mu_e_CO, color='lightgreen')
    ax[1][2].set_xlabel(r'$\log(\rho \rm{ (g/cm^3)})$', fontsize=universal_fontsize)
    ax[1][2].set_ylabel(r'$\mu_e$', fontsize=universal_fontsize)

    ax[1][3].plot(logRho_CO, mu_n_CO, color='pink')
    ax[1][3].set_xlabel(r'$\log(\rho \rm{ (g/cm^3)})$', fontsize=universal_fontsize)
    ax[1][3].set_ylabel(r'$\mu_n$', fontsize=universal_fontsize)

    ax[2][0].plot(logRho_CO, mu_p_CO, color='pink')
    ax[2][0].set_xlabel(r'$\log(\rho \rm{ (g/cm^3)})$', fontsize=universal_fontsize)
    ax[2][0].set_ylabel(r'$\mu_p$', fontsize=universal_fontsize)

    ax[2][1].plot(logRho_CO, entropy_CO, color='skyblue')
    ax[2][1].set_xlabel(r'$\log(\rho \rm{ (g/cm^3)})$', fontsize=universal_fontsize)
    ax[2][1].set_ylabel(r'$S_{entropy}$', fontsize=universal_fontsize)

    ax[2][2].plot(logRho_CO, cs2_CO, color='lightgreen')
    ax[2][2].set_xlabel(r'$\log(\rho \rm{ (g/cm^3)})$', fontsize=universal_fontsize)
    ax[2][2].set_ylabel(r'$c^2$', fontsize=universal_fontsize)
    
    ax[2][3].axis('off')

    return fig




