from socket import MsgFlag
import pytest
import numpy as np
import CompOSE_to_SC.conversion as conversion
import CompOSE_to_SC.download as dl
import h5py
import os
import shutil

h5_files = []

def look_for_test_file():
    for root, dir, files in os.walk('../PracticeFiles'):
        [h5_files.append(file) for file in files if file[-3:]=='.h5']
        print(h5_files)
    try:
        assert len(h5_files)>0, 'No EOS h5 files found in TestFiles directory'
    except AssertionError as msg:
        print(msg)
        dl('https://stellarcollapse.org/EOS/LS220_234r_136t_50y_analmu_20091212_SVNr26.h5.bz2')
        [h5_files.append(files[0]) for root, dir, files in os.walk('.') if file[-3:]=='.h5']
        shutil.move('./LS220_234r_136t_50y_analmu_20091212_SVNr26.h5', '../PracticeFiles/LS220_234r_136t_50y_analmu_20091212_SVNr26.h5')
        print(h5_files)


def test_conv_h5():
    '''
    Makes sure the input file exists
    Makes sure the input and output files are in h5 format
    Makes sure the new file contains the right StellarCollapse list of keys
    '''
    filename='../PracticeFiles/' + h5_files[0]
    new_file=filename[:-3]+'_converted.h5'

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
                    print('Everything seems to be working!')
                    os.remove(new_file)


if __name__ == '__main__':
   look_for_test_file()
   test_conv_h5() 
   
