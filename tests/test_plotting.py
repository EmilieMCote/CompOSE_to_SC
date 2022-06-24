from CompOSE_to_SC.conversion import conv_h5 as convert
from CompOSE_to_SC.plotting import plot_EOS
from os import system
import h5py
from matplotlib.figure import Figure
import tarfile
from os.path import split

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


def test_plotting():
    """Test plotting from a 'blank' H5 file

    Create a blank H5 file of all zeros and plot it

    Args:
        show (bool): whether to plot the figure

    Returns:
        None
    
    """
    url = 'https://stellarcollapse.org/~evanoc/Hempel_TMAEOS_rho234_temp180_ye60_version_1.1_20120817.h5.bz2'
    filename = download(url,'PracticeFiles/',True)
    fig = plot_EOS(filename)
    assert isinstance(fig,Figure)
    print('Single case worked')
    fig.show()

    fig = plot_EOS([filename])
    assert isinstance(fig,Figure)
    print('len=1 list case worked')
    fig.show()

    fig = plot_EOS([filename,filename])
    assert isinstance(fig,Figure)
    print('len=2 list case worked')
    fig.show()
    system('rm %s' % filename)
    