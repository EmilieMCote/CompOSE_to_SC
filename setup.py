from setuptools import setup, find_packages
import tarfile
setup(
name='CompOSE_to_SC',
version='1.0.0',
packages=find_packages()
)

dir_path = 'PracticeFiles/'
f1tar = 'eoscomposeBHBDD2L.tar.gz'
f1h5 = f1tar.split('.')[0] + '.h5'
f2tar = 'eoscomposeLS220.tar.gz'
f2h5 = f2tar.split('.')[0] + '.h5'
with tarfile.open(dir+f1tar) as file:
    file.extractall('dir+f1h5')
with tarfile.open(dir+f2tar) as file:
    file.extractall('dir+f2h5')