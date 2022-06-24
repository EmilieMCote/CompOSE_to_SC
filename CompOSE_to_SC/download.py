import wget
import tarfile
from os import system

def untar(path):
    """Untar practice files
    
    Decompress practice files for use in tests.
    Please remove these files after they are created with
    system('rm %s' % path)

    Args:
        None
    Returns:
        None
    """
    file =  tarfile.open(path)
    head,tail = split(path)
    file.extractall(head)
    file.close
    return head+ '/' +tail.split('.')[0] + '.h5'

def download(url,new_path = './',untar_file = True):
    filename = url.split('/')[-1]
    path = new_path+filename
    response = wget.download(url,path)
    if untar_file:
        if filename.split('.')[-1] == 'bz2':
            system('bzip2 -d %s' % path)
            return path.split('.')[0] + '.h5'
        else:
            return untar(path)
    else:
        return path