import wget
import tarfile

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

def download(url,untar_file = True):
    filename = url.split('/')[-1]
    response = wget.download(url,filename)
    if untar_file:
        return untar(filename)
    else:
        return filename