import numpy as np
import os
import h5py
from CompOSE_to_SC.ConstantsAndConversions import *
from collections import OrderedDict
import warnings

def conv_h5(filename,new_file):
    """Convert H5

    Convert an H5 file from the CompOSE format to the stellarcollapse format

    Args:
        filename (str): input file in CompOSE format
        new_file (str): output file in stellarcollapse format

    Returns:
        None
    
    """
    if os.path.exists(new_file):
        os.remove(new_file)

    f = h5py.File(filename, 'r')
    n = h5py.File(new_file, 'w-', track_order=True)

    try:
        ye = f['Parameters'].get('yq')     # shape == (71) dtype == f8
    except KeyError:
        warnings.warn('File[Parameters][yq]-->ye not found')
        ye = np.zeros(71,dtype='f8')
    try:
        nb = f['Parameters'].get('nb')    # shape == (114) dtype == f8
    except KeyError:
        warnings.warn('File[Parameters][nb]-->nb not found')
        nb = np.zeros(114,dtype='f8')
    try:
        temp = f['Parameters'].get('t')    # shape == (34) dtype == f8
    except KeyError:
        warnings.warn('File[Parameters][t]-->temp not found')
        temp = np.zeros(34,dtype='f8')

    try:
        EOS = f['Thermo_qty'].get('thermo')
    except KeyError:
        warnings.warn('File[Thermo_qty][thermo]-->EOS not found')
        EOS = np.zeros(24,dtype='i4')
    try:
        EOS_index = f['Thermo_qty'].get('index_thermo')     # shape == 24 dtype == i4
    except KeyError:
        warnings.warn('File[Thermo_qty][index_thermo]-->EOS_index not found')
        EOS_index = np.zeros(24,dtype='i4')
        
    try:
        yi = f['Composition_pairs'].get('yi')               # shape == (7, 71, 34, 114) dtype == f8 # relative abundance like electron frac for other isotopes
    except KeyError:
        warnings.warn('File[Composition_pairs][yi]-->yi not found')
        yi = np.zeros((7, 71, 34, 114),dtype='f8')
    try:
        yi_index = f['Composition_pairs'].get('index_yi')   # shape == (7) dtype == i4
    except KeyError:
        warnings.warn('File[Composition_pairs][index_yi]-->yi_index not found')
        yi_index = np.zeros(7,dtype='i4')

    try:
        micro = f['Micro_qty'].get('micro')                 # shape == (2, 71, 34, 114) dtype == f8
    except KeyError:
        warnings.warn('File[Micro_qty][micro]-->micro not found')
        micro = np.zeros((2, 71, 34, 114),dtype='f8')
    try:
        index_micro = f['Micro_qty'].get('index_micro')     # shape == (1) dtype == i4
    except KeyError:
        warnings.warn('File[Micro_qty][index_micro]-->index_micro not found')
        index_micro = np.zeros(1,dtype='i4')
    
    try:
        aav = f['Composition_quadrupels'].get('aav')            # shape == (1, 71, 34, 114) dtype == f8  'Abar'
    except KeyError:
        warnings.warn('File[Composition_quadrupels][aav]-->aav not found')
        aav = np.zeros((1, 71, 34, 114),dtype='f8')
    try:
        index_av = f['Composition_quadrupels'].get('index_av')  # shape == (1) dtype == i4
    except KeyError:
        warnings.warn('File[Composition_quadrupels][index_aav]-->index_aav not found')
        index_av = np.zeros(1,dtype='i4')
    try:
        nav = f['Composition_quadrupels'].get('nav')            # shape == (1, 71, 34, 114) dtype == f8
    except KeyError:
        warnings.warn('File[Composition_quadrupels][nav]-->nav not found')
        nav = np.zeros((1, 71, 34, 114),dtype='f8')
    try:
        yav = f['Composition_quadrupels'].get('yav')            # shape == (1, 71, 34, 114) dtype == f8
    except KeyError:
        warnings.warn('File[Composition_quadrupels][yav]-->yav not found')
        yav = np.zeros((1, 71, 34, 114),dtype='f8')
    try:
        zav = f['Composition_quadrupels'].get('zav')            # shape == (1, 71, 34, 114) dtype == f8
    except KeyError:
        warnings.warn('File[Composition_quadrupels][zav]-->zav not found')
        zav = np.zeros((1, 71, 34, 114),dtype='f8')
    
    energy_shift_num = 9.24041641437038*10**18

    Abar = aav[0]  # shape == (71, 34, 114)
    Xa = Abar*0
    Xh = Abar*0
    Xn = Abar*0
    Xp = Abar*0
    Zbar = Abar*0
    cs2 = EOS[11]
    dedt = Abar*0                   # erg g^-1 K^-1       
    dpderho = EOS[10]*(convfmtocm**(-3))*nuetronMassCgs            # fm^-3  convert to  g cm^-3        
    dpdrhoe = (EOS[9]*convMeVtoGeV*convGeVtog)/nuetronMassCgs               # MeV convert to cm^2 s^-2
    energy_shift = np.array([energy_shift_num])
    entropy = EOS[1]
    gamma = EOS[14]
    logenergy = np.log10(((EOS[6])*clight_cgs**2)+energy_shift)  # change units?  E/mc^2 - 1 
                                                    # the log10 of the specific internal energy + the energy shift (to ensure positive energies) in erg/g)
    logpress = np.log10(EOS[0] * convMeVtoGeV * convGeVtog * convfmtocm**-3)    # MeV fm^-3 convert to dyn cm^-2 1MeV = 1.60217733E-6 dyn*cm
    logrho = np.log10(np.asarray(nb)*(convfmtocm**(-3))*nuetronMassCgs)         # already in MeV   shape should == (114,)
    logtemp = np.log10(temp)       # already in MeV   shape should == (34,)
    mu_e = EOS[4]-EOS[3]                 # already in MeV
    mu_n = EOS[2]+nuetronMassCgs*convgtoGeV*1e3
    mu_p = mu_n+EOS[3]                  # already in MeV
    muhat = EOS[2]                 # already in MeV
    munu = EOS[3]*0
    pointsrho = np.array([len(logrho)])
    pointstemp = np.array([len(logtemp)])
    pointsye = np.array([len(ye)])
    ye = ye        # shape should == (71,)
    P = OrderedDict()
    P['Abar'] = Abar
    P['Xa'] = Xa
    P['Xh'] = Xh
    P['Xn'] = Xn
    P['Xp'] = Xp
    P['Zbar'] = Zbar
    P['cs2'] = cs2
    P['dedt'] = dedt
    P['dpderho'] = dpderho
    P['dpdrhoe'] = dpdrhoe
    P['energy_shift'] = energy_shift
    P['entropy'] = entropy
    P['gamma'] = gamma
    P['logenergy'] = logenergy
    P['logpress'] = logpress
    P['logrho'] = logrho
    P['logtemp'] = logtemp
    P['mu_e'] = mu_e
    P['mu_n'] = mu_n
    P['mu_p'] = mu_p
    P['muhat'] = muhat
    P['munu'] = munu 
    P['pointsrho'] = pointsrho
    P['pointstemp'] = pointstemp 
    P['pointsye'] = pointsye 
    P['ye'] = ye 

    for i in P:
        n.create_dataset(i, data=P[i], track_order=True)
        
    print(n.keys())
        
    n.close()