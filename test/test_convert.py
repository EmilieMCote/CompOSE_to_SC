from socket import MsgFlag
import pytest
import numpy as np
import CompOSE_to_SC.conversion as conversion
import h5py
import os


filename = '../PracticeFiles/eoscomposeLS220.h5'
filename1 ='../PracticeFiles/eoscomposeLS220.tar.gz'
new_file = filename[:-3]+'_converted.h5'

print(new_file)

def test_conv_h5(filename, new_file):
    try:
        assert os.path.exists(filename), 'path for input file does not exist'
        assert filename[-3:]=='.h5', 'original file is not in h5 format'
        assert new_file[-3:]=='.h5', 'new file name chosen must have .h5 extension'
        print('files are h5 format')
    except AssertionError as msg:
        if str(msg) == 'original file is not in h5 format':
            try:
                assert 'tar' not in filename and 'zip' not in filename, 'original file is in a compressed format'
            except AssertionError as msg:
                print(msg)
    else:
        conversion.conv_h5(filename, new_file)
        try:
            assert os.path.exists(new_file), 'conv_h5 did not create a new file'
        except AssertionError as msg:
            print(msg)
        else:
            with h5py.File(new_file, 'r') as f:
                try:
                    assert list(f.keys()) == ['Abar', 'Xa', 'Xh', 'Xn', 'Xp', 'Zbar', 'cs2', 'dedt', 'dpderho', 'dpdrhoe', 'energy_shift', 'entropy', 'gamma', 'logenergy', 'logpress', 'logrho', 'logtemp', 'mu_e', 'mu_n', 'mu_p', 'muhat', 'munu', 'pointsrho', 'pointstemp', 'pointsye', 'ye'], 'new file does not contain all necessary Stellar Collapse keys, or they are not in the right order'
                except AssertionError as msg:
                    print(msg)
                else: 
                    print('new file has proper Stellar Collapse keys')

    
    
test_conv_h5(filename, new_file)

